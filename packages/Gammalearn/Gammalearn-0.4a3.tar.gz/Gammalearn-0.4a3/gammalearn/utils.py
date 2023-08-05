import os
import logging
import inspect
import csv
import subprocess
import collections
import json
import pkg_resources

import numpy as np
import tables
import torch
import torch.nn as nn
from ignite.engine import Events
from ctapipe.image import tailcuts_clean, leakage
from ctapipe.instrument import CameraGeometry
from ctaplot.ana import angular_separation_altaz
from gammalearn import version


def browse_folder(data_folder, extension=None):
    """
    Browse folder given to find hdf5 files
    Parameters
    ----------
    data_folder (string)
    extension (string)

    Returns
    -------
    set of hdf5 files
    """
    logger = logging.getLogger(__name__)
    if extension is None:
        extension = ['.hdf5', '.h5']
    try:
        assert isinstance(extension, list)
    except AssertionError as e:
        logger.exception('extension must be provided as a list')
        raise e
    logger.debug('browse folder')
    file_set = set()
    for dirname, dirnames, filenames in os.walk(data_folder):
        logger.debug('found folders : {}'.format(dirnames))
        logger.debug('in {}'.format(dirname))
        logger.debug('found files : {}'.format(filenames))
        for file in filenames:
            filename, ext = os.path.splitext(file)
            if ext in extension:
                file_set.add(dirname+'/'+file)
    return file_set


def prepare_experiment_folder(main_directory, experiment_name):
    """
    Prepare experiment folder and check if already exists
    Parameters
    ----------
    main_directory (string)
    experiment_name (string)

    Returns
    -------

    """
    logger = logging.getLogger(__name__)
    experiment_directory = main_directory + '/' + experiment_name + '/'
    if not os.path.exists(experiment_directory):
        os.makedirs(experiment_directory)
        os.chmod(experiment_directory, 0o775)
    else:
        logger.info('The experiment {} already exists !'.format(experiment_name))
    logger.info('Experiment directory: %s ' % experiment_directory)


def prepare_tensorboard_folder(main_directory, experiment_name):
    """
    Prepare tensorboard run folder for the experiment
    Parameters
    ----------
    main_directory (string)
    experiment_name (string)

    Returns
    -------

    """
    logger = logging.getLogger(__name__)
    run_directory = main_directory + '/runs/' + experiment_name
    if not os.path.exists(run_directory):
        os.makedirs(run_directory)
        os.chmod(run_directory, 0o775)
    logger.info('Tensorboard run directory: {} '.format(run_directory))
    return run_directory


def prepare_gammaboard_folder(main_directory, experiment_name):
    """
    Prepare tensorboard run folder for the experiment
    Parameters
    ----------
    main_directory (string)
    experiment_name (string)

    Returns
    -------

    """
    logger = logging.getLogger(__name__)
    test_directory = main_directory + '/gammaboard/' + experiment_name
    if not os.path.exists(test_directory):
        os.makedirs(test_directory)
        os.chmod(test_directory, 0o775)
    logger.debug('Gammaboard runs directory: {} '.format(test_directory))
    return test_directory


def record_experiment(experiment):
    """
    Record the main parameters of the experiment in a file containing all the experiments

    Parameters
    ----------
    experiment (Experiment) : experiment

    Returns
    -------

    """
    with open(experiment.main_directory + '/experiments.csv', 'a', newline='') as f:
        writer = csv.writer(f)

        optim = {}
        for key in experiment.optimizer_dic.keys():
            optim[key] = experiment.optimizer_dic[key].__name__

        criterion = {}
        for task, param in experiment.targets.items():
            criterion[task] = param['loss'].__name__ if inspect.isfunction(param['loss']) \
                else param['loss'].__class__.__name__

        writer.writerow([experiment.experiment_name,
                         experiment.model_net.__name__,
                         optim,
                         experiment.optimizer_parameters,
                         criterion,
                         experiment.batch_size,
                         experiment.nepochs,
                         experiment.image_filter,
                         experiment.event_filter,
                         experiment.files_folders])


