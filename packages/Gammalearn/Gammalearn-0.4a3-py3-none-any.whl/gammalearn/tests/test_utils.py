import unittest
import gammalearn.utils as utils
import numpy as np


class MockDataset(object):

    def __init__(self):

        self.images = np.array([np.full(1855, 0.001),
                                np.full(1855, 1),
                                np.full(1855, 0.0001),
                                np.full(1855, 0.1)])
        self.images[3, 903:910] = 30
        self.images[2, 1799:1806] = 10  # for cleaning and leakage
        self.energies = np.log10(np.array([0.010, 2.5, 0.12, 0.8]))
        self.trig_energies = self.energies.copy()
        self.group_by = 'image'
        self.camera_type = 'LST_LSTCam'
        self.cta_particle_types = np.array([1, 0, 0, 0])
        self.tel_altitude = np.deg2rad(70)
        self.tel_azimuth = np.deg2rad(180)
        self.altitudes = np.deg2rad([71, 75, 68, 69])
        self.azimuths = np.deg2rad([180, 180, 179.5, 175])
        self.targets = {'direction': {'unit': 'radian'},
                        'impact': {'unit': 'm'}}
        self.image_indices = np.array([[0, 1, 0],
                                       [2, 3, 0],
                                       [0, 0, 4],
                                       [5, 0, 0]])
        self.trig_image_indices = self.image_indices.copy()
        self.tel_positions = np.array([[-70.93, -52.07, 54],
                                       [75.28, 50.46, 39.7],
                                       [-70.93, 53.1, 42]])
        self.xCores = np.array([50.3, -150, -100, 100])
        self.yCores = np.array([48, -51, 0, 0])
        self.tel_ids = np.array([1, 2, 3])

    def __len__(self):
        return len(self.images)


class TestUtils(unittest.TestCase):

    def setUp(self) -> None:

        self.amplitude_filter_parameters = [300, np.inf]
        self.amplitude_true_mask = [False, True, False, True]

        self.cleaning_filter_parameters = {'picture_thresh': 6, 'boundary_thresh': 3,
                                           'keep_isolated_pixels': False, 'min_number_picture_neighbors': 2}
        self.cleaning_true_mask = [False, False, True, True]

        self.leakage_parameters = {'leakage2_cut': 0.2, 'picture_thresh': 6, 'boundary_thresh': 3,
                                   'keep_isolated_pixels': False, 'min_number_picture_neighbors': 2}
        self.leakage_true_mask = [False, False, False, True]

        self.energy_parameters = {'energy': [0.02, 2], 'filter_only_gammas': True}
        self.energy_true_mask = [True, False, True, True]

        self.telescope_id_parameters = {'tel_id': 1}
        self.tel_true_mask = [False, True, False, True]
        self.tel_true_image_indices = np.array([[0, 0, 0],
                                                [2, 0, 0],
                                                [0, 0, 0],
                                                [5, 0, 0]])
        self.telescope_id_list_parameters = {'tel_id': [1, 2]}
        self.tel_list_true_mask = [True, True, False, True]
        self.telescope_id_list_strict_parameters = {'tel_id': [1, 2], 'strict': True}
        self.tel_list_strict_true_mask = [False, True, False, False]
        self.tel_list_strict_true_image_indices = np.array([[0, 1, 0],
                                                            [2, 3, 0],
                                                            [0, 0, 0],
                                                            [5, 0, 0]])

        self.emission_cone_parameters = {'max_angle': np.deg2rad(4.)}
        self.emission_cone_true_mask = [True, False, True, True]

        self.impact_distance_parameters = {'max_distance': 0.05}
        self.impact_distance_true_indices = np.array([[0, 1, 0],
                                                      [0, 0, 0],
                                                      [0, 0, 0],
                                                      [0, 0, 0]])
        self.impact_distance_true_mask = [True, False, False, False]

        self.multiplicity_parameters = {'multiplicity': 1}
        self.multiplicity_true_mask = [True, True, True, True]
        self.multiplicity_strict_parameters = {'multiplicity': 1, 'strict': True}
        self.multiplicity_strict_true_mask = [True, False, True, True]
        self.multiplicity_strict_true_trig_image_indices = np.array([[0, 1, 0],
                                                                     [0, 0, 4],
                                                                     [5, 0, 0]])
        self.multiplicity_strict_true_trig_energies = np.log10(np.array([0.010, 0.12, 0.8]))

    def test_amplitude(self):
        self.dataset = MockDataset()
        assert np.all(utils.amplitude_filter(self.dataset, self.amplitude_filter_parameters) ==
                      self.amplitude_true_mask)

    def test_cleaning(self):
        self.dataset = MockDataset()
        assert np.all(utils.cleaning_filter(self.dataset, **self.cleaning_filter_parameters) == self.cleaning_true_mask)

    def test_leakage(self):
        self.dataset = MockDataset()
        assert np.all(utils.leakage_filter(self.dataset, **self.leakage_parameters) == self.leakage_true_mask)

    def test_energy(self):
        self.dataset = MockDataset()
        assert np.all(utils.energyband_filter(self.dataset, **self.energy_parameters) == self.energy_true_mask)

    def test_telescope_id(self):
        self.dataset = MockDataset()
        assert np.all(utils.telescope_id_filter(self.dataset, **self.telescope_id_parameters) == self.tel_true_mask)
        assert np.all(self.dataset.image_indices == self.tel_true_image_indices)

    def test_telescope_id_list(self):
        self.dataset = MockDataset()
        assert np.all(utils.telescope_id_filter(self.dataset, **self.telescope_id_list_parameters) ==
                      self.tel_list_true_mask)

    def test_telescope_id_list_strict(self):
        self.dataset = MockDataset()
        assert np.all(utils.telescope_id_filter(self.dataset, **self.telescope_id_list_strict_parameters) ==
                      self.tel_list_strict_true_mask)
        assert np.all(self.dataset.image_indices == self.tel_list_strict_true_image_indices)

    def test_emission_cone(self):
        self.dataset = MockDataset()
        assert np.all(utils.emission_cone_filter(self.dataset, **self.emission_cone_parameters) ==
                      self.emission_cone_true_mask)

    def test_impact_distance(self):
        self.dataset = MockDataset()
        assert np.all(utils.impact_distance_filter(self.dataset, **self.impact_distance_parameters) ==
                      self.impact_distance_true_mask)
        assert np.all(self.dataset.image_indices == self.impact_distance_true_indices)

    def test_multiplicity(self):
        self.dataset = MockDataset()
        assert np.all(utils.telescope_multiplicity_filter(self.dataset, **self.multiplicity_parameters) ==
                      self.multiplicity_true_mask)

    def test_multiplicity_strict(self):
        self.dataset = MockDataset()
        assert np.all(utils.telescope_multiplicity_filter(self.dataset, **self.multiplicity_strict_parameters) ==
                      self.multiplicity_strict_true_mask)
        assert np.all(self.dataset.trig_energies == self.multiplicity_strict_true_trig_energies)
        assert np.all(self.dataset.trig_image_indices == self.multiplicity_strict_true_trig_image_indices)


if __name__ == '__main__':
    unittest.main()
