from src.csvcombiner import combine_csv
from unittest.mock import patch

import unittest
import pandas

test_data_dict1 = {
    "email_hash": ["a", "b", "c"],
    "category": ["Shirts", "Blouses", "\"Gingham\" Shorts"]
}

test_data_dict2 = {
    "email_hash": ["d", "e", "f"],
    "category": ["Purple", "Unicorns", "First"
                 ]
}

expected_data_dict_two_files = {
    "email_hash": ["a", "b", "c", "d", "e", "f"],
    "category": ["Shirts", "Blouses", "\"Gingham\" Shorts",
                 "Purple", "Unicorns", "First"],
    "filename": ["l.csv", "l.csv", "l.csv", "r.csv", "r.csv", "r.csv"],
}

expected_data_dict_multiple_files = {
    "email_hash": ["a", "b", "c", "d", "e", "f", "a", "b", "c"],
    "category": ["Shirts", "Blouses", "\"Gingham\" Shorts",
                 "Purple", "Unicorns", "First",
                 "Shirts", "Blouses", "\"Gingham\" Shorts"],
    "filename": ["l.csv", "l.csv", "l.csv", "r.csv", "r.csv", "r.csv", "m.csv", "m.csv", "m.csv"],
}



class TestCvsCombiner(unittest.TestCase):

    @patch('src.csvcombiner.read_csv')
    def test_combine_csv_two_files(self, read_csv):
        dataframe1 = pandas.DataFrame(test_data_dict1)
        dataframe2 = pandas.DataFrame(test_data_dict2)

        expected_dataframe = pandas.DataFrame(expected_data_dict_two_files)

        read_csv.side_effect = [dataframe1, dataframe2]
        actual_dataframe = combine_csv(["l.csv", "r.csv"])

        self.assertEqual(expected_dataframe.to_string(index=False), actual_dataframe.to_string(index=False))

    @patch('src.csvcombiner.read_csv')
    def test_combine_csv_multiple_files(self, read_csv):
        dataframe1 = pandas.DataFrame(test_data_dict1)
        dataframe2 = pandas.DataFrame(test_data_dict2)
        dataframe3 = pandas.DataFrame(test_data_dict1)

        expected_dataframe = pandas.DataFrame(expected_data_dict_multiple_files)

        read_csv.side_effect = [dataframe1, dataframe2, dataframe3]
        actual_dataframe = combine_csv(["l.csv", "r.csv", "m.csv"])

        self.assertEqual(expected_dataframe.to_string(index=False), actual_dataframe.to_string(index=False))
