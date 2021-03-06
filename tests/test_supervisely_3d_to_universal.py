import shutil
from pathlib import Path

from universal_devkit.scripts.supervisely_3d_to_universal import (
    convert_supervisely_3d_to_universal,
)
from universal_devkit.utils import read_json


def get_relative_path(relative_file_path):
    return Path(__file__).parent / relative_file_path


def equal_dicts(d1: dict, d2: dict, ignore_keys: list):
    """Check two dictionaries for equality with the ability to ignore
    specific keys.

    Source: https://stackoverflow.com/a/10480904/6942666

    Args:
        d1 (dict): the first dictionary
        d2 (dict): the second dictionary
        ignore_keys (list): a list of strings with keys to ignore

    Returns:
        bool: whether the dicts are equal
    """
    d1_filtered = {k: v for k, v in d1.items() if k not in ignore_keys}
    d2_filtered = {k: v for k, v in d2.items() if k not in ignore_keys}
    return d1_filtered == d2_filtered


def test_supervisely_3d_to_universal_single_file():
    # The path to the folder with a single file
    supervisely_annotations_path = get_relative_path(
        "assets/supervisely_annotations/single_file_input"
    )

    # The correct output for the single file
    correct_output_path = get_relative_path(
        "assets/supervisely_annotations/single_file_correct.json"
    )

    # The path to use as the output directory
    output_file_dir = get_relative_path(
        "assets/supervisely_annotations/single_file_output"
    )
    output_file_path = get_relative_path(
        "assets/supervisely_annotations/single_file_output/input.json"
    )

    # Convert the annotations
    convert_supervisely_3d_to_universal(supervisely_annotations_path, output_file_dir)

    # Make sure the output is correct
    correct_data = read_json(correct_output_path)
    output_annotations = read_json(output_file_path)

    ignore_keys = ["token", "sample_token", "instance_token"]

    assert len(correct_data) == len(output_annotations)

    for i in range(len(output_annotations)):
        output_d = output_annotations[i]
        correct_d = correct_data[i]
        assert equal_dicts(output_d, correct_d, ignore_keys=ignore_keys)

    shutil.rmtree(output_file_dir)
