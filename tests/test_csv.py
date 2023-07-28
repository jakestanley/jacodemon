import unittest

from lib.py.csv import *

class TestCsv(unittest.TestCase):

    def test_valid_csv(self):
        self.assertTrue(csv_is_valid("tests/data/valid_csv.csv"))

    def test_valid_minimal_csv_file_is_valid(self):
        self.assertTrue(csv_is_valid("tests/data/valid_minimal_csv.csv"))

    # TODO: later we may wish to add this functionality so that we can 
    #   reuse files from other mods
    # def test_valid_csv_missing_files_is_valid(self):
    #     self.assertFalse(csv_is_valid("tests/data/valid_csv_missing_files.csv"))

    def test_invalid_csv_is_invalid(self):
        self.assertFalse(csv_is_valid("tests/data/invalid_csv.csv"))

    def test_duplicate_mods_is_invalid(self):
        self.assertFalse(csv_is_valid("tests/data/duplicate_mods.csv"))

    def test_minimal_csv_duplicate_mods_is_invalid(self):
        self.assertFalse(csv_is_valid("tests/data/minimal_csv_duplicate_mods.csv"))

    def test_minimal_csv_missing_files_is_invalid(self):
        self.assertFalse(csv_is_valid("tests/data/minimal_csv_missing_files.csv"))
