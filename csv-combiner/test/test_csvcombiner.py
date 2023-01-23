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
    "category": ["Shirts", "Blouses", "\"Gingham\" Shorts"
                 ]
}

test_data_dict3 = {
    "email_hash": ["a", "b", "c", "d", "e", "f"],
    "category": ["Shirts", "Blouses", "\"Gingham\" Shorts",
                 "Shirts", "Blouses", "\"Gingham\" Shorts"],
    "filename": ["l.csv", "l.csv", "l.csv", "r.csv", "r.csv", "r.csv"],
}


class TestCvsCombiner(unittest.TestCase):

    @patch('src.csvcombiner.read_csv')
    def test_combine_csv_two_files(self, read_csv):
        dataframe1 = pandas.DataFrame(test_data_dict1)
        dataframe2 = pandas.DataFrame(test_data_dict2)

        expected_dataframe = pandas.DataFrame(test_data_dict3)

        read_csv.side_effect = [dataframe1, dataframe2]
        actual_dataframe = combine_csv(["l.csv", "r.csv"])

        self.assertEqual(expected_dataframe.to_string(index=False), actual_dataframe.to_string(index=False))