def resume_model(model, path):
    """
    Resume the model with the one stored in the path.
    https://discuss.pytorch.org/t/how-to-load-part-of-pre-trained-model/1113/16
    Parameters
    ----------
    model (torch.Module)
    path (string)

    Returns
    -------

    """
    pretrained_dict = torch.load(f=path,  map_location=lambda storage, loc: storage)
    model_dict = model.state_dict()
    # 1. filter out unnecessary keys (not in the model)
    pretrained_dict = {k: v for k, v in pretrained_dict.items() if
                       k in model_dict and not ('mask_' in k or 'indices_' in k)}
    # 2. overwrite entries in the existing state dict
    model_dict.update(pretrained_dict)
    # 3. load the new state dict
    model.load_state_dict(model_dict)


def define_device(cuda_id):
    """
    Define the cuda devices id to use according to the id of devices in configuration file
    Parameters
    ----------
    cuda_id

    Returns
    -------
    """
    logger = logging.getLogger(__name__)

    if torch.cuda.is_available() and not (cuda_id == -1):
        if cuda_id is list:
            id = cuda_id[0]
            logger.debug('cuda device used : {}'.format(id))
        else:
            id = cuda_id
            logger.debug('cuda device used : {}'.format(id))
        device = torch.device('cuda:' + str(id))
        logger.info('GPU name : {}'.format(torch.cuda.get_device_name(id)))

    else:
        logger.debug('no cuda device used, run on CPU')
        device = torch.device('cpu')

    return device
    # TODO take into account multi GPUs with DataParallel


def find_datafiles(data_folders, files_max_number=0):
    """
    Find datafiles in the folders specified
    Parameters
    ----------
    data_folders (list): the folders where the data are stored
    files_max_number (int, optional): the maximum number of files to keep per folder

    Returns
    -------

    """
    logger = logging.getLogger(__name__)
    logger.debug('data folders : {}'.format(data_folders))
    # We can have several folders
    datafiles = set()
    for folder in data_folders:
        logger.debug('data folder : {}'.format(folder))
        dataf = list(browse_folder(folder))
        dataf.sort()
        if files_max_number and 0 < files_max_number <= len(dataf):
            dataf = dataf[0:files_max_number]
        dataf = set(dataf)
        datafiles.update(dataf)

    return datafiles


def is_datafile_healthy(file_path):
    """
    Check that the data file does not contain empty dataset
    Parameters
    ----------
    file_path (str): the path to the file

    Returns
    -------
    A boolean
    """
    dataset_emptiness = []

    _, ext = os.path.splitext(file_path)
    if ext in ['.hdf5', '.h5']:
        with tables.File(file_path, 'r') as f:
            for n in f.walk_nodes():
                if isinstance(n, tables.Table):
                    dataset_emptiness.append(n.shape[0])
    return not np.any(np.array(dataset_emptiness) == 0)


def load_optimizers(net, experiment):
    """
    Loads the optimizers using functions in optimizer_dic
    Parameters
    ----------
    net
    experiment

    Returns
    -------

    """
    logger = logging.getLogger(__name__)
    optim_keys = experiment.optimizer_dic.keys()
    if 'network' in optim_keys:
        assert not any(key in optim_keys for key in ['feature', 'classifier', 'regressor']), \
            'If you define an optimizer for the whole network, you cannot also define an optimizer for a subpart of it.'
    if 'feature' in optim_keys:
        assert 'classifier' in optim_keys or 'regressor' in optim_keys, \
            'You need an optimizer for every subparts of the net.'

    optimizers = {}
    for key in experiment.optimizer_dic.keys():
        if key == 'network':
            optimizers[key] = experiment.optimizer_dic[key](net, experiment.optimizer_parameters[key])
        elif key == 'feature':
            optimizers[key] = experiment.optimizer_dic[key](net.feature, experiment.optimizer_parameters[key])
        elif key == 'classifier':
            optimizers[key] = experiment.optimizer_dic[key](net.classifier, experiment.optimizer_parameters[key])
        elif key == 'regressor':
            optimizers[key] = experiment.optimizer_dic[key](net.regressor, experiment.optimizer_parameters[key])
        elif key == 'loss_balancing':
            assert isinstance(experiment.compute_loss, nn.Module)
            optimizers[key] = experiment.optimizer_dic[key](experiment.compute_loss,
                                                            experiment.optimizer_parameters[key])
        logger.debug('{} : {}'.format(key, optimizers[key]))

    return optimizers


def log_config(experiment):
    """
    Print the configuration parameters on screen
    Parameters
    ----------
    experiment (Experiment)

    Returns
    -------

    """
    logger = logging.getLogger('settings')
    logger.debug('*' * 40)
    logger.debug('Experiment settings')
    attrs = experiment.__dict__
    log_dic(attrs, logger)
    logger.debug('*' * 40)


