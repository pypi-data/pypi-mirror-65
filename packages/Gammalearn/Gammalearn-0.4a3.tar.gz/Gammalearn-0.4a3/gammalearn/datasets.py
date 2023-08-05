import multiprocessing as mp
import copy

import tables
import numpy as np
import torch
from torch.utils.data import Dataset
from torchvision.transforms import Compose
from ctapipe.instrument import CameraGeometry
from ctapipe.image import tailcuts_clean
from ctapipe.io.containers import MCHeaderContainer
import pandas as pd

import gammalearn.utils as utils


class BaseDL1DHDataset(Dataset):
    """camera simulation dataset for DL1DH hdf5 files. """

    def __init__(self, hdf5_file_path, camera_type, group_by, targets, particle_dict, use_time=False, transform=None,
                 target_transform=None, telescope_transform=None):
        """
        Parameters
        ----------
            hdf5_file_path (str): path to hdf5 file containing the data
            camera_type (str) : name of the camera used (e.g. camera_type='LST')
            group_by (str): the way to group images in the dataset (e.g. 'event_triggered_tels' :
            by event only for telescopes which triggered)
            targets (list): the targets to include in the sample
            particle_dict (dict): Dictionary of particle types
            use_time (bool, optional): whether or not include the time peak in the sample
            transform (callable, optional): Optional transform to be applied on a sample
            target_transform (callable, optional): Optional transform to be applied on a sample
            telescope_transform (callable, optional): Optional transform to be applied on a sample
        """
        self.hdf5_file_path = hdf5_file_path
        self.hdf5_file = None
        self.camera_type = camera_type
        self.targets = targets
        self.particle_dict = particle_dict
        self.transform = transform
        self.target_transform = target_transform
        self.telescope_transform = telescope_transform
        self.use_time = use_time

        self.images = None
        self.times = None
        self.filtered_indices = None
        self.altitudes = None
        self.azimuths = None
        self.xCores = None
        self.yCores = None
        self.height_first = None
        self.xmax = None

        group_by_options = ['image', 'event_all_tels', 'event_triggered_tels']

        assert group_by in group_by_options, '{} is not a suitable group option. Must be in {}'.format(group_by,
                                                                                                       group_by_options)

        self.group_by = group_by

        self.run_config = {}

        with tables.File(hdf5_file_path, 'r') as hdf5_file:
            # Load run config
            mcheader = {}
            for attr in hdf5_file.root._v_attrs._f_list('user'):
                if attr in ['ctapipe_version', 'dl1_data_handler_version', 'runlist']:
                    self.run_config[attr] = hdf5_file.root._v_attrs[attr]
                else:
                    mcheader[attr] = hdf5_file.root._v_attrs[attr]
                self.run_config[attr] = hdf5_file.root._v_attrs[attr]
            self.run_config['mcheader'] = MCHeaderContainer(**mcheader)

            # Load event info
            self.multiplicity = hdf5_file.root.Events[:][self.camera_type + '_multiplicity'][()]
            indices_mask = self.multiplicity > 0
            self.image_indices = hdf5_file.root.Events[:][self.camera_type + '_indices'][()][indices_mask]
            self.multiplicity = self.multiplicity[indices_mask]
            # Energy is always in log
            self.energies = np.log10(hdf5_file.root.Events[:]['mc_energy'][()][indices_mask], dtype=np.float32)
            self.cta_particle_types = hdf5_file.root.Events[:]['shower_primary_id'][()][indices_mask]
            self.event_ids = hdf5_file.root.Events[:]['event_id'][()][indices_mask]
            self.run_ids = hdf5_file.root.Events[:]['obs_id'][()][indices_mask]

            self.xCores = hdf5_file.root.Events[:]['core_x'][()][indices_mask]
            self.yCores = hdf5_file.root.Events[:]['core_y'][()][indices_mask]
            self.altitudes = hdf5_file.root.Events[:]['alt'][()][indices_mask]
            self.azimuths = hdf5_file.root.Events[:]['az'][()][indices_mask]

            # Load array info
            tel_info_mask = np.in1d(hdf5_file.root.Array_Information[:]['type'], self.camera_type.encode('ascii'))
            self.tel_ids = hdf5_file.root.Array_Information[tel_info_mask]['id'][()]
            self.tel_positions = np.column_stack((hdf5_file.root.Array_Information[tel_info_mask]['x'][()],
                                                  hdf5_file.root.Array_Information[tel_info_mask]['y'][()],
                                                  hdf5_file.root.Array_Information[tel_info_mask]['z'][()]))
            self.tel_altitude = hdf5_file.root._v_attrs.run_array_direction[1]
            self.tel_azimuth = hdf5_file.root._v_attrs.run_array_direction[0]

            # Keep a copy of triggered energies and image indices for gammaboard
            self.trig_energies = self.energies.copy()
            self.trig_image_indices = self.image_indices.copy()

            # Load targets info
            for t in self.targets:
                if t == 'impact':
                    if self.targets[t]['unit'] == 'km':
                        self.xCores /= 1000
                        self.yCores /= 1000
                        self.tel_positions /= 1000
                    elif self.targets[t]['unit'] != 'm':
                        raise ValueError('Unknown unit')
                elif t == 'direction':
                    if self.targets[t]['unit'] == 'degrees':
                        self.altitudes = np.rad2deg(self.altitudes, dtype=np.float32)  # direction in degrees
                        self.azimuths = np.rad2deg(self.azimuths, dtype=np.float32)   # direction in degrees
                        self.tel_altitude = np.rad2deg(self.tel_altitude, dtype=np.float32)
                        self.tel_azimuth = np.rad2deg(self.tel_azimuth, dtype=np.float32)
                elif t == 'xmax':
                    self.xmax = hdf5_file.root.Events[:]['x_max'][()][indices_mask]
                    self.xmax = self.xmax / 1000
                elif t == 'height_first':
                    self.height_first = hdf5_file.root.Events[:]['h_first_int'][()][indices_mask]

    def __len__(self):
        if self.group_by == 'image':
            return len(self.filtered_indices) - 1 if len(self.filtered_indices) > 0 else 0
        else:
            return len(self.energies)

    def _get_sample(self, idx):
        if self.group_by == 'image':
            # first image is full of zeros
            idx = idx + 1
            data_t = self._get_image_data(idx)
            if self.use_time:
                data = np.stack(data_t)
            else:
                data = data_t[0]
            image_id = self.filtered_indices[idx]
            event_mask = np.any(np.in1d(self.image_indices, image_id).reshape(self.image_indices.shape), axis=1)
            event_id = np.arange(len(self.energies))[event_mask].item()

            tel_id = np.argwhere(self.image_indices[event_id] == image_id).item()
            tel_altitude = self.tel_altitude
            tel_azimuth = self.tel_azimuth
            tel_position = self.tel_positions[tel_id]
            tel_info = np.concatenate(([tel_altitude, tel_azimuth], tel_position))
        else:
            event_id = idx
            if self.group_by == 'event_all_tels':
                # We want as many images as telescopes
                images_ids = self.image_indices[event_id]
                tel_positions = self.tel_positions
            elif self.group_by == 'event_triggered_tels':
                images_ids = self.image_indices[event_id][self.image_indices[event_id] != 0]
                tel_positions = self.tel_positions[self.image_indices[event_id] != 0]
            else:
                raise ValueError('group_by option has an incorrect value.')
            data_t = self._get_image_data(images_ids)
            tel_info = np.column_stack((np.full(tel_positions.shape[0], self.tel_altitude),
                                        np.full(tel_positions.shape[0], self.tel_azimuth), tel_positions))
            if self.use_time:
                assert len(data_t) == 2, 'When using both charge and peakpos you need the same' \
                                               'amount of each'
                event_images = data_t[0]
                event_times = data_t[1]
                data = np.empty((event_images.shape[0]*2, event_images.shape[1]), dtype=np.float32)
                data[0::2, :] = event_images
                data[1::2, :] = event_times
            else:
                data = data_t[0]
        labels = {}
        for t in self.targets:
            if t == 'energy':
                labels[t] = np.array([self.energies[event_id]])
            elif t == 'impact':
                if self.group_by == 'image':
                    labels[t] = np.array([self.xCores[event_id] - tel_info[2], self.yCores[event_id] - tel_info[3]])
                else:
                    labels[t] = np.array([self.xCores[event_id], self.yCores[event_id]])
            elif t == 'direction':
                labels[t] = np.array([self.altitudes[event_id] - self.tel_altitude.item(),
                                      self.azimuths[event_id] - self.tel_azimuth.item()], dtype=np.float32)
            elif t == 'xmax':
                labels[t] = np.array([self.xmax[event_id]])
            elif t == 'class':
                labels[t] = self.particle_dict[self.cta_particle_types[event_id]]
            else:
                raise ValueError('Unknown target')

        sample = {'image': data, 'telescope': tel_info, 'label': labels,
                  'mc_energy': self.energies[event_id]}

        if self.transform:
            sample['image'] = self.transform(sample['image'])
        if self.target_transform:
            sample['label'] = {t: self.target_transform(label) for t, label in sample['label'].items()}
            sample['mc_energy'] = self.target_transform(sample['mc_energy'])
        if self.telescope_transform:
            sample['telescope'] = self.telescope_transform(sample['telescope'])

        return sample

    def _get_image_data(self, idx):
        raise NotImplementedError

    def filter_event(self, filter_dict):
        filter_mask = np.full(len(self.energies), True)
        for filter_func, params in filter_dict.items():
            filter_mask = filter_mask & filter_func(self, **params)
        # Apply filtering
        self._update_events(filter_mask)
        # update images filtered ids
        new_indices = np.unique(self.image_indices)
        image_mask = np.in1d(self.filtered_indices, new_indices)
        self.filtered_indices = new_indices
        # update images
        self._update_images(image_mask)
        # update multiplicity
        self.multiplicity = np.count_nonzero(self.image_indices, axis=1)

    def _update_events(self, filter_mask):
        self.image_indices = self.image_indices[filter_mask]
        self.multiplicity = self.multiplicity[filter_mask]
        self.energies = self.energies[filter_mask]
        self.cta_particle_types = self.cta_particle_types[filter_mask]
        self.event_ids = self.event_ids[filter_mask]
        self.run_ids = self.run_ids[filter_mask]
        self.xCores = self.xCores[filter_mask]
        self.yCores = self.yCores[filter_mask]
        self.altitudes = self.altitudes[filter_mask]
        self.azimuths = self.azimuths[filter_mask]
        self.xmax = self.xmax[filter_mask] if self.xmax is not None else self.xmax
        self.height_first = self.height_first[filter_mask] if self.height_first is not None else self.height_first

    def _filter_image(self, filter_dict):
        filter_mask = np.full(len(self.images), True)
        for filter_func, params in filter_dict.items():
            filter_mask = filter_mask & filter_func(self, **params)
        # First image is full of zeros, we want to keep it for stereo
        filter_mask[0] = True
        # Apply filtering
        self.filtered_indices = np.arange(len(self.images))[filter_mask]
        self.images = self.images[filter_mask]
        if self.times is not None:
            self.times = self.times[filter_mask]
        # update indices
        ids_mask = np.in1d(self.image_indices, self.filtered_indices).reshape(self.image_indices.shape)
        self.image_indices[~ids_mask] = 0
        # update multiplicity
        self.multiplicity = np.count_nonzero(self.image_indices, axis=1)
        # update events
        event_mask = np.any(self.image_indices, axis=1)
        self._update_events(event_mask)

    def _update_images(self, image_mask):
        if self.images is not None:
            self.images = self.images[image_mask]
        if self.times is not None:
            self.times = self.times[image_mask]

    def filter_image(self, filter_dict):

        raise NotImplementedError


