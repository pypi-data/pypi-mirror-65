#!/usr/bin/env python

from __future__ import division, print_function
import sys
import argparse
import importlib.util
import inspect
import logging
import shutil
import faulthandler
import gc

import torch
from ignite.engine import Engine, Events
from torch.utils.tensorboard.writer import SummaryWriter
import torch.backends.cudnn as cudnn

import gammalearn.version as version
import gammalearn.utils as utils
import gammalearn.data_handlers as data_handlers
import gammalearn.handlers as handlers
from gammalearn.history import History
from gammalearn.metrics import BufferMetric, SingleBufferMetric

faulthandler.enable()


class Experiment(object):
    """Loads the settings of the experiment from the settings object,
    check them and defines default values for not specified ones.
    """
    def __init__(self, settings):
        """
        Parameters
        ----------
        settings : the object created from the settings.py import
        """
        self._logger = logging.getLogger(__name__)

        self.gpu_history = History()
        self.net = None
        self.optimizers = None
        self.tensorboard_writer = None
        self.gpu_frequency = None

        self._settings = settings
        # Load mandatory settings
        # Experiment settings
        self._has_mandatory('main_directory', 'where the experiments are stored')
        self.main_directory = settings.main_directory

        self._has_mandatory('experiment_name', 'the name of the experiment !')
        self.experiment_name = settings.experiment_name

        self._has_mandatory('CUDA_id', 'the gpu id to use. If -1, run on CPU')
        assert isinstance(getattr(settings, 'CUDA_id'), int), 'CUDA device id must be int !'
        self.device = utils.define_device(settings.CUDA_id)

        # Data settings
        self._has_mandatory('files_folders', 'the training and validating data folders')
        self.files_folders = settings.files_folders

        self._has_mandatory('dataset_class', 'the class to load the data')
        self.dataset_class = settings.dataset_class

        self._has_mandatory('dataset_parameters', 'the parameters of the dataset (camera type, group by option...)')
        self.dataset_parameters = settings.dataset_parameters
        utils.check_particle_mapping(self.dataset_parameters['particle_dict'])

        self._has_mandatory('validating_ratio', 'the ratio of data for validation')
        self.validating_ratio = settings.validating_ratio

        self._has_mandatory('nepochs', 'the maximum number of epochs')
        self.nepochs = settings.nepochs

        self._has_mandatory('batch_size', 'the batch size')
        self._is_positive('batch_size')
        self.batch_size = settings.batch_size

        self._has_mandatory('targets', 'the targets to reconstruct')
        self.targets = settings.targets
        if 'class' in self.targets:
            try:
                assert 'output_shape' not in self.targets['class']
            except AssertionError:
                self._logger.warning('Output shape of target class defined in settings will be overwritten with '
                                     'particle_dict length')
            self.targets['class']['output_shape'] = len(self.dataset_parameters['particle_dict'])

        # Net settings
        self._has_mandatory('net_definition_file', 'the file containing the net class')
        self.net_definition_file = settings.net_definition_file

        self._has_mandatory('net_parameters_dic', 'the parameters of the net described by a dictionary')
        assert isinstance(getattr(settings, 'net_parameters_dic'), dict), 'The net parameters must be a dict !'
        self.net_parameters_dic = settings.net_parameters_dic
        self.net_parameters_dic['targets'] = {k: v['output_shape'] for k, v in self.targets.items()}

        self._has_mandatory('model_net', 'the net to use')
        self.model_net = settings.model_net

        # Training settings
        self._has_mandatory('compute_loss', 'the function to compute the loss')
        self.compute_loss = settings.compute_loss

        self._has_mandatory('optimizer_parameters', 'the optimizers parameters described as a dictionary')
        self.optimizer_parameters = settings.optimizer_parameters

        self._has_mandatory('optimizer_dic', 'the optimizers described as a dictionary')
        self.optimizer_dic = settings.optimizer_dic

        self._has_mandatory('training_step', 'the function for the training step')
        self._is_function('training_step', 1)
        self.training_step = settings.training_step

        self._has_mandatory('eval_step', 'the function for the evaluation step')
        self._is_function('eval_step', 1)
        self.eval_step = settings.eval_step

        # Test settings
        self._has_mandatory('test', 'whether to test the model after training')
        self._is_of_type('test', bool)
        self.test = settings.test

        self._has_mandatory('use_gammaboard', 'whether or not to write files for gammaboard')
        self._is_of_type('use_gammaboard', bool)
        self.use_gammaboard = settings.use_gammaboard

        # Load optional settings
        # Experiment settings
        self.hooks = {}

        if hasattr(settings, 'info'):
            self._is_of_type('info', str)
            self.info = settings.info
        else:
            self.info = None

        if hasattr(settings, 'tensorboard'):
            self._is_of_type('tensorboard', bool)
            self.tensorboard = settings.tensorboard
        else:
            self.tensorboard = True

        if hasattr(settings, 'print_every'):
            self._is_positive('print_every')
            self.print_every = settings.print_every
        else:
            self.print_every = 100

        if hasattr(settings, 'save_every'):
            self._is_of_type('save_every', int)
            if settings.save_every > 0:
                self.save_every = settings.save_every
            else:
                self.save_every = -1
        else:
            self.save_every = None

        if hasattr(settings, 'window_size'):
            self._is_positive('window_size')
            self.window_size = settings.window_size
        else:
            self.window_size = 100

        if hasattr(settings, 'random_seed'):
            self._is_of_type('random_seed', int)
            self.random_seed = settings.random_seed
        else:
            self.random_seed = None

        if hasattr(settings, 'monitor_gpu'):
            self._is_of_type('monitor_gpu', bool)
            self.monitor_gpu = settings.monitor_gpu
        else:
            self.monitor_gpu = False

        if hasattr(settings, 'monitor_gpu_per_epoch'):
            self._is_of_type('monitor_gpu_per_epoch', int)
            self._is_positive('monitor_gpu_per_epoch')
            self.monitor_gpu_per_epoch = settings.monitor_gpu_per_epoch
        else:
            self.monitor_gpu_per_epoch = 5

        # Data settings
        if hasattr(settings, 'image_filter'):
            self._is_of_type('image_filter', dict)
            self.image_filter = settings.image_filter
        else:
            self.image_filter = None

        if hasattr(settings, 'event_filter'):
            self._is_of_type('event_filter', dict)
            self.event_filter = settings.event_filter
        else:
            self.event_filter = None

        if hasattr(settings, 'test_image_filter'):
            self._is_of_type('test_image_filter', dict)
            self.test_image_filter = settings.test_image_filter
        else:
            self.test_image_filter = None

        if hasattr(settings, 'test_event_filter'):
            self._is_of_type('test_event_filter', dict)
            self.test_event_filter = settings.test_event_filter
        else:
            self.test_event_filter = None

        if hasattr(settings, 'data_transform'):
            self._is_of_type('data_transform', dict)
            self.data_transform = settings.data_transform
        else:
            self.data_transform = None

        if hasattr(settings, 'data_augment'):
            self._is_of_type('data_augment', dict)
            self.data_augment = settings.data_augment
        else:
            self.data_augment = None

        if hasattr(settings, 'dataset_size'):
            self._is_of_type('dataset_size', int)
            self.dataset_size = settings.dataset_size
        else:
            self.dataset_size = None

        if hasattr(settings, 'files_max_number'):
            self._is_of_type('files_max_number', int)
            self.files_max_number = settings.files_max_number
        else:
            self.files_max_number = None

        if hasattr(settings, 'preprocessing_workers'):
            self._is_of_type('preprocessing_workers', int)
            if settings.preprocessing_workers > 0:
                self.preprocessing_workers = settings.preprocessing_workers
            else:
                self.preprocessing_workers = 0
        else:
            self.preprocessing_workers = 0

        if hasattr(settings, 'dataloader_workers'):
            self._is_of_type('dataloader_workers', int)
            if settings.dataloader_workers > 0:
                self.dataloader_workers = settings.dataloader_workers
            else:
                self.dataloader_workers = 0
        else:
            self.dataloader_workers = 0

        if hasattr(settings, 'mp_start_method'):
            self._is_of_type('mp_start_method', str)
            try:
                assert settings.mp_start_method in ['fork', 'spawn']
            except AssertionError:
                self.mp_start_method = torch.multiprocessing.get_start_method()
            else:
                self.mp_start_method = settings.mp_start_method
        else:
            self.mp_start_method = torch.multiprocessing.get_start_method()

        if hasattr(settings, 'pin_memory'):
            self._is_of_type('pin_memory', bool)
            self.pin_memory = settings.pin_memory
        else:
            self.pin_memory = False

        if hasattr(settings, 'split_by_file'):
            self._is_of_type('split_by_file', bool)
            self.split_by_file = settings.split_by_file
        else:
            self.split_by_file = True

        if hasattr(settings, 'test_folders'):
            self._is_of_type('test_folders', list)
            self.test_folders = settings.test_folders
        else:
            self.test_folders = None

        self.num_runs = None

        # Net settings
        if hasattr(settings, 'resume_path'):
            self.resume_path = settings.resume_path
        else:
            self.resume_path = None

        # Train settings
        if hasattr(settings, 'regularization'):
            self.regularization = settings.regularization
        else:
            self.regularization = None

        if hasattr(settings, 'validating_interval'):
            self._is_positive('validating_interval')
            self.validating_interval = settings.validating_interval
        else:
            self.validating_interval = 1

        if hasattr(settings, 'lr_scheduler_parameters'):
            self.lr_scheduler_parameters = settings.lr_scheduler_parameters
        else:
            self.lr_scheduler_parameters = None

        if hasattr(settings, 'regularization_handler_parameters'):
            self.regularization_handler_parameters = settings.regularization_handler_parameters
        else:
            self.regularization_handler_parameters = None

        # [testing settings]
        if self.test and self.use_gammaboard:
            self.gammaboard_directory = ''

        # [event handlers]
        if hasattr(settings, 'training_handlers'):
            self.training_handlers = settings.training_handlers
        else:
            self.training_handlers = None

        if hasattr(settings, 'training_metrics'):
            self._check_events_handlers('training_metrics', 1)
            self.training_metrics = settings.training_metrics
        else:
            self.training_metrics = None

        if hasattr(settings, 'validating_metrics'):
            self._check_events_handlers('validating_metrics', 1)
            self.validating_metrics = settings.validating_metrics
        else:
            self.validating_metrics = None

        if hasattr(settings, 'test_metrics'):
            self.test_metrics = settings.test_metrics
        else:
            self.test_metrics = None

        if hasattr(settings, 'training_model_metrics'):
            self._check_events_handlers('training_model_metrics', 1)
            self.training_model_metrics = settings.training_model_metrics
        else:
            self.training_model_metrics = None

        if hasattr(settings, 'validating_model_metrics'):
            self._check_events_handlers('validating_model_metrics', 1)
            self.validating_model_metrics = settings.validating_model_metrics
        else:
            self.validating_model_metrics = None

    def _has_mandatory(self, parameter, message):
        try:
            assert hasattr(self._settings, parameter)
        except AssertionError as err:
            self._logger.exception('Missing {param} : {msg}'.format(param=parameter, msg=message))
            raise err

    def _is_positive(self, parameter):
        message = 'Specification error on  {param}. It must be set above 0'.format(param=parameter)
        try:
            assert getattr(self._settings, parameter) > 0
        except AssertionError as err:
            self._logger.exception(message)
            raise err

    def _is_of_type(self, parameter, p_type):
        message = 'Specification error on  {param}. It must be of type {type}'.format(param=parameter,
                                                                                      type=p_type)
        try:
            assert isinstance(getattr(self._settings, parameter), p_type)
        except AssertionError as err:
            self._logger.exception(message)
            raise err

    def _is_function(self, parameter, n_args):
        message = 'Specification error on  {param}. It must be a function of {n_args} args'.format(param=parameter,
                                                                                                   n_args=n_args)
        try:
            assert inspect.isfunction(getattr(self._settings, parameter))
        except AssertionError as err:
            self._logger.exception(message)
            raise err
        try:
            assert len(inspect.getfullargspec(getattr(self._settings, parameter))[0]) == n_args
        except AssertionError as err:
            self._logger.exception(message)
            raise err

    def _check_events_handlers(self, parameter, n_args):
        """
        Function to check events handlers format as dictionary of ignite event : list of functions
        Parameters
        ----------
        parameter (str): name of the setting
        n_args (int): number of parameters of the functions

        Returns
        -------

        """
        message_1 = 'Specification error on  {param}. It must be a dictionary'.format(param=parameter)
        message_2 = 'Specification error on  {param}. Its keys must be of type TrainingEvents'.format(param=parameter)
        message_3 = 'Specification error on  {param}. Its values must be lists of functions'.format(param=parameter)
        message_4 = 'Specification error on  {param}. ' \
                    'Its values must be lists of functions with {n_args} args'.format(param=parameter,
                                                                                      n_args=n_args)
        _handlers = getattr(self._settings, parameter)
        try:
            assert isinstance(_handlers, dict)
        except AssertionError as err:
            self._logger.exception(message_1)
            raise err

        for key in _handlers:
            try:
                assert isinstance(key, Events)
            except AssertionError as err:
                self._logger.exception(message_2)
                raise err
            try:
                assert isinstance(_handlers[key], list)
            except AssertionError as err:
                self._logger.exception(message_3)
                raise err
            for func in _handlers[key]:
                try:
                    assert inspect.isfunction(func)
                except AssertionError as err:
                    self._logger.exception(message_3)
                    raise err
                try:
                    assert len(inspect.getfullargspec(func)[0]) == n_args
                except AssertionError as err:
                    self._logger.exception(message_4)
                    raise err


