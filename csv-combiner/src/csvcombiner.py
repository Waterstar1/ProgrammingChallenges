#!/usr/bin/env python3

import argparse
import csv
import os.path as path
import sys
import pandas

DIR = path.abspath(path.dirname(__file__) + "/../")


def combine_csv(filepaths: list):
    """ Combines csv files by header and outputs to stdout """

    dataframes = []

    for filepath in filepaths:
        dataframe = pandas.read_csv(filepath, doublequote=False, escapechar='\\', quoting=csv.QUOTE_ALL)
        filename = path.basename(path.normpath(filepath))

        # add additional column to specify filename
        dataframe['filename'] = filename

        dataframes.append(dataframe)

    combined_dataframes = pandas.concat(dataframes)
    combined_dataframes.to_csv(sys.stdout, index=False, doublequote=False, escapechar='\\', quoting=csv.QUOTE_ALL, lineterminator='\n')


def main():
    """ Script to stack csv files with similar headers """

    parser = argparse.ArgumentParser()
    parser.add_argument('filepaths', metavar='N', type=str, nargs='+', help='a csv file to combine')

    args = parser.parse_args()
    combine_csv(args.filepaths)


if __name__ == '__main__':
    main()