class MemoryDL1DHDataset(BaseDL1DHDataset):

    def __init__(self, hdf5_file_path, camera_type, group_by, targets, particle_dict, use_time=False, transform=None,
                 target_transform=None, telescope_transform=None):

        super(MemoryDL1DHDataset, self).__init__(hdf5_file_path, camera_type, group_by, targets, particle_dict,
                                                 use_time, transform, target_transform, telescope_transform)

        with tables.File(hdf5_file_path, 'r') as hdf5_file:
            # Load images and peak times
            self.images = hdf5_file.root[self.camera_type][:]['charge'][()]
            if self.use_time:
                self.times = hdf5_file.root[self.camera_type][:]['peakpos'][()]
        self.filtered_indices = np.arange(len(self.images))

    def __getitem__(self, idx):
        return self._get_sample(idx)

    def _get_image_data(self, idx):
        data = (self.images[idx],)
        if self.use_time:
            data += self.times[idx],
        return data

    def filter_image(self, filter_dict):
        self._filter_image(filter_dict)


class FileDL1DHDataset(BaseDL1DHDataset):

    def __init__(self, hdf5_file_path, camera_type, group_by, targets, particle_dict, use_time=False, transform=None,
                 target_transform=None, telescope_transform=None):

        super(FileDL1DHDataset, self).__init__(hdf5_file_path, camera_type, group_by, targets, particle_dict,
                                               use_time, transform, target_transform, telescope_transform)

        with tables.File(hdf5_file_path, 'r') as hdf5_file:
            self.filtered_indices = np.arange(len(hdf5_file.root[self.camera_type]))

    def __len__(self):
        if self.group_by == 'image':
            return len(self.filtered_indices) - 1
        else:
            return len(self.energies)

    def __getitem__(self, idx):
        if self.hdf5_file is None:
            self.hdf5_file = tables.File(self.hdf5_file_path, 'r')
        return self._get_sample(idx)

    def _get_image_data(self, idx):
        data = self.hdf5_file.root[self.camera_type][idx]['charge'],
        if self.use_time:
            data += self.hdf5_file.root[self.camera_type][idx]['peakpos'],
        return data

    def filter_image(self, filter_dict):
        self._open_file()
        self._filter_image(filter_dict)
        self._close_file()

    def _open_file(self):
        if self.hdf5_file is None:
            self.hdf5_file = tables.File(self.hdf5_file_path, 'r')
            self.images = self.hdf5_file.root[self.camera_type][:]['charge']
            self.times = self.hdf5_file.root[self.camera_type][:]['peakpos']

    def _close_file(self):
        if self.hdf5_file is not None:
            self.hdf5_file.close()
            self.hdf5_file = None
            self.images = None
            self.times = None


