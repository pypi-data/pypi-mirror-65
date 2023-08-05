# pylint: disable=missing-docstring,redefined-outer-name,no-self-use,protected-access

import copy
import os
from collections import OrderedDict

import pytest

from dump2polarion.exceptions import Dump2PolarionException, NothingToDoException
from dump2polarion.exporters.requirements_exporter import RequirementExport
from tests import conf

REQ_DATA = [
    OrderedDict(
        (
            ("title", "req01"),
            ("approver-ids", "sbulage:approved"),
            ("assignee", "mkourim"),
            ("category-ids", "CAT-01"),
            ("dueDate", "2018-05-30"),
            ("plannedIn", "PROJ-01"),
            ("initialEstimate", "1/4h"),
            ("priority", "medium"),
            ("severity", "nice_to_have"),
            ("status", "STAT-01"),
            ("reqtype", "functional"),
        )
    ),
    OrderedDict(
        (
            ("title", "req02"),
            ("description", "requirement description"),
            ("assignee-id", "mkourim"),
            ("initial-estimate", "1/4h"),
        )
    ),
    OrderedDict((("id", "PROJ-01"), ("title", "req03"), ("initial-estimate", None))),
    OrderedDict((("id", "PROJ-02"),)),
]


@pytest.fixture(scope="module")
def config_cloudtp(config_prop):
    cloudtp = copy.deepcopy(config_prop)
    cloudtp["polarion-project-id"] = "CLOUDTP"
    cloudtp["requirements-document-relative-path"] = "testing/requirements"
    cloudtp["requirements_import_properties"] = {"prop1": "val1", "prop2": "val2"}
    return cloudtp


class TestRequirement:
    def test_export(self, config_cloudtp):
        req_exp = RequirementExport(REQ_DATA, config_cloudtp)
        complete = req_exp.export()
        fname = "requirement_complete.xml"
        with open(os.path.join(conf.DATA_PATH, fname), encoding="utf-8") as input_xml:
            parsed = input_xml.read()
        assert complete == parsed

    def test_invalid_lookup(self, config_cloudtp):
        new_config = copy.deepcopy(config_cloudtp)
        new_config["requirements_import_properties"] = {"lookup-method": "inv"}
        req_exp = RequirementExport(REQ_DATA, new_config)
        with pytest.raises(Dump2PolarionException) as excinfo:
            req_exp.export()
        assert "Invalid value 'inv' for the 'lookup-method' property" in str(excinfo.value)

    def test_no_requirements(self, config_cloudtp):
        req_exp = RequirementExport([], config_cloudtp)
        with pytest.raises(NothingToDoException) as excinfo:
            req_exp.export()
        assert "Nothing to export" in str(excinfo.value)
