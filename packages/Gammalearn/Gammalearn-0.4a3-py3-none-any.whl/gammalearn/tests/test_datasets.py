import unittest
import collections
import numpy as np
import gammalearn.datasets as dsets
import gammalearn.utils as utils


class TestDL1DHDataset(unittest.TestCase):

    def setUp(self) -> None:
        self.data_file = '../../share/data/gamma_example.h5'
        self.camera_type = 'LST_LSTCam'
        self.particle_dict = {0: 1, 1: 0, 101: 0}
        self.targets = collections.OrderedDict({
            'energy': {
                'output_shape': 1,
                'unit': 'log10(TeV)',
            },
            'impact': {
                'output_shape': 2,
                'unit': 'km',
            },
            'direction': {
                'output_shape': 2,
                'unit': 'radian',
            },
            'class': {
                'output_shape': 2,
                'label_shape': 1,
                'unit': None,
            },
        })
        self.group_by_image = {
            0: {
                'image_0': np.float32(2.9275095),
                'image_950': np.float32(4.3886013),
                'image_1854': np.float32(-2.5380642),
                'time_0': np.float32(4.),
                'time_950': np.float32(18.),
                'time_1854': np.float32(20.),
                'labels': {
                    'energy': np.float32(0.01640345),
                    'corex': np.float32(-40.23255),
                    'corey': np.float32(-207.50215),
                    'alt': np.float32(1.2172362),
                    'az': np.float32(3.2659276)
                },
                'telescope': {
                    'alt': np.float32(1.2217305),
                    'az': np.float32(3.1415927),
                    'position': np.array([30.91, -64.54, 43.])
                }
            },
            16: {
                'image_0': np.float32(-1.663076),
                'image_950': np.float32(1.2384766),
                'image_1854': np.float32(.16535203),
                'time_0': np.float32(13.),
                'time_950': np.float32(14.),
                'time_1854': np.float32(31.),
                'labels': {
                    'energy': np.float32(0.03191287),
                    'corex': np.float32(-60.348785),
                    'corey': np.float32(40.010925),
                    'alt': np.float32(1.2556471),
                    'az': np.float32(3.1234822)
                },
                'telescope': {
                    'alt': np.float32(1.2217305),
                    'az': np.float32(3.1415927),
                    'position': np.array([30.91, -64.54, 43.])
                }
            },
        }

        self.group_by_all = {
            10: {
                'image_0': np.float32(-1.663076),
                'image_950': np.float32(1.2384766),
                'image_1854': np.float32(.16535203),
                'time_0': np.float32(13.),
                'time_950': np.float32(14.),
                'time_1854': np.float32(31.),
                'labels': {
                    'energy': np.float32(0.03191287),
                    'corex': np.float32(-60.348785),
                    'corey': np.float32(40.010925),
                    'alt': np.float32(1.2556471),
                    'az': np.float32(3.1234822)
                },
                'telescope': {
                    'alt': np.float32(1.2217305),
                    'az': np.float32(3.1415927),
                    'position': np.array([30.91, -64.54, 43.])
                }
            },
        }

        self.group_by_triggered = {
            12: {
                'image_0_0': np.float32(-1.6636664),
                'image_0_950': np.float32(-0.36771095),
                'image_0_1854': np.float32(-1.7226539),
                'time_0_0': np.float32(38.),
                'time_0_950': np.float32(8.),
                'time_0_1854': np.float32(10.),
                'image_1_0': np.float32(0.18670945),
                'image_1_950': np.float32(-0.013801108),
                'image_1_1854': np.float32(-2.0320477),
                'time_1_0': np.float32(0.),
                'time_1_950': np.float32(11.),
                'time_1_1854': np.float32(29.),
                'labels': {
                    'energy': np.float32(0.02468489),
                    'corex': np.float32(75.495895),
                    'corey': np.float32(-66.52175),
                    'alt': np.float32(1.1956633),
                    'az': np.float32(3.2049599)
                },
                'telescope': {
                    'alt': np.float32(1.2217305),
                    'az': np.float32(3.1415927),
                }
            },
        }

        self.energy_filter_parameters = {'energy': [0.02, 2], 'filter_only_gammas': True}
        self.energy_filter_true_events = 36

        self.amplitude_filter_parameters = {'amplitude': [50, np.inf]}

        self.tel_id_parameters = {'tel_id': 1}
        self.len_trig_energies = 27
        self.len_images = 28

    def test_mono_memory(self):

        dataset = dsets.MemoryDL1DHDataset(self.data_file, self.camera_type, 'image', self.targets, self.particle_dict,
                                           use_time=True)
        sample_0 = dataset[0]

        assert sample_0['image'][0, 0] == self.group_by_image[0]['image_0']
        assert sample_0['image'][0, 950] == self.group_by_image[0]['image_950']
        assert sample_0['image'][0, 1854] == self.group_by_image[0]['image_1854']
        assert sample_0['image'][1, 0] == self.group_by_image[0]['time_0']
        assert sample_0['image'][1, 950] == self.group_by_image[0]['time_950']
        assert sample_0['image'][1, 1854] == self.group_by_image[0]['time_1854']
        assert np.isclose(sample_0['label']['energy'], np.log10(self.group_by_image[0]['labels']['energy']))
        assert np.isclose(sample_0['mc_energy'], np.log10(self.group_by_image[0]['labels']['energy']))
        assert np.isclose(sample_0['label']['impact'][0], (self.group_by_image[0]['labels']['corex'] -
                                                           self.group_by_image[0]['telescope']['position'][0])/1000)
        assert np.isclose(sample_0['label']['impact'][1], (self.group_by_image[0]['labels']['corey'] -
                                                           self.group_by_image[0]['telescope']['position'][1]) / 1000)

        assert np.isclose(sample_0['label']['direction'][0], (self.group_by_image[0]['labels']['alt'] -
                                                              self.group_by_image[0]['telescope']['alt']))
        assert np.isclose(sample_0['label']['direction'][1], (self.group_by_image[0]['labels']['az'] -
                                                              self.group_by_image[0]['telescope']['az']))

        sample_16 = dataset[16]

        assert sample_16['image'][0, 0] == self.group_by_image[16]['image_0']
        assert sample_16['image'][0, 950] == self.group_by_image[16]['image_950']
        assert sample_16['image'][0, 1854] == self.group_by_image[16]['image_1854']
        assert sample_16['image'][1, 0] == self.group_by_image[16]['time_0']
        assert sample_16['image'][1, 950] == self.group_by_image[16]['time_950']
        assert sample_16['image'][1, 1854] == self.group_by_image[16]['time_1854']
        assert np.isclose(sample_16['label']['energy'], np.log10(self.group_by_image[16]['labels']['energy']))
        assert np.isclose(sample_16['mc_energy'], np.log10(self.group_by_image[16]['labels']['energy']))
        assert np.isclose(sample_16['label']['impact'][0], (self.group_by_image[16]['labels']['corex'] -
                                                            self.group_by_image[16]['telescope']['position'][0]) / 1000)
        assert np.isclose(sample_16['label']['impact'][1], (self.group_by_image[16]['labels']['corey'] -
                                                            self.group_by_image[16]['telescope']['position'][1]) / 1000)

        assert np.isclose(sample_16['label']['direction'][0], (self.group_by_image[16]['labels']['alt'] -
                                                               self.group_by_image[16]['telescope']['alt']))
        assert np.isclose(sample_16['label']['direction'][1], (self.group_by_image[16]['labels']['az'] -
                                                               self.group_by_image[16]['telescope']['az']))

    def test_stereo_all_memory(self):
        dataset = dsets.MemoryDL1DHDataset(self.data_file, self.camera_type, 'event_all_tels', self.targets,
                                           self.particle_dict, use_time=True)
        sample_10 = dataset[10]

        assert sample_10['image'][6, 0] == self.group_by_all[10]['image_0']
        assert sample_10['image'][6, 950] == self.group_by_all[10]['image_950']
        assert sample_10['image'][6, 1854] == self.group_by_all[10]['image_1854']
        assert sample_10['image'][7, 0] == self.group_by_all[10]['time_0']
        assert sample_10['image'][7, 950] == self.group_by_all[10]['time_950']
        assert sample_10['image'][7, 1854] == self.group_by_all[10]['time_1854']
        assert np.isclose(sample_10['label']['energy'], np.log10(self.group_by_all[10]['labels']['energy']))
        assert np.isclose(sample_10['mc_energy'], np.log10(self.group_by_all[10]['labels']['energy']))
        assert np.isclose(sample_10['label']['impact'][0], (self.group_by_all[10]['labels']['corex']) / 1000)
        assert np.isclose(sample_10['label']['impact'][1], (self.group_by_all[10]['labels']['corey']) / 1000)
        assert np.isclose(sample_10['label']['direction'][0], (self.group_by_all[10]['labels']['alt'] -
                                                               self.group_by_all[10]['telescope']['alt']))
        assert np.isclose(sample_10['label']['direction'][1], (self.group_by_all[10]['labels']['az'] -
                                                               self.group_by_all[10]['telescope']['az']))

    def test_stereo_triggered_memory(self):
        dataset = dsets.MemoryDL1DHDataset(self.data_file, self.camera_type, 'event_triggered_tels', self.targets,
                                           self.particle_dict, use_time=True)
        sample_12 = dataset[12]

        assert sample_12['image'][0, 0] == self.group_by_triggered[12]['image_0_0']
        assert sample_12['image'][0, 950] == self.group_by_triggered[12]['image_0_950']
        assert sample_12['image'][0, 1854] == self.group_by_triggered[12]['image_0_1854']
        assert sample_12['image'][1, 0] == self.group_by_triggered[12]['time_0_0']
        assert sample_12['image'][1, 950] == self.group_by_triggered[12]['time_0_950']
        assert sample_12['image'][1, 1854] == self.group_by_triggered[12]['time_0_1854']
        assert sample_12['image'][2, 0] == self.group_by_triggered[12]['image_1_0']
        assert sample_12['image'][2, 950] == self.group_by_triggered[12]['image_1_950']
        assert sample_12['image'][2, 1854] == self.group_by_triggered[12]['image_1_1854']
        assert sample_12['image'][3, 0] == self.group_by_triggered[12]['time_1_0']
        assert sample_12['image'][3, 950] == self.group_by_triggered[12]['time_1_950']
        assert sample_12['image'][3, 1854] == self.group_by_triggered[12]['time_1_1854']
        assert np.isclose(sample_12['label']['energy'], np.log10(self.group_by_triggered[12]['labels']['energy']))
        assert np.isclose(sample_12['mc_energy'], np.log10(self.group_by_triggered[12]['labels']['energy']))
        assert np.isclose(sample_12['label']['impact'][0], (self.group_by_triggered[12]['labels']['corex']) / 1000)
        assert np.isclose(sample_12['label']['impact'][1], (self.group_by_triggered[12]['labels']['corey']) / 1000)
        assert np.isclose(sample_12['label']['direction'][0], (self.group_by_triggered[12]['labels']['alt'] -
                                                               self.group_by_triggered[12]['telescope']['alt']))
        assert np.isclose(sample_12['label']['direction'][1], (self.group_by_triggered[12]['labels']['az'] -
                                                               self.group_by_triggered[12]['telescope']['az']))

    def test_mono_file(self):

        dataset = dsets.FileDL1DHDataset(self.data_file, self.camera_type, 'image', self.targets, self.particle_dict,
                                         use_time=True)
        sample_0 = dataset[0]

        assert sample_0['image'][0, 0] == self.group_by_image[0]['image_0']
        assert sample_0['image'][0, 950] == self.group_by_image[0]['image_950']
        assert sample_0['image'][0, 1854] == self.group_by_image[0]['image_1854']
        assert sample_0['image'][1, 0] == self.group_by_image[0]['time_0']
        assert sample_0['image'][1, 950] == self.group_by_image[0]['time_950']
        assert sample_0['image'][1, 1854] == self.group_by_image[0]['time_1854']
        assert np.isclose(sample_0['label']['energy'], np.log10(self.group_by_image[0]['labels']['energy']))
        assert np.isclose(sample_0['mc_energy'], np.log10(self.group_by_image[0]['labels']['energy']))
        assert np.isclose(sample_0['label']['impact'][0], (self.group_by_image[0]['labels']['corex'] -
                                                           self.group_by_image[0]['telescope']['position'][0])/1000)
        assert np.isclose(sample_0['label']['impact'][1], (self.group_by_image[0]['labels']['corey'] -
                                                           self.group_by_image[0]['telescope']['position'][1]) / 1000)

        assert np.isclose(sample_0['label']['direction'][0], (self.group_by_image[0]['labels']['alt'] -
                                                              self.group_by_image[0]['telescope']['alt']))
        assert np.isclose(sample_0['label']['direction'][1], (self.group_by_image[0]['labels']['az'] -
                                                              self.group_by_image[0]['telescope']['az']))

        sample_16 = dataset[16]

        assert sample_16['image'][0, 0] == self.group_by_image[16]['image_0']
        assert sample_16['image'][0, 950] == self.group_by_image[16]['image_950']
        assert sample_16['image'][0, 1854] == self.group_by_image[16]['image_1854']
        assert sample_16['image'][1, 0] == self.group_by_image[16]['time_0']
        assert sample_16['image'][1, 950] == self.group_by_image[16]['time_950']
        assert sample_16['image'][1, 1854] == self.group_by_image[16]['time_1854']
        assert np.isclose(sample_16['label']['energy'], np.log10(self.group_by_image[16]['labels']['energy']))
        assert np.isclose(sample_16['mc_energy'], np.log10(self.group_by_image[16]['labels']['energy']))
        assert np.isclose(sample_16['label']['impact'][0], (self.group_by_image[16]['labels']['corex'] -
                                                            self.group_by_image[16]['telescope']['position'][0]) / 1000)
        assert np.isclose(sample_16['label']['impact'][1], (self.group_by_image[16]['labels']['corey'] -
                                                            self.group_by_image[16]['telescope']['position'][1]) / 1000)

        assert np.isclose(sample_16['label']['direction'][0], (self.group_by_image[16]['labels']['alt'] -
                                                               self.group_by_image[16]['telescope']['alt']))
        assert np.isclose(sample_16['label']['direction'][1], (self.group_by_image[16]['labels']['az'] -
                                                               self.group_by_image[16]['telescope']['az']))

    def test_stereo_all_file(self):
        dataset = dsets.FileDL1DHDataset(self.data_file, self.camera_type, 'event_all_tels', self.targets,
                                         self.particle_dict, use_time=True)
        sample_10 = dataset[10]

        assert sample_10['image'][6, 0] == self.group_by_all[10]['image_0']
        assert sample_10['image'][6, 950] == self.group_by_all[10]['image_950']
        assert sample_10['image'][6, 1854] == self.group_by_all[10]['image_1854']
        assert sample_10['image'][7, 0] == self.group_by_all[10]['time_0']
        assert sample_10['image'][7, 950] == self.group_by_all[10]['time_950']
        assert sample_10['image'][7, 1854] == self.group_by_all[10]['time_1854']
        assert np.isclose(sample_10['label']['energy'], np.log10(self.group_by_all[10]['labels']['energy']))
        assert np.isclose(sample_10['mc_energy'], np.log10(self.group_by_all[10]['labels']['energy']))
        assert np.isclose(sample_10['label']['impact'][0], (self.group_by_all[10]['labels']['corex']) / 1000)
        assert np.isclose(sample_10['label']['impact'][1], (self.group_by_all[10]['labels']['corey']) / 1000)
        assert np.isclose(sample_10['label']['direction'][0], (self.group_by_all[10]['labels']['alt'] -
                                                               self.group_by_all[10]['telescope']['alt']))
        assert np.isclose(sample_10['label']['direction'][1], (self.group_by_all[10]['labels']['az'] -
                                                               self.group_by_all[10]['telescope']['az']))

    def test_stereo_triggered_file(self):
        dataset = dsets.FileDL1DHDataset(self.data_file, self.camera_type, 'event_triggered_tels', self.targets,
                                         self.particle_dict, use_time=True)
        sample_12 = dataset[12]

        assert sample_12['image'][0, 0] == self.group_by_triggered[12]['image_0_0']
        assert sample_12['image'][0, 950] == self.group_by_triggered[12]['image_0_950']
        assert sample_12['image'][0, 1854] == self.group_by_triggered[12]['image_0_1854']
        assert sample_12['image'][1, 0] == self.group_by_triggered[12]['time_0_0']
        assert sample_12['image'][1, 950] == self.group_by_triggered[12]['time_0_950']
        assert sample_12['image'][1, 1854] == self.group_by_triggered[12]['time_0_1854']
        assert sample_12['image'][2, 0] == self.group_by_triggered[12]['image_1_0']
        assert sample_12['image'][2, 950] == self.group_by_triggered[12]['image_1_950']
        assert sample_12['image'][2, 1854] == self.group_by_triggered[12]['image_1_1854']
        assert sample_12['image'][3, 0] == self.group_by_triggered[12]['time_1_0']
        assert sample_12['image'][3, 950] == self.group_by_triggered[12]['time_1_950']
        assert sample_12['image'][3, 1854] == self.group_by_triggered[12]['time_1_1854']
        assert np.isclose(sample_12['label']['energy'], np.log10(self.group_by_triggered[12]['labels']['energy']))
        assert np.isclose(sample_12['mc_energy'], np.log10(self.group_by_triggered[12]['labels']['energy']))
        assert np.isclose(sample_12['label']['impact'][0], (self.group_by_triggered[12]['labels']['corex']) / 1000)
        assert np.isclose(sample_12['label']['impact'][1], (self.group_by_triggered[12]['labels']['corey']) / 1000)
        assert np.isclose(sample_12['label']['direction'][0], (self.group_by_triggered[12]['labels']['alt'] -
                                                               self.group_by_triggered[12]['telescope']['alt']))
        assert np.isclose(sample_12['label']['direction'][1], (self.group_by_triggered[12]['labels']['az'] -
                                                               self.group_by_triggered[12]['telescope']['az']))

    def test_energy_filter_file(self):

        dataset_mono = dsets.FileDL1DHDataset(self.data_file, self.camera_type, 'image', self.targets,
                                              self.particle_dict, use_time=True)
        dataset_mono.filter_event({utils.energyband_filter: self.energy_filter_parameters})
        assert len(dataset_mono.energies) == self.energy_filter_true_events
        dataset_stereo_all = dsets.FileDL1DHDataset(self.data_file, self.camera_type, 'event_all_tels', self.targets,
                                                    self.particle_dict, use_time=True)
        dataset_stereo_all.filter_event({utils.energyband_filter: self.energy_filter_parameters})
        assert len(dataset_stereo_all.energies) == self.energy_filter_true_events
        dataset_stereo_trig = dsets.FileDL1DHDataset(self.data_file, self.camera_type, 'event_triggered_tels',
                                                     self.targets, self.particle_dict, use_time=True)
        dataset_stereo_trig.filter_event({utils.energyband_filter: self.energy_filter_parameters})
        assert len(dataset_stereo_trig.energies) == self.energy_filter_true_events

    def test_energy_filter_memory(self):

        dataset_mono = dsets.MemoryDL1DHDataset(self.data_file, self.camera_type, 'image', self.targets,
                                                self.particle_dict, use_time=True)
        dataset_mono.filter_event({utils.energyband_filter: self.energy_filter_parameters})
        assert len(dataset_mono.energies) == self.energy_filter_true_events
        dataset_stereo_all = dsets.MemoryDL1DHDataset(self.data_file, self.camera_type, 'event_all_tels', self.targets,
                                                      self.particle_dict, use_time=True)
        dataset_stereo_all.filter_event({utils.energyband_filter: self.energy_filter_parameters})
        assert len(dataset_stereo_all.energies) == self.energy_filter_true_events
        dataset_stereo_trig = dsets.MemoryDL1DHDataset(self.data_file, self.camera_type, 'event_triggered_tels',
                                                       self.targets, self.particle_dict, use_time=True)
        dataset_stereo_trig.filter_event({utils.energyband_filter: self.energy_filter_parameters})
        assert len(dataset_stereo_trig.energies) == self.energy_filter_true_events

    def test_amplitude_filter_memory(self):

        dataset_mono = dsets.MemoryDL1DHDataset(self.data_file, self.camera_type, 'image', self.targets,
                                                self.particle_dict, use_time=True)
        dataset_mono.filter_image({utils.amplitude_filter: self.amplitude_filter_parameters})
        assert len(dataset_mono.images) == len(np.unique(dataset_mono.image_indices))
        assert np.all(np.any(dataset_mono.image_indices))
        dataset_stereo_all = dsets.MemoryDL1DHDataset(self.data_file, self.camera_type, 'event_all_tels', self.targets,
                                                      self.particle_dict, use_time=True)
        dataset_stereo_all.filter_image({utils.amplitude_filter: self.amplitude_filter_parameters})
        assert len(dataset_stereo_all.images) == len(np.unique(dataset_stereo_all.image_indices))
        assert np.all(np.any(dataset_stereo_all.image_indices))
        dataset_stereo_trig = dsets.MemoryDL1DHDataset(self.data_file, self.camera_type, 'event_triggered_tels',
                                                       self.targets, self.particle_dict, use_time=True)
        dataset_stereo_trig.filter_image({utils.amplitude_filter: self.amplitude_filter_parameters})
        assert np.all(np.any(dataset_stereo_trig.image_indices))
        assert len(dataset_stereo_trig.images) == len(np.unique(dataset_stereo_trig.image_indices))

    def test_amplitude_filter_file(self):

        dataset_mono = dsets.FileDL1DHDataset(self.data_file, self.camera_type, 'image', self.targets,
                                              self.particle_dict, use_time=True)
        dataset_mono.filter_image({utils.amplitude_filter: self.amplitude_filter_parameters})
        assert len(dataset_mono.filtered_indices) == len(np.unique(dataset_mono.image_indices))
        assert np.all(np.any(dataset_mono.image_indices))
        dataset_stereo_all = dsets.FileDL1DHDataset(self.data_file, self.camera_type, 'event_all_tels', self.targets,
                                                    self.particle_dict, use_time=True)
        dataset_stereo_all.filter_image({utils.amplitude_filter: self.amplitude_filter_parameters})
        assert len(dataset_stereo_all.filtered_indices) == len(np.unique(dataset_stereo_all.image_indices))
        assert np.all(np.any(dataset_stereo_all.image_indices))
        dataset_stereo_trig = dsets.FileDL1DHDataset(self.data_file, self.camera_type, 'event_triggered_tels',
                                                     self.targets, self.particle_dict, use_time=True)
        dataset_stereo_trig.filter_image({utils.amplitude_filter: self.amplitude_filter_parameters})
        assert np.all(np.any(dataset_stereo_trig.image_indices))
        assert len(dataset_stereo_trig.filtered_indices) == len(np.unique(dataset_stereo_trig.image_indices))

    def test_tel_id_filter_memory(self):
        dataset_mono = dsets.MemoryDL1DHDataset(self.data_file, self.camera_type, 'image', self.targets,
                                                self.particle_dict, use_time=True)
        dataset_mono.filter_event({utils.telescope_id_filter: self.tel_id_parameters})
        assert len(dataset_mono.images) == self.len_images
        assert len(dataset_mono.trig_energies) == self.len_trig_energies


if __name__ == '__main__':
    unittest.main()