def log_dic(dic, logger):
    """
    Print a dictionary of experiment parameters
    Parameters
    ----------
    dic
    logger

    Returns
    -------

    """
    for key in dic.keys():
        if isinstance(dic[key], dict):
            logger.debug('{} :'.format(key))
            log_dic(dic[key], logger)
        elif isinstance(dic[key], list):
            for val in dic[key]:
                log_parameter(key, val, logger)
        else:
            log_parameter(key, dic[key], logger)


def log_parameter(name, value, logger):
    """
    Print an experiment parameter and its value
    Parameters
    ----------
    name
    value
    logger

    Returns
    -------

    """
    if inspect.isfunction(value) | inspect.isclass(value) | inspect.ismodule(value):
        value = value.__name__
    elif isinstance(value, nn.Module):
        value = value.__class__.__name__
    if isinstance(name, str):
        if not name.startswith('_'):
            logger.debug('{} : {}'.format(name, value))
    elif isinstance(name, Events):
        logger.debug('{} : {}'.format(name.name, value))
    else:
        logger.debug('{} : {}'.format(name, value))


def get_gpu_usage_map(device_id):
    """Get the current gpu usage.
    inspired from : https://discuss.pytorch.org/t/access-gpu-memory-usage-in-pytorch/3192/4
    Parameters
    ----------
    device_id (int): the GPU id as GPU/Unit's 0-based index in the natural enumeration returned  by
       the driver
    Returns
    -------
    usage: dict
        Keys are device ids as integers.
        Values are memory usage as integers in MB, total memory usage as integers in MB, gpu utilization in %.
    """
    result = subprocess.check_output(
        [
            'nvidia-smi', '--id=' + str(device_id), '--query-gpu=memory.used,memory.total,utilization.gpu',
            '--format=csv,nounits,noheader'
        ], encoding='utf-8')
    # Convert lines into a dictionary
    gpu_usage = [int(y) for y in result.split(',')]
    gpu_usage_map = {'memory_used': gpu_usage[0], 'total_memory': gpu_usage[1], 'utilization': gpu_usage[2]}

    return gpu_usage_map


def compute_total_parameter_number(net):
    """
    Compute the total number of parameters of a network
    Parameters
    ----------
    net (nn.Module): the network

    Returns
    -------
    int: the number of parameters
    """
    num_parameters = 0
    for name, param in net.named_parameters():
        num_parameters += param.clone().cpu().data.view(-1).size(0)

    return num_parameters


def load_camera_parameters(camera_type):
    """
    Load camera parameters : nbCol and injTable
    Parameters
    ----------
    datafiles (List) : files to load data from
    camera_type (str): the type of camera to load data for ; eg 'LST_LSTCam'

    Returns
    -------
    A dictionary
    """
    camera_parameters = {}
    if camera_type == 'LST':
        camera_type = 'LST_LSTCam'
    if camera_type in ['LST_LSTCam', 'MST_FlashCam', 'MST_NectarCam', 'CIFAR']:
        camera_parameters['layout'] = 'Hex'
    else:
        camera_parameters['layout'] = 'Square'
    camera_parameters_file = pkg_resources.resource_filename(__name__, 'data/camera_parameters.h5')
    with tables.File(camera_parameters_file, 'r') as hdf5_file:
        camera_parameters['nbRow'] = hdf5_file.root[camera_type]._v_attrs.nbRow
        camera_parameters['nbCol'] = hdf5_file.root[camera_type]._v_attrs.nbCol
        camera_parameters['injTable'] = hdf5_file.root[camera_type].injTable[()]
        camera_parameters['pixelsPosition'] = hdf5_file.root[camera_type].pixelsPosition[()]

    return camera_parameters


