# pylint: disable=missing-docstring,redefined-outer-name,no-self-use,protected-access

import copy
import os

import pytest
from lxml import etree

from dump2polarion.exceptions import Dump2PolarionException, NothingToDoException
from dump2polarion.exporters.xunit_exporter import ImportedData, XunitExport
from dump2polarion.results.importer import import_results
from dump2polarion.utils import get_unicode_str
from tests import conf


@pytest.fixture(scope="module")
def records_ids():
    csv_file = os.path.join(conf.DATA_PATH, "workitems_ids.csv")
    return import_results(csv_file)


@pytest.fixture(scope="module")
def records_names():
    csv_file = os.path.join(conf.DATA_PATH, "workitems_ids.csv")
    records = import_results(csv_file)
    for res in records.results:
        res.pop("id")
    return records


def test_top_element(config_prop, records_ids):
    exporter = XunitExport("5_8_0_17", records_ids, config_prop, transform_func=lambda: None)
    top_element = exporter._top_element()
    parsed = "<testsuites><!--Generated for testrun 5_8_0_17--></testsuites>".strip()
    top_element_str = get_unicode_str(etree.tostring(top_element, encoding="utf-8").strip())
    assert top_element_str == parsed


class TestConfigPropMixin:
    @pytest.fixture(autouse=True)
    def base_config_prop(self, config_prop):
        self.config_prop = config_prop


class TestProperties(TestConfigPropMixin):
    def test_properties_element(self, records_ids):
        exporter = XunitExport(
            "5_8_0_17", records_ids, self.config_prop, transform_func=lambda: None
        )
        top_element = exporter._top_element()
        properties_element = exporter._properties_element(top_element)
        parsed = (
            "<properties>"
            '<property name="polarion-testrun-id" value="5_8_0_17"/>'
            '<property name="polarion-project-id" value="RHCF3"/>'
            '<property name="polarion-dry-run" value="False"/>'
            '<property name="polarion-response-test" value="test"/>'
            '<property name="polarion-testrun-status-id" value="inprogress"/>'
            "</properties>".strip()
        )
        properties_str = get_unicode_str(
            etree.tostring(properties_element, encoding="utf-8").strip()
        )
        assert properties_str == parsed

    def test_properties_lookup_config(self, records_names):
        new_config = copy.deepcopy(self.config_prop)
        new_config["xunit_import_properties"]["polarion-lookup-method"] = "id"
        exporter = XunitExport("5_8_0_17", records_names, new_config, transform_func=lambda: None)
        top_element = exporter._top_element()
        properties_element = exporter._properties_element(top_element)
        exporter._fill_lookup_prop(properties_element)
        properties_str = get_unicode_str(
            etree.tostring(properties_element, encoding="utf-8").strip()
        )
        assert '<property name="polarion-lookup-method" value="id"/>' in properties_str

    def test_properties_invalid_lookup(self, records_ids):
        new_config = copy.deepcopy(self.config_prop)
        new_config["xunit_import_properties"]["polarion-lookup-method"] = "invalid"
        exporter = XunitExport("5_8_0_17", records_ids, new_config)
        with pytest.raises(Dump2PolarionException) as excinfo:
            exporter.export()
        assert "Invalid value 'invalid' for the 'polarion-lookup-method'" in str(excinfo.value)


class TestE2E(TestConfigPropMixin):
    def test_e2e_noresults(self, records_ids):
        exporter = XunitExport(
            "5_8_0_17", records_ids, self.config_prop, transform_func=lambda arg: None
        )
        with pytest.raises(NothingToDoException) as excinfo:
            exporter.export()
        assert "Nothing to export" in str(excinfo.value)

    def test_e2e_missing_results(self):
        new_records = ImportedData(results=[], testrun=None)
        exporter = XunitExport(
            "5_8_0_17", new_records, self.config_prop, transform_func=lambda arg: arg
        )
        with pytest.raises(NothingToDoException) as excinfo:
            exporter._fill_tests_results(None)
        assert "Nothing to export" in str(excinfo.value)

    def test_e2e_all_ignored(self, captured_log):
        new_records = ImportedData(
            results=[{"title": "foo", "id": "foo", "verdict": "waiting", "ignored": True}],
            testrun=None,
        )
        exporter = XunitExport(
            "5_8_0_17", new_records, self.config_prop, transform_func=lambda arg: arg
        )
        with pytest.raises(NothingToDoException) as excinfo:
            exporter.export()
        assert "Nothing to export" in str(excinfo.value)
        assert "Skipping ignored testcase" in captured_log.getvalue()

    def test_e2e_ids_notransform(self, records_ids):
        exporter = XunitExport(
            "5_8_0_17", records_ids, self.config_prop, transform_func=lambda arg: arg
        )
        complete = exporter.export()
        fname = "complete_notransform.xml"
        with open(os.path.join(conf.DATA_PATH, fname), encoding="utf-8") as input_xml:
            parsed = input_xml.read()
        assert complete == parsed

    def test_e2e_ids_transform(self, records_ids):
        exporter = XunitExport("5_8_0_17", records_ids, self.config_prop)
        complete = exporter.export()
        fname = "complete_transform.xml"
        with open(os.path.join(conf.DATA_PATH, fname), encoding="utf-8") as input_xml:
            parsed = input_xml.read()
        assert complete == parsed

    def test_e2e_names_notransform(self, records_names):
        exporter = XunitExport(
            "5_8_0_17", records_names, self.config_prop, transform_func=lambda arg: arg
        )
        complete = exporter.export()
        fname = "complete_notransform_name.xml"
        with open(os.path.join(conf.DATA_PATH, fname), encoding="utf-8") as input_xml:
            parsed = input_xml.read()
        assert complete == parsed

    def test_e2e_names_transform(self, records_names):
        exporter = XunitExport("5_8_0_17", records_names, self.config_prop)
        complete = exporter.export()
        fname = "complete_transform_name.xml"
        with open(os.path.join(conf.DATA_PATH, fname), encoding="utf-8") as input_xml:
            parsed = input_xml.read()
        assert complete == parsed
