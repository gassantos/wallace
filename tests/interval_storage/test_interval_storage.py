from unittest import TestCase

from wallace.interval_storage import IntervalStorage
from wallace.settings import AbstractSettings

class IntervalStorageTest(TestCase):
    def test_interval_storage_with_a_single_interval(self):
        interval_storage = IntervalStorage()
        self.assertFalse(interval_storage.has_intersection(0.0, 1.0))
        interval_storage.add_interval("1", 0.0, 1.0)

        self.assertEqual("1", interval_storage.get_entry(0.5))

        with self.assertRaises(ValueError):
            interval_storage.get_entry(1.5)

    def test_interval_storage_for_invalid_intervals(self):
        interval_storage = IntervalStorage()
        with self.assertRaises(ValueError):
            interval_storage.add_interval("1", 0.0, 1.2)

        with self.assertRaises(ValueError):
            interval_storage.add_interval("1", -3.2, 0.8)

        with self.assertRaises(ValueError):
            interval_storage.add_interval("1", -3.2, 1.4)

    def test_interval_storage_for_completely_containing_intervals(self):
        interval_storage = IntervalStorage()
        interval_storage.add_interval("1", 0.5, 0.7)

        with self.assertRaises(ValueError):
            interval_storage.add_interval("2", 0.55, 0.65)

        with self.assertRaises(ValueError):
            interval_storage.add_interval("3", 0.45, 0.75)

    def test_interval_storage_for_has_entry(self):
        interval_storage = IntervalStorage()
        self.assertFalse(interval_storage.has_entry(0.5))
        self.assertFalse(interval_storage.has_entry(1.5))

        interval_storage.add_interval("1", 0.3, 0.7)
        self.assertTrue(interval_storage.has_entry(0.5))
        self.assertFalse(interval_storage.has_entry(0.8))
        self.assertFalse(interval_storage.has_entry(0.2))
        self.assertFalse(interval_storage.has_entry(-0.2))


    def test_interval_storage_with_two_intervals_and_midpoint_get(self):
        interval_storage = IntervalStorage()
        interval_storage.add_interval("1", 0.0, 0.5)
        interval_storage.add_interval("2", 0.5, 1.0)

        self.assertEqual("1", interval_storage.get_entry(0.25))
        self.assertEqual("2", interval_storage.get_entry(0.5))
        self.assertEqual("2", interval_storage.get_entry(0.8))

    def test_interval_storage_with_three_intervals(self):
        interval_storage = IntervalStorage()
        interval_storage.add_interval("1", 0.0, 0.3)
        interval_storage.add_interval("2", 0.3, 0.6)
        interval_storage.add_interval("3", 0.6, 1.0)

        self.assertEqual("1", interval_storage.get_entry(0.0))
        self.assertEqual("1", interval_storage.get_entry(0.2))
        self.assertEqual("2", interval_storage.get_entry(0.3))
        self.assertEqual("2", interval_storage.get_entry(0.5))
        self.assertEqual("3", interval_storage.get_entry(0.6))
        self.assertEqual("3", interval_storage.get_entry(0.85))

        with self.assertRaises(ValueError):
            interval_storage.get_entry(1.0)

        with self.assertRaises(ValueError):
            interval_storage.get_entry(-0.01)

    def test_initializing_interval_storage_with_a_map(self):
        interval_storage = IntervalStorage({
            "1": (0.0, 0.3),
            "2": (0.3, 0.6),
            "3": (0.6, 1.0)
            })

        self.assertEqual("1", interval_storage.get_entry(0.0))
        self.assertEqual("1", interval_storage.get_entry(0.2))
        self.assertEqual("2", interval_storage.get_entry(0.3))
        self.assertEqual("2", interval_storage.get_entry(0.5))
        self.assertEqual("3", interval_storage.get_entry(0.6))
        self.assertEqual("3", interval_storage.get_entry(0.85))

    def test_initializing_interval_storage_with_a_map_with_invalid_intervals(self):
        with self.assertRaises(ValueError):
            interval_storage = IntervalStorage({
                "1": (0.0, 0.5),
                "2": (0.4, 1.0)
                })

        with self.assertRaises(ValueError):
            interval_storage = IntervalStorage({
                "1": (-10.0, 20.5),
                "2": (0.4, 1.0)
                })

        with self.assertRaises(ValueError):
            interval_storage = IntervalStorage({
                "1": (0.0, 0.5),
                "2": (0.5, 1.2)
                })