def dump_experiment_config(experiment):
    """
    Load experiment info from the settings file
    Parameters
    ----------
    experiment (Experiment): experiment

    Returns
    -------

    """
    exp_settings = collections.OrderedDict({'exp_name': experiment.experiment_name,
                                            'gammalearn': version.__version__,
                                            'files_folders': experiment.files_folders,
                                            'dataset_class': experiment.dataset_class.__name__,
                                            'dataset_parameters': experiment.dataset_parameters,
                                            'num_epochs': experiment.nepochs,
                                            'batch_size': experiment.batch_size,
                                            })
    if experiment.info is not None:
        exp_settings['info'] = experiment.info
    if experiment.image_filter is not None:
        exp_settings['image filters'] = {filter_func.__name__: filter_param
                                         for filter_func, filter_param
                                         in experiment.image_filter.items()}
    if experiment.event_filter is not None:
        exp_settings['event filters'] = {filter_func.__name__: filter_param
                                         for filter_func, filter_param
                                         in experiment.event_filter.items()}
    if experiment.data_augment is not None:
        exp_settings['data_augmentation'] = {
            experiment.data_augment['function'].__name__: experiment.data_augment['kwargs']
        }
    exp_settings['network'] = {experiment.model_net.__name__: experiment.net_parameters_dic}
    exp_settings['losses'] = {
        k: {
            'loss': v['loss'].__name__ if inspect.isfunction(v['loss']) else v['loss'].__class__.__name__,
            'weight': v['loss_weight']
        }
        for k, v in experiment.targets.items()
    }
    if inspect.isfunction(experiment.compute_loss):
        exp_settings['loss_function'] = experiment.compute_loss.__name__
    else:
        exp_settings['loss_function'] = experiment.compute_loss.__class__.__name__
    exp_settings['optimizer'] = {key: value.__name__ for key, value in experiment.optimizer_dic.items()}
    exp_settings['optimizer_parameters'] = {opt: {key: value.__name__ if isinstance(value, type) else value
                                                  for key, value in param.items()}
                                            for opt, param in experiment.optimizer_parameters.items()}
    if experiment.training_handlers is not None:
        exp_settings['training_handlers'] = {handler.__name__: param
                                             for handler, param in experiment.training_handlers.items()}
    if experiment.lr_scheduler_parameters is not None:
        exp_settings['lr_scheduler_parameters'] = experiment.lr_scheduler_parameters
    if experiment.test_folders is not None:
        exp_settings['test_folders'] = experiment.test_folders
    settings_path = experiment.main_directory + '/' + experiment.experiment_name + \
                    '/' + experiment.experiment_name + '_settings.json'
    with open(settings_path, 'w') as f:
        json.dump(exp_settings, f)


def check_particle_mapping(particle_dict):
    assert len(particle_dict) == len(set(particle_dict.values())), 'Each mc particle type must have its own class'


###########
# Filters #
###########
##################################################################################################
# Event base filters

def energyband_filter(dataset, energy=None, filter_only_gammas=False):
    """
    Filter dataset on energy (in TeV)
    Parameters
    ----------
    dataset (Dataset) : the dataset to filter
    energy
    filter_only_gammas

    Returns
    -------
    (list of bool): the mask to filter the data
    """
    if energy is None:
        energy = [0, np.inf]
    en_min = np.log10(energy[0])
    en_max = np.log10(energy[1])
    energy_mask = (dataset.energies > en_min) & (dataset.energies < en_max)
    if filter_only_gammas:
        energy_mask = energy_mask | (dataset.cta_particle_types != 0)
    return energy_mask


def telescope_multiplicity_filter(dataset, multiplicity, strict=False):
    """
    Filter dataset on number of telescopes that triggered (for a particular type of telescope)
    Parameters
    ----------
    dataset (Dataset): the dataset to filter
    multiplicity (int): the number of telescopes that triggered
    strict (bool)

    Returns
    -------
    (list of bool): the mask to filter the data
    """
    if strict:
        event_mask = np.count_nonzero(dataset.image_indices, axis=1) == multiplicity
        trig_mask = np.count_nonzero(dataset.trig_image_indices, axis=1) == multiplicity
    else:
        event_mask = np.count_nonzero(dataset.image_indices, axis=1) >= multiplicity
        trig_mask = np.count_nonzero(dataset.trig_image_indices, axis=1) >= multiplicity
    dataset.trig_image_indices = dataset.trig_image_indices[trig_mask]
    dataset.trig_energies = dataset.trig_energies[trig_mask]

    return event_mask