def main():

    # For better performance (if the input size does not vary from a batch to another)
    cudnn.benchmark = True
    
    logging_level = logging.INFO
    # Parse script arguments
    print('parse arguments')
    parser = argparse.ArgumentParser()
    parser.add_argument("configuration_file", help="path to configuration file")
    parser.add_argument("--debug", help="log useful information for debug purpose",
                        action="store_true")
    parser.add_argument("--logfile", help="whether to write the log on disk", action="store_true")
    args = parser.parse_args()
    configuration_file = args.configuration_file
    debug = args.debug
    logfile = args.logfile

    # Load logging config
    if debug:
        logging_level = logging.DEBUG
    logger = logging.getLogger()
    logger.setLevel(logging_level)
    for handler in logger.handlers:
        logger.removeHandler(handler)
    # create formatter
    if debug:
        formatter = logging.Formatter('[%(levelname)s] %(name)s - %(message)s')
    else:
        formatter = logging.Formatter('[%(levelname)s] - %(message)s')
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.debug('logger created')

    logger.info('gammalearn {}'.format(version.__version__))

    # load settings file
    logger.info('load settings')
    spec = importlib.util.spec_from_file_location("settings", configuration_file)
    settings = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(settings)

    # check config and prepare experiment
    experiment = Experiment(settings)

    # prepare folders
    logger.info('prepare folders')
    utils.prepare_experiment_folder(experiment.main_directory, experiment.experiment_name)
    if experiment.tensorboard:
        tensorboard_directory = utils.prepare_tensorboard_folder(experiment.main_directory, experiment.experiment_name)
        experiment.tensorboard_writer = SummaryWriter(tensorboard_directory)

    # record experiment in experiments.csv
    utils.record_experiment(experiment)

    # Prepare to log to file
    if logfile:
        formatter_file = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
        file_handler = logging.FileHandler('{}/{}/{}.log'.format(settings.main_directory,
                                                                 settings.experiment_name,
                                                                 settings.experiment_name))
        file_handler.setFormatter(formatter_file)
        logger.addHandler(file_handler)

    # print config
    utils.log_config(experiment)

    # save config(settings)
    logger.info('save configuration file')
    shutil.copyfile(configuration_file, '{}/{}/{}_settings.py'.format(experiment.main_directory,
                                                                      experiment.experiment_name,
                                                                      experiment.experiment_name))
    # dump settings
    utils.dump_experiment_config(experiment)

    # look for data and create datasets and dataloaders
    # set seed
    if experiment.random_seed is not None:
        torch.manual_seed(experiment.random_seed)
    logger.info('look for data files')
    datafiles_list = utils.find_datafiles(experiment.files_folders, experiment.files_max_number)
    logger.debug(datafiles_list)
    datafiles_list = list(datafiles_list)
    datafiles_list.sort()
    for file in datafiles_list:
        logger.debug('found : {}'.format(file))
    dataset = data_handlers.create_datasets_memory(datafiles_list, experiment)
    try:
        assert torch.multiprocessing.get_start_method() == experiment.mp_start_method
    except AssertionError:
        torch.multiprocessing.set_start_method(experiment.mp_start_method, force=True)
    logger.info('mp start method: {}'.format(torch.multiprocessing.get_start_method()))

    training_loader, validating_loader = data_handlers.create_dataloaders(dataset, experiment)

    # load camera parameters
    camera_parameters = utils.load_camera_parameters(experiment.dataset_parameters['camera_type'])

    # create network
    # reset seed
    if experiment.random_seed is not None:
        torch.manual_seed(experiment.random_seed)

    logger.info('Save net definition file')
    shutil.copyfile(experiment.net_definition_file, '{}/{}/nets.py'.format(experiment.main_directory,
                                                                           experiment.experiment_name))
    experiment.net = experiment.model_net(experiment.net_parameters_dic, camera_parameters)
    logger.info('network parameters number : {}'.format(utils.compute_total_parameter_number(experiment.net)))
    if experiment.resume_path is not None:
        logger.info('Load pretrained model : {}'.format(experiment.resume_path))
        utils.resume_model(experiment.net, experiment.resume_path)
    experiment.net.to(experiment.device)
    logger.info(('Experiment running on {}'.format(experiment.device)))
    if experiment.device.type == 'cuda':
        logger.info('GPU name : {}'.format(torch.cuda.get_device_name(experiment.device.index)))

    # put the loss function on the device if needed
    if isinstance(experiment.compute_loss, torch.nn.Module):
        experiment.compute_loss.to(experiment.device)
    # create optimizers
    experiment.optimizers = utils.load_optimizers(experiment.net, experiment)

    # create ignite net trainer
    logger.info('create net trainer')
    net_trainer = Engine(experiment.training_step(experiment))

    # create net evaluator
    net_evaluator = Engine(experiment.eval_step(experiment))

    # create net tester
    if experiment.test:
        net_tester = Engine(experiment.eval_step(experiment))
    else:
        net_tester = None

    training_metrics = {}
    # Attach metrics to trainer, validator and tester
    for task, param in experiment.targets.items():
        # Loss metric
        def transform_loss(task_):
            def transform(x):
                return torch.as_tensor(x[2][task_], dtype=torch.float).unsqueeze(dim=0)
            return transform
        metric = SingleBufferMetric(lambda x: x.mean(), window=experiment.window_size,
                                    output_transform=transform_loss(task))
        metric.attach(net_trainer, 'Loss_' + task)
        training_metrics['Loss_' + task] = metric

        SingleBufferMetric(lambda x: x.mean(),
                           output_transform=transform_loss(task)).attach(net_evaluator, 'Loss_' + task)

        # Other metrics
        for name, func in param['metrics'].items():
            def transform_output(task_):
                def transform(x):
                    return x[0][task_], x[1][task_].squeeze()
                return transform

            metric = BufferMetric(func, window=experiment.window_size,
                                  output_transform=transform_output(task))
            metric.attach(net_trainer, name + '_' + task)
            training_metrics[name + '_' + task] = metric

            BufferMetric(func, output_transform=transform_output(task)).attach(net_evaluator, name + '_' + task)

        # Store evaluator outputs (for resolution for example)
        def transform_eval_output(idx, task_):
            def transform(x):
                return x[idx][task_]
            return transform
        SingleBufferMetric(lambda x: x,
                           output_transform=transform_eval_output(0, task)).attach(net_evaluator, task + '_outputs')
        SingleBufferMetric(lambda x: x,
                           output_transform=transform_eval_output(1, task)).attach(net_evaluator, task + '_labels')
    SingleBufferMetric(lambda x: x, output_transform=lambda x: x[3]).attach(net_evaluator, 'mc_energy')
    SingleBufferMetric(lambda x: x, output_transform=lambda x: x[4]).attach(net_evaluator, 'tel_info')

    @net_trainer.on(Events.ITERATION_COMPLETED)
    def log_iteration_training_metrics(engine):
        itera = (engine.state.iteration - 1) % len(training_loader) + 1
        if itera % experiment.print_every == 0:
            logger.info("Epoch[{}] Iteration[{}/{}]".format(engine.state.epoch, itera, len(training_loader)))
            for n, m in training_metrics.items():
                iter_metric = m.compute()
                if torch.is_tensor(iter_metric):
                    if iter_metric.ndim > 0:
                        iter_metric = iter_metric.mean()
                    logger.info('Training ' + n + ' {:.4f}'.format(iter_metric))
                else:
                    logger.info('Training ' + n + ' {}'.format(iter_metric))
        if engine.state.iteration == 1 and experiment.tensorboard:
            total_loss = 0
            for n, m in training_metrics.items():
                iter_metric = m.compute()
                if torch.is_tensor(iter_metric) and iter_metric.ndim > 0:
                    iter_metric = iter_metric.mean()
                if 'Loss' in n:
                    total_loss += iter_metric
                    experiment.tensorboard_writer.add_scalars('Training', {n: iter_metric}, global_step=0)
            experiment.tensorboard_writer.add_scalars('Loss', {'training': total_loss}, global_step=0)

    @net_trainer.on(Events.EPOCH_COMPLETED)
    def log_epoch_training_metrics(engine):
        # TODO take into account loss balancing for total loss
        itera = (engine.state.iteration - 1) % len(training_loader) + 1
        metrics = engine.state.metrics
        logger.info("Epoch[{}] Iteration[{}/{}]".format(engine.state.epoch, itera, len(training_loader)))
        total_loss = 0
        for n, m in metrics.items():
            if torch.is_tensor(m):
                if m.ndim > 0:
                    m = m.mean()
                logger.info('Training ' + n + ' {:.4f}'.format(m))
            else:
                logger.info('Training ' + n + ' {}'.format(m))
            if experiment.tensorboard:
                if 'Loss' in n:
                    total_loss += m
                    experiment.tensorboard_writer.add_scalars('Training', {n: m},
                                                              global_step=net_trainer.state.epoch)
                elif 'Accuracy' in n:
                    experiment.tensorboard_writer.add_scalars('Accuracy', {'training': m},
                                                              global_step=net_trainer.state.epoch)
                elif 'AUC' in n:
                    experiment.tensorboard_writer.add_scalars('AUC', {'training': m},
                                                              global_step=net_trainer.state.epoch)
                elif 'Resolution' in n:
                    experiment.tensorboard_writer.add_scalars(n + '_training', m,
                                                              global_step=net_trainer.state.epoch)
                else:
                    experiment.tensorboard_writer.add_scalars(n, {'training': m},
                                                              global_step=net_trainer.state.epoch)
        if experiment.tensorboard:
            experiment.tensorboard_writer.add_scalars('Loss', {'training': total_loss},
                                                      global_step=net_trainer.state.epoch)

    @net_evaluator.on(Events.COMPLETED)
    def log_validating_metrics(engine):
        # TODO take into account loss balancing for total loss
        metrics = engine.state.metrics
        logger.info("Epoch[{}]".format(net_trainer.state.epoch))
        total_loss = 0
        for n, m in metrics.items():
            if not any(suffix in n for suffix in ['outputs', 'labels', 'mc_energy', 'tel_info']):
                if torch.is_tensor(m):
                    if m.ndim > 0:
                        m = m.mean()
                    logger.info('Validating ' + n + ' {:.4f}'.format(m))
                else:
                    logger.info('Validating ' + n + ' {}'.format(m))
                if experiment.tensorboard:
                    if 'Loss' in n:
                        total_loss += m
                        experiment.tensorboard_writer.add_scalars('Validating', {n: m},
                                                                  global_step=net_trainer.state.epoch)
                    elif 'Accuracy' in n:
                        experiment.tensorboard_writer.add_scalars('Accuracy', {'validating': m},
                                                                  global_step=net_trainer.state.epoch)
                    elif 'AUC' in n:
                        experiment.tensorboard_writer.add_scalars('AUC', {'validating': m},
                                                                  global_step=net_trainer.state.epoch)
                    elif 'Resolution' in n:
                        experiment.tensorboard_writer.add_scalars(n + '_validating', m,
                                                                  global_step=net_trainer.state.epoch)
                    else:
                        experiment.tensorboard_writer.add_scalars(n, {'validating': m},
                                                                  global_step=net_trainer.state.epoch)
        if experiment.tensorboard:
            experiment.tensorboard_writer.add_scalars('Loss', {'validating': total_loss},
                                                      global_step=net_trainer.state.epoch)

    # Attach evaluator to trainer
    @net_trainer.on(Events.EPOCH_COMPLETED)
    def validate(engine):
        if experiment.validating_ratio > 0:
            net_evaluator.trainer_epoch = engine.state.epoch
            net_evaluator.run(validating_loader)

    # add training handlers (fired after each validation)
    if experiment.training_handlers is not None:
        for create_handler, options in experiment.training_handlers.items():
            handler = create_handler(experiment, **options)
            if handler is not None:
                net_evaluator.add_event_handler(Events.COMPLETED, handler)

    # add saving net handler
    if experiment.save_every is not None:
        if experiment.save_every > 0:
            net_trainer.add_event_handler(Events.EPOCH_COMPLETED,
                                          handlers.create_save_model_handler(experiment))
        else:
            net_trainer.add_event_handler(Events.COMPLETED,
                                          handlers.create_save_model_handler(experiment))

    # add training model metrics handlers
    if experiment.training_model_metrics is not None:
        for key in experiment.training_model_metrics.keys():
            for create_handler in experiment.training_model_metrics[key]:
                handler = create_handler(experiment)
                if handler is not None:
                    net_trainer.add_event_handler(key, handler)

    # add validating model metrics handlers
    if experiment.validating_model_metrics is not None:
        for key in experiment.validating_model_metrics.keys():
            for create_handler in experiment.validating_model_metrics[key]:
                handler = create_handler(experiment)
                if handler is not None:
                    net_evaluator.add_event_handler(key, handler)

    # add gpu history handler
    if experiment.device.type == 'cuda' and experiment.monitor_gpu:
        # Register the GPU monitoring function
        try:
            assert len(training_loader) > experiment.monitor_gpu_per_epoch
        except AssertionError:
            experiment.monitor_gpu_per_epoch = len(training_loader)
        experiment.gpu_frequency = int(len(training_loader) / experiment.monitor_gpu_per_epoch)
        net_trainer.add_event_handler(Events.ITERATION_STARTED,
                                      handlers.create_store_gpu_history(experiment))

    # train network
    logger.info('run trainer')
    net_trainer.run(training_loader, max_epochs=experiment.nepochs)

    experiment.tensorboard_writer.close()

    # test network
    if experiment.test:
        logger.info('test model')

        for task, param in experiment.targets.items():
            # Loss metric
            def transform_loss(task_):
                def transform(x):
                    return torch.as_tensor(x[2][task_], dtype=torch.float).unsqueeze(dim=0)

                return transform

            SingleBufferMetric(lambda x: x.mean(),
                               output_transform=transform_loss(task)).attach(net_tester, 'Loss_' + task)

        @net_tester.on(Events.COMPLETED)
        def log_test_metrics(engine):
            # TODO take into account loss balancing for total loss
            metrics = engine.state.metrics
            logger.info('Test results')
            for n, m in metrics.items():
                if not any(suffix in n for suffix in ['outputs', 'labels', 'mc_energy', 'tel_info']):
                    if torch.is_tensor(m):
                        if m.ndim > 0:
                            m = m.mean()
                        logger.info(n + ' {:.4f}'.format(m))
                    else:
                        logger.info(n + ' {}'.format(m))

        # logger.info('look for data files')
        if experiment.test_folders is not None:
            # Try to free some memory
            del training_loader
            del validating_loader
            del dataset
            gc.collect()
            # Look for specific data filters
            if experiment.test_image_filter is not None:
                experiment.image_filter.update(experiment.test_image_filter)
            if experiment.test_event_filter is not None:
                experiment.event_filter.update(experiment.test_event_filter)
            # We need the fork start method to create datasets with multiprocessing
            try:
                assert torch.multiprocessing.get_start_method() == 'fork'
            except AssertionError:
                torch.multiprocessing.set_start_method('fork', force=True)
            test_loader = []
            for folder in experiment.test_folders:
                test_files_list = utils.find_datafiles([folder])
                logger.debug('test files : {}'.format(test_files_list))
                test_set = data_handlers.create_datasets_memory(test_files_list, experiment)
                test_loader.append(data_handlers.create_test_dataloaders(test_set, experiment))
            try:
                assert torch.multiprocessing.get_start_method() == experiment.mp_start_method
            except AssertionError:
                torch.multiprocessing.set_start_method(experiment.mp_start_method, force=True)
        else:
            test_loader = [validating_loader]

        if experiment.use_gammaboard:
            net_tester.add_event_handler(Events.COMPLETED, handlers.create_write_gammaboard_files(experiment))
            for task, param in experiment.targets.items():
                def transform_eval_output(idx, task_):
                    def transform(x):
                        return x[idx][task_]
                    return transform

                SingleBufferMetric(lambda x: x,
                                   output_transform=transform_eval_output(0, task)).attach(net_tester,
                                                                                           task + '_outputs')
                SingleBufferMetric(lambda x: x,
                                   output_transform=transform_eval_output(1, task)).attach(net_tester,
                                                                                           task + '_labels')
            SingleBufferMetric(lambda x: x, output_transform=lambda x: x[3]).attach(net_tester, 'mc_energy')
            SingleBufferMetric(lambda x: x, output_transform=lambda x: x[4]).attach(net_tester, 'tel_info')

        for t_loader in test_loader:
            experiment.test_loader = t_loader
            net_tester.run(t_loader, max_epochs=1)


if __name__ == '__main__':
    main()
