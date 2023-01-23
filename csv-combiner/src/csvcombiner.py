#!/usr/bin/env python3

import argparse
import csv
import os.path as path
import sys
import pandas

FILE_DIR = path.abspath(path.dirname(__file__))
PROJECT_DIR = path.dirname(FILE_DIR)


def write_csv(dataframe: pandas.DataFrame, output):
    """ Writes dataframe to output """
    dataframe.to_csv(output, index=False, doublequote=False, escapechar='\\', quoting=csv.QUOTE_ALL,
                     lineterminator='\n')


def read_csv(filepath: str):
    """ Reads dataframe from filepath """
    return pandas.read_csv(path.join(PROJECT_DIR, filepath), doublequote=False, escapechar='\\', quoting=csv.QUOTE_ALL)


def combine_csv(filepaths: list):
    """ Combines csv file and returns resulting dataframe """

    dataframes = []

    for filepath in filepaths:
        dataframe = read_csv(filepath)
        filename = path.basename(path.normpath(filepath))

        # add additional column to specify filename
        dataframe['filename'] = filename

        dataframes.append(dataframe)

    combined_dataframe = pandas.concat(dataframes)
    return combined_dataframe


def main():
    """ Script to stack csv files with similar headers """
    parser = argparse.ArgumentParser()
    parser.add_argument('filepaths', metavar='N', type=str, nargs='+', help='a csv file to combine')

    args = parser.parse_args()

    combined_dataframe = combine_csv(args.filepaths)
    write_csv(combined_dataframe, sys.stdout)


if __name__ == '__main__':
    main()