def telescope_id_filter(dataset, tel_id, strict=False):
    """
    Filter dataset on telescope id
    Parameters
    ----------
    dataset (Dataset) : the dataset to filter
    tel_id (int or list of int)
    strict (bool)

    Returns
    -------
    (list of bool): the mask to filter the data
    """
    if isinstance(tel_id, int):
        # filter triggered energies
        tel_idx = np.argwhere(dataset.tel_ids == tel_id).item()
        mask = dataset.trig_image_indices[:, tel_idx] > 0
        # update image_indices
        id_mask = np.full(dataset.image_indices.shape[1], True)
        id_mask[tel_idx] = False
        dataset.image_indices[:, id_mask] = 0
        dataset.trig_image_indices = dataset.trig_image_indices[mask]
        dataset.trig_image_indices[:, id_mask] = 0
        dataset.trig_energies = dataset.trig_energies[mask]
        return dataset.image_indices[:, tel_idx] > 0
    elif isinstance(tel_id, list):
        tel_idx = list(map(lambda x: np.argwhere(dataset.tel_ids == x).item(), tel_id))
        id_mask = np.full(dataset.image_indices.shape[1], True)
        id_mask[tel_idx] = False
        if strict:
            event_mask = np.full(len(dataset.image_indices), True)
            trig_mask = np.full(len(dataset.trig_image_indices), True)
            for idx in tel_idx:
                event_mask &= dataset.image_indices[:, idx] > 0
                trig_mask &= dataset.trig_image_indices[:, idx] > 0
        else:
            event_mask = np.full(len(dataset.image_indices), False)
            trig_mask = np.full(len(dataset.trig_image_indices), False)
            for idx in tel_idx:
                event_mask |= dataset.image_indices[:, idx] > 0
                trig_mask |= dataset.trig_image_indices[:, idx] > 0
        dataset.image_indices[:, id_mask] = 0
        dataset.trig_image_indices = dataset.trig_image_indices[trig_mask]
        dataset.trig_image_indices[:, id_mask] = 0
        dataset.trig_energies = dataset.trig_energies[trig_mask]
        return event_mask


def emission_cone_filter(dataset, max_angle=np.inf):
    """
    Filter the dataset on the maximum distance between the impact point and the telescope position in km
    Parameters
    ----------
    dataset (Dataset): the dataset to filter
    max_angle (float): the max angle between the telescope pointing direction and the direction of the shower in rad

    Returns
    -------
    (list of bool): the mask to filter the data
    """
    tel_alt = np.full(len(dataset.altitudes), dataset.tel_altitude)
    tel_az = np.full(len(dataset.azimuths), dataset.tel_azimuth)
    for t in dataset.targets:
        if t == 'direction':
            if dataset.targets[t]['unit'] == 'degrees':
                separations = angular_separation_altaz(np.deg2rad(dataset.altitudes),
                                                       np.deg2rad(dataset.azimuths),
                                                       np.deg2rad(tel_alt),
                                                       np.deg2rad(tel_az))
                break
    else:
        separations = angular_separation_altaz(dataset.altitudes, dataset.azimuths, tel_alt, tel_az)
    return separations <= max_angle


def impact_distance_filter(dataset, max_distance=np.inf):
    """
    Filter the dataset on the maximum distance between the impact point and the telescope position in km
    Parameters
    ----------
    dataset (Dataset): the dataset to filter
    max_distance (float): the maximum distance between the impact point and the telescope position in km

    Returns
    -------
    (list of bool): the mask to filter the data
        """
    scale = 1
    for t in dataset.targets:
        if t == 'impact':
            if dataset.targets[t]['unit'] == 'm':
                scale = 1000
    for i, position in enumerate(dataset.tel_positions):
        distances = np.sqrt((dataset.xCores - position[0]) ** 2 + (dataset.yCores - position[1]) ** 2)
        dataset.image_indices[distances > max_distance*scale, i] = 0

    return np.any(dataset.image_indices, axis=1)


##################################################################################################
# Image base filters

def amplitude_filter(dataset, amplitude=None):
    """
    Filter dataset on amplitude (in pe)
    Parameters
    ----------
    dataset (Dataset) : the dataset to filter
    amplitude

    Returns
    -------
    (list of bool): the mask to filter the data
    """
    if amplitude is None:
        amplitude = [-np.inf, np.inf]
    pe_min = amplitude[0]
    pe_max = amplitude[1]
    amps = dataset.images.sum(axis=-1)
    mask1 = pe_min < amps
    mask2 = amps < pe_max
    mask = mask1 & mask2
    return mask


def cleaning_filter(dataset, **opts):
    """
    Filter images according to a cleaning operation.

    Parameters
    ----------
    dataset: `Dataset`

    Returns
    -------
    (list of bool): the mask to filter the data
    """
    camera_type = 'LST_LSTCam' if dataset.camera_type == 'LST' else dataset.camera_type
    geom = CameraGeometry.from_name(camera_type.split('_')[1])  # camera_type is of form LST_LSTCam

    def clean(img):
        return tailcuts_clean(geom, img, **opts)

    clean_mask = np.apply_along_axis(clean, 1, dataset.images)
    mask = clean_mask.any(axis=1)

    return mask