class RealDataSet(Dataset):
    # TODO add target and transform to dataset parameter dictionary before instanciating Dataset
    def __init__(self, file, camera_type=None, targets=None,
                 transform=None, target_transform=None, telescope_transform=None,):
        with tables.open_file(file) as f:
            event_ids = \
                f.root.dl1.event.telescope.parameters.LST_LSTCam.read_where('(intensity >= 300) & (leakage < 0.2)')[
                    'event_id']
            mask = np.isin(f.root.dl1.event.telescope.image.LST_LSTCam[:]['event_id'], event_ids)
            image = f.root.dl1.event.telescope.image.LST_LSTCam[:]['image'][mask]
            time = f.root.dl1.event.telescope.image.LST_LSTCam[:]['pulse_time'][mask]
            time = np.minimum(40, np.maximum(0, time))
            self.event_id = f.root.dl1.event.telescope.image.LST_LSTCam[:]['event_id'][mask]
        self.data = np.stack((image, time), axis=1)
        geom_002 = CameraGeometry.from_name('LSTCam-002')
        geom_simu = CameraGeometry.from_name('LSTCam')
        self.injtable = geom_002.position_to_pix_index(geom_simu.pix_y, geom_simu.pix_x)

    def __len__(self):
        return len(self.event_id)

    def __getitem__(self, idx):
        data = self.data[idx]
        return {'image': torch.tensor(data[..., self.injtable]).float(),
                'event_id': self.event_id[idx]
                }


