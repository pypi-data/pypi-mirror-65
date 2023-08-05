"""Import data using correct tools."""

import os

from dump2polarion.results import dbtools
from dump2polarion.exceptions import Dump2PolarionException


def _get_importer(input_file):
    """Select importer based on input file type."""
    __, ext = os.path.splitext(input_file)
    ext = ext.lower()

    if "ostriz" in input_file:
        from dump2polarion.results import ostriztools

        importer = ostriztools.import_ostriz
    elif ext == ".xml":
        # expect junit-report from pytest
        from dump2polarion.results import junittools

        importer = junittools.import_junit
    elif ext == ".csv":
        from dump2polarion.results import csvtools

        importer = csvtools.import_csv
    elif ext in dbtools.SQLITE_EXT:
        importer = dbtools.import_sqlite
    elif ext == ".json":
        from dump2polarion.results import jsontools

        importer = jsontools.import_json
    else:
        raise Dump2PolarionException("Cannot recognize type of input data, add file extension.")

    return importer


def import_results(input_file, **kwargs):
    """Import the input file."""
    return _get_importer(input_file)(input_file, **kwargs)
