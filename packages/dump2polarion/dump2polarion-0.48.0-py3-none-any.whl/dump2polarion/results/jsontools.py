"""Helper functions for handling JSON data."""

import json

from dump2polarion.exceptions import Dump2PolarionException
from dump2polarion.exporters import xunit_exporter


def _load_json(json_filename):
    with open(json_filename, encoding="utf-8") as input_json:
        return json.load(input_json)


def import_pytest_collect(json_filename):
    """Read the content of the JSON file produced by pytest-polarion-collect file."""
    try:
        results = _load_json(json_filename)["results"]
    except Exception as err:
        raise Dump2PolarionException("Cannot load results from {}: {}".format(json_filename, err))

    return xunit_exporter.ImportedData(results=results, testrun=None)


# pylint: disable=unused-argument
def import_json(json_filename, **kwargs):
    """Read the content of the JSON file."""
    # results from pytest-polarion-collect are the only ones supported so far
    return import_pytest_collect(json_filename)
