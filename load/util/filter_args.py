from typing import Any
import argparse


def filter_args(
    parsed_args: argparse.Namespace,
    include_values: list = None,
    exclude_values: list = None,
    include_keys: list = None,
    exclude_keys: list = None,
) -> dict[Any, Any]:
    """
    Function to filter out command line arguments that are None
    Pass in the unpacked result of this function to the appropriate call
    to use that callable's default values, rather than the ones from argparse

    @param parsed_args: The parsed command line arguments (i.e., parser.parse_args())
    @param include_values: Values by which to include items from the parsed args
    @param exclude_values: Values by which to exclude items from the parsed args
    @param include_keys: Keys by which to include items from the parsed args
    @param exclude_keys: Keys by which to exclude items from the parsed args
    @return: The same dictionary without any None-valued items
    """
    parsed_args_dict = parsed_args.__dict__
    if include_keys is None:
        include_keys = list(parsed_args_dict.keys())
    if exclude_keys is None:
        exclude_keys = []
    if include_values is None:
        include_values = list(parsed_args_dict.values())
    if exclude_values is None:
        exclude_values = [None, {}, []]

    return {
        key: value
        for key, value in parsed_args_dict.items()
        if key in include_keys
        and key not in exclude_keys
        and value in include_values
        and value not in exclude_values
    }