class NumpyDataset(Dataset):

    def __init__(self, data, labels, transform=None, target_transform=None):
        self.images = data
        self.labels = labels
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, item):

        if self.transform:
            self.images[item] = self.transform(self.images[item])
        if self.target_transform:
            self.labels[item] = self.target_transform(self.labels[item])

        return self.images[item], self.labels[item]


class HDF5Dataset(Dataset):
    """Loads data in a Dataset from a HDF5 file.

    Args:
        path (str): The path to the HDF5 file.
        transform (callable, optional): A callable or a composition of callable to be applied to the data.
        target_transform (callable, optional): A callable or a composition of callable to be applied to the labels.
    """
    def __init__(self, path, camera_type, transform=None, target_transform=None, telescope_transform=None):
        with tables.File(path, 'r') as f:
            self.images = f.root['images'][:][()]
            self.labels = f.root['labels'][:][()]
        self.transform = transform
        self.target_transform = target_transform
        self.camera_type = camera_type

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, item):
        image, label = self.images[item], self.labels[item]
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.transform(label)

        return {'image': image, 'label': label}


# Transforms classes

class Unsqueeze(object):
    """Unsqueeze a tensor"""
    def __call__(self, data):
        data.unsqueeze_(0)
        return data


class NumpyToTensor(object):
    """Convert a numpy array to a tensor"""

    def __call__(self, data):
        data = torch.tensor(data)
        return data


