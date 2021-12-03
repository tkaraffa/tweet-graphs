from util.base_api import APIBase
from google.cloud import bigquery


import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket")
    parser.add_argument("--table")
    return parser.parse_args()


def main():
    args = get_args()
    target_table = args.table
    target_bucket = args.bucket


if __name__ == "__main__":
    main()