def leakage_filter(dataset, leakage1_cut=None, leakage2_cut=None, **opts):
    """
    Filter images according to a cleaning operation.

    Parameters
    ----------
    dataset: `Dataset`
    leakage1_cut: `int`
    leakage2_cut: `int`

    Returns
    -------
    (list of bool): the mask to filter the data
    """
    assert leakage1_cut is not None or leakage2_cut is not None, 'Leakage filter: At least one cut must be defined'
    camera_type = 'LST_LSTCam' if dataset.camera_type == 'LST' else dataset.camera_type
    geom = CameraGeometry.from_name(camera_type.split('_')[1])  # camera_type is of form LST_LSTCam

    def leak2(img):
        mask = tailcuts_clean(geom, img, **opts)
        if np.any(mask):
            return leakage(geom, img, mask).leakage2_intensity
        else:
            return 1.

    def leak1(img):
        mask = tailcuts_clean(geom, img, **opts)
        if np.any(mask):
            return leakage(geom, img, mask).leakage1_intensity
        else:
            return 1.

    if leakage1_cut is not None:
        image_leak1 = np.apply_along_axis(leak1, 1, dataset.images)
        img_mask1 = image_leak1 < leakage1_cut
    else:
        img_mask1 = np.full(dataset.images.shape[0], True)

    if leakage2_cut is not None:
        image_leak2 = np.apply_along_axis(leak2, 1, dataset.images)
        img_mask2 = image_leak2 < leakage2_cut
    else:
        img_mask2 = np.full(dataset.images.shape[0], True)

    img_mask = img_mask1 & img_mask2

    return img_mask


###################
# Transformations #
###################

def rotated_indices(pixels_position, theta):
    """
    Function that returns the rotated indices of an image from the pixels position.
    Parameters
    ----------
    pixels_position (numpy.Array): an array of the position of the pixels
    theta (float): angle of rotation

    Returns
    -------
    Rotated indices
    """
    from math import isclose
    rot_indices = np.zeros(len(pixels_position)).astype(np.int)
    rotation_matrix = [[np.cos(theta), -np.sin(theta)],
                       [np.sin(theta), np.cos(theta)]]
    new_pix_pos = np.matmul(rotation_matrix, pixels_position.T).T.astype(np.float32)

    for i, pos in enumerate(new_pix_pos):
        for j, old_pos in enumerate(pixels_position):
            if isclose(old_pos[0], pos[0], abs_tol=10e-5) and isclose(old_pos[1], pos[1], abs_tol=10e-5):
                rot_indices[j] = i
    assert len(set(list(rot_indices))) == len(pixels_position), \
        'Rotated indices do not match the length of pixels position.'

    return rot_indices


# TODO move to transforms
def center_time(dataset, **opts):
    """
    Filter images according to a cleaning operation.

    Parameters
    ----------
    dataset: `Dataset`

    Returns
    -------
    indices: `numpy.array`
    """
    geom = CameraGeometry.from_name(dataset.camera_type.split('_')[1])  # camera_type is of form LST_LSTCam

    def clean(img):
        return tailcuts_clean(geom, img, **opts)

    clean_mask = np.apply_along_axis(clean, 1, dataset.images)

    cleaned = dataset.images * clean_mask
    max_pix = cleaned.argmax(axis=1)
    for i, times in enumerate(dataset.times):
        times -= times[max_pix[i]]


# TODO move to transforms
def rgb_to_grays(dataset):
    """
    Function to convert RGB images to 2 channels gray images.
    Parameters
    ----------
    dataset (Dataset)
    """
    assert dataset.images.ndim in [3, 4]
    assert dataset.images.shape[1] == 3
    d_size = dataset.images.shape
    gamma = 2.2
    new_images = np.empty((d_size[0], 2) + d_size[2:], dtype=np.float32)
    new_images[:, 0:1] = np.sum(dataset.images, 1, keepdims=True)  # Naive sum
    new_images[:, 1:] = (0.2126 * dataset.images[:, 0:1]**gamma
                         + 0.7152 * dataset.images[:, 1:2]**gamma
                         + 0.0722 * dataset.images[:, 2:]**gamma)  # weighted sum

    dataset.images = new_images

    return np.arange(len(dataset))