class RotateImage(object):
    """Rotate telescope image based on rotated indices"""

    def __init__(self, rotated_indices):
        self.rotated_indices = rotated_indices

    def __call__(self, data):
        assert data.shape[-1] == self.rotated_indices.shape[0], 'The length of rotated indices must match the size ' \
                                                                'of the image to rotate. '
        return data[..., self.rotated_indices]


class NormalizePixel(object):

    def __init__(self, max_pix):
        self.max = max_pix

    def __call__(self, data):
        return data / self.max


class CleanImages(object):

    def __init__(self, camera_type, **opts):
        self.opts = opts
        camera_type = 'LST_LSTCam' if camera_type == 'LST' else camera_type
        self.geom = CameraGeometry.from_name(camera_type.split('_')[1])  # camera_type is of form LST_LSTCam

    def __call__(self, data):
        image = data if data.ndim == 1 else data[0]
        clean_mask = tailcuts_clean(self.geom, image, **self.opts)

        return data * clean_mask


# Augment data functions

def augment_via_rotation(datasets, thetas, num_workers):
    """
    Function to augment dataset via image rotation
    Parameters
    ----------
    datasets (list): list of Subsets
    thetas (list): list of thetas (in rad)
    num_workers (int): number of processes to use

    Returns
    -------

    """
    def process_subset():
        torch.set_num_threads(1)
        while True:
            if input_queue.empty():
                break
            else:
                sub = input_queue.get()
            for theta in thetas:
                pixels_position = utils.load_camera_parameters(sub.dataset.camera_type)['pixelsPosition']
                rot_indices = utils.rotated_indices(pixels_position, theta)
                new_subset = copy.copy(sub)
                new_subset.dataset.transform = Compose([RotateImage(rot_indices)] + sub.dataset.transform.transforms)
                new_datasets.append(new_subset)

    input_queue = mp.Queue()
    for subset in datasets:
        input_queue.put(subset)
    manager = mp.Manager()
    new_datasets = manager.list()
    workers = [mp.Process(target=process_subset) for _ in range(num_workers)]
    for w in workers:
        w.start()
    input_queue.close()
    for w in workers:
        w.join()

    datasets += list(new_datasets)

    return datasets


def augment_via_duplication(datasets, scale, num_workers):
    """
    Augment data by duplicating events based on the inverse detected energies distribution
    Parameters
    ----------
    datasets (list): list of Subsets
    scale (float): the scale to constrain the maximum duplication factor
    num_workers (int): number of processes to use

    Returns
    -------

    """
    def get_factor(energy, scale):
        fitlog = 1.19 * (2.59 - energy) * (1 - np.exp(-2.91 - energy))
        p = 1/(10**fitlog) * 1/(1/(10**fitlog)).min()
        return np.floor(1 + scale * np.log10(p)).astype(np.int)

    def process_subset():
        torch.set_num_threads(1)
        while True:
            if input_queue.empty():
                break
            else:
                sub = input_queue.get()
                factors = get_factor(np.log10(sub.dataset.energies), scale)
                augmented_ids = np.repeat(np.arange(len(sub.dataset)), factors)
                sub.indices = augmented_ids[np.in1d(augmented_ids, sub.indices)]
                new_datasets.append(sub)

    input_queue = mp.Queue()
    for subset in datasets:
        input_queue.put(subset)
    manager = mp.Manager()
    new_datasets = manager.list()
    workers = [mp.Process(target=process_subset) for _ in range(num_workers)]
    for w in workers:
        w.start()
    input_queue.close()
    for w in workers:
        w.join()
    return list(new_datasets)
