from src.csvcombiner import run_csvcombiner_script

import unittest
import os.path as path
import random
import string
import pandas
import csv
import os
import shutil

DIR = path.abspath(path.dirname(__file__))
RESOURCES_DIR = path.join(DIR, 'resources')
RESULTS_FILE = path.join(RESOURCES_DIR, "output.csv")

NUM_FILES = 10
NUM_HEADERS = 10
NUM_ROWS = 10000


class TestCvsCombinerIntegration(unittest.TestCase):

    @staticmethod
    def generate_random_word(n: int):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(n))

    @staticmethod
    def write_file(dataframe: pandas.DataFrame, output):
        dataframe.to_csv(output, index=False, doublequote=False, escapechar='\\', quoting=csv.QUOTE_ALL,
                         lineterminator='\n')

    @staticmethod
    def read_file(filepath: str):
        return pandas.read_csv(filepath, doublequote=False, escapechar='\\', quoting=csv.QUOTE_ALL)

    @staticmethod
    def generate_dataframe(headers: list):
        dataframe_dict = {}
        for header in headers:
            dataframe_dict[header] = []

            for _ in range(NUM_ROWS):
                dataframe_dict[header].append(TestCvsCombinerIntegration.generate_random_word(10))

        return pandas.DataFrame(dataframe_dict)

    def setUp(self):
        self.filenames = [TestCvsCombinerIntegration.generate_random_word(10) + ".csv"for _ in range(NUM_FILES)]
        self.headers = [TestCvsCombinerIntegration.generate_random_word(10) for _ in range(NUM_HEADERS)]
        self.dataframes = [TestCvsCombinerIntegration.generate_dataframe(self.headers) for _ in range(NUM_FILES)]

        os.makedirs(RESOURCES_DIR, exist_ok=True)

        for filename, dataframe in zip(self.filenames, self.dataframes):
            TestCvsCombinerIntegration.write_file(dataframe, path.join(RESOURCES_DIR, filename))

    def tearDown(self):
        shutil.rmtree(RESOURCES_DIR)

    def rowExists(self, dataframe: pandas.DataFrame, row: pandas.DataFrame):
        return (dataframe == row).all(1).any()

    def test_csvcombiner(self):
        filepaths = [path.join(RESOURCES_DIR, filename) for filename in self.filenames]
        run_csvcombiner_script(filepaths, RESULTS_FILE)

        output_dataframe = TestCvsCombinerIntegration.read_file(RESULTS_FILE)

        self.assertEqual(self.headers + ["filename"], list(output_dataframe.columns))
        self.assertEqual(NUM_FILES * NUM_ROWS, len(output_dataframe))

        for filename, dataframe in zip(self.filenames, self.dataframes):
            dataframe["filename"] = filename
            for i in range(10):
                self.assertTrue(self.rowExists(output_dataframe, dataframe.iloc[random.randint(0, NUM_ROWS - 1)]))
