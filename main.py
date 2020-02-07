import os
import sys
import argparse
import logging

from lib import *


__author__ = "Im yeonjae"
__date__ = "20200207"
__description__ = "Practice for coding test"


def get_cmd_args():
    """
    Set the option
    """
    parser = argparse.ArgumentParser(
        description=__description__,
        epilog="Developed by {} on {}".format(
            __author__, __date__
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("-e", "--evidence",
                        dest="evidence_file",
                        help="Evidence file path")

    parser.add_argument("-c", "--csv",
                        dest="csv",
                        help="Extract to csv file",
                        action="store_true")

    parser.add_argument("-d", "--db",
                        dest="db",
                        help="Extract to db file",
                        action="store_true")

    parser.add_argument("-o",
                        dest="output",
                        help="Store output file in output path")

    parser.add_argument("-v", "--version",
                        dest="version",
                        help="Displays tool version information",
                        action="store_true")

    return parser.parse_args()


def main():
    args = get_cmd_args()
    kwargs = vars(args)

    # ext = extract.PytskUtil(args.evidence_file)
    # ext.extract_file(name='$MFT')
    parse = parse_mft.Parse('extract/$MFT_extracted')
    data = parse.parse()
    #
    # if args.output_path is None:
    #     output_path = '01.csv'
    # else:
    #     output_path = args.output_path
    # write_output = write.WriteOutput(data, output_path)
    #
    # if kwargs['csv']:
    #     write_output.write_output('csv')
    # if kwargs['db']:
    #     write_output.write_output('db')


if __name__ == "__main__":
    main()


