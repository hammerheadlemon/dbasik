from datetime import date

from django.test import TestCase

from datamap.models import DatamapLine
from excelparser.helpers.parser import ParsedSpreadsheet, CellData, CellValueType
from factories.datamap_factories import DatamapFactory
from factories.datamap_factories import ProjectFactory
from register.models import FinancialQuarter
from returns.models import Return
from exceptions.exceptions import DatamapLineValidationError


class TestWorksheetFromDatamap(TestCase):
    def setUp(self):
        self.financial_quarter = FinancialQuarter.objects.create(quarter=4, year=2018)
        self.project = ProjectFactory()
        self.datamap = DatamapFactory()
        self.return_obj = Return.objects.create(
            project=self.project, financial_quarter=self.financial_quarter
        )
        DatamapLine.objects.create(
            datamap=self.datamap,
            key="Bad mobile number",
            data_type="Phone",
            sheet="Sheet1",
            cell_ref="B1",
        )
        DatamapLine.objects.create(
            datamap=self.datamap,
            key="Key 2",
            data_type="Integer",
            sheet="Sheet1",
            cell_ref="B2",
        )
        self.populated_template = "/home/lemon/code/python/dbasik-dev/dbasik-dftgovernance/excelparser/tests/bad_phone_number.xlsm"
        self.parsed_spreadsheet = ParsedSpreadsheet(
            template_path=self.populated_template,
            project=self.project,
            return_obj=self.return_obj,
            datamap=self.datamap,
            use_datamap_types=True,
        )

    def test_worksheetfromdatamap_obj(self):
        breakpoint()
        """
        prior to process(), this object's _sheet_data is empty
        order - process(), _process_sheets() -> creates
        self._sheet_data[SHEETNAME] (a WorksSheetFromDatamap object)
        the WorksSheetFromDatamap object has _data() attribute
        which is populated by WorksSheetFromDatamap._convert()
        _convert() goes through each line in Datamap:

            if use_datamap_types:
            creates a CellData(key, sheet, parsed_value, cellref CellValueType)
            whose CellValueType is from the Datamap, otherwise it is inferred
            by the system.

        Once _process_sheets() is complete (a parsed sheet for each
        in the source spreadsheet), each item in ParsedSpreadsheet._sheet_data
        (a dict of str: WorksSheetFromDatamap) is then processed by
        _process_sheet_to_return() to ensure the data is fit for the database.

        Here is where currently the validation happens. The objective is to:
            assign the value from the sheet to the correct db field:
                * value_str
                * value_int
                * value_float
                * value_date
                * value_datetime
                * value_phone
        During this process, each cellref: value dict is processed by
        ParsedSpreadsheet._type_fix_or_raise_exception(), which does

            if use datamap_types:
                checks depending on the expected_type (value_phone, etc)
                if value does not meet the condition, it is either
                fixed in place, or if cannot have obvious fix, an
                exception is raised (which is caught be calling func
                (_process_sheet_to_return()).
                The fixed value is returned or the exception
            else
                the value in the cell is returned an no action is taken.
        This dict is then packed up with other possible values for the database
        such as value_str, value_in, etc - which are made None if not used
        and then a ReturnItem object is created from these and saved to the
        database.

        It's a bit of a mess! But crucial to the application so needs to be sorted.
        """
        self.parsed_spreadsheet.process()
        # after process(), _sheet_data is populated
        data = self.parsed_spreadsheet._sheet_data["Sheet1"]._data
        self.assertEqual(data["Key 2"].sheet, "Sheet1")
        self.assertEqual(data["Key 2"].key, "Key 2")
        self.assertEqual(data["Key 2"].value, 2)
        self.assertEqual(data["Key 2"].type, CellValueType.INTEGER)

        self.assertEqual(data["Bad mobile number"].sheet, "Sheet1")
        self.assertEqual(data["Bad mobile number"].key, "Bad mobile number")
        # TODO data var is created before this phone integer is getting
        # turned into a string, therefore this test is failing
        self.assertEqual(data["Bad mobile number"].value, "7678877654")
        self.assertEqual(data["Bad mobile number"].type, CellValueType.PHONE)


class TestSpecificErrors(TestCase):
    def setUp(self):
        """
        If looking to test specific error types, add a corresponding
        cell in the datamap; create a test spreadsheet containing the
        error and point to it from here.
        """
        self.financial_quarter = FinancialQuarter.objects.create(quarter=4, year=2018)
        self.project = ProjectFactory()
        self.datamap = DatamapFactory()
        self.return_obj = Return.objects.create(
            project=self.project, financial_quarter=self.financial_quarter
        )
        DatamapLine.objects.create(
            datamap=self.datamap,
            key="Bad Phone Number",
            data_type="Phone",
            sheet="Sheet1",
            cell_ref="B1",
        )
        self.populated_template = "/home/lemon/code/python/dbasik-dev/dbasik-dftgovernance/excelparser/tests/bad_phone_number.xlsm"
        self.parsed_spreadsheet = ParsedSpreadsheet(
            template_path=self.populated_template,
            project=self.project,
            return_obj=self.return_obj,
            datamap=self.datamap,
            use_datamap_types=True,
        )

    def test_return_parser_flags_bad_number(self):
        with self.assertRaises(DatamapLineValidationError):
            self.parsed_spreadsheet.process()


class TestParseToReturn(TestCase):
    def setUp(self):
        self.financial_quarter = FinancialQuarter.objects.create(quarter=4, year=2018)
        self.project = ProjectFactory()
        self.datamap = DatamapFactory()
        self.return_obj = Return.objects.create(
            project=self.project, financial_quarter=self.financial_quarter
        )
        DatamapLine.objects.create(
            datamap=self.datamap,
            key="Project Name",
            sheet="Test Sheet 1",
            cell_ref="B1",
        )
        DatamapLine.objects.create(
            datamap=self.datamap, key="Total Cost", sheet="Test Sheet 1", cell_ref="B2"
        )
        DatamapLine.objects.create(
            datamap=self.datamap, key="SRO", sheet="Test Sheet 1", cell_ref="B3"
        )
        DatamapLine.objects.create(
            datamap=self.datamap,
            key="SRO Retirement Date",
            sheet="Test Sheet 1",
            cell_ref="B4",
        )
        DatamapLine.objects.create(
            datamap=self.datamap,
            key="Missing Data",
            sheet="Test Sheet 1",
            cell_ref="B5",
        )
        DatamapLine.objects.create(
            datamap=self.datamap,
            key="Janitor's Favourite Colour",
            sheet="Test Sheet 2",
            cell_ref="B1",
        )

        self.populated_template = "/home/lemon/code/python/dbasik-dev/dbasik-dftgovernance/excelparser/tests/populated.xlsm"
        self.parsed_spreadsheet = ParsedSpreadsheet(
            template_path=self.populated_template,
            project=self.project,
            return_obj=self.return_obj,
            datamap=self.datamap,
        )

    def test_return_parser(self):
        self.parsed_spreadsheet.process()
        return_item = Return.objects.get(
            id=self.return_obj.id
        ).return_returnitems.first()
        self.assertEqual(return_item.datamapline.key, "Project Name")
        self.assertEqual(return_item.value_str, "Testable Project")

    def test_celldata_mapper(self):
        self.parsed_spreadsheet.process()
        cell_data_int = CellData("Key", "Sheet", 1, "B1", CellValueType.INTEGER)
        cell_data_float = CellData("Key", "Sheet", 1, "B1", CellValueType.FLOAT)
        cell_data_date = CellData(
            "Key", "Sheet", date(2018, 1, 1), "B1", CellValueType.DATE
        )
        self.assertEqual(
            self.parsed_spreadsheet._map_to_keyword_param(cell_data_int), "value_int"
        )
        self.assertEqual(
            self.parsed_spreadsheet._map_to_keyword_param(cell_data_float),
            "value_float",
        )
        self.assertEqual(
            self.parsed_spreadsheet._map_to_keyword_param(cell_data_date), "value_date"
        )

    def test_parse_to_return_object(self):
        self.parsed_spreadsheet.process()

        dml_project_name = (
            DatamapLine.objects.filter(datamap=self.datamap)
            .filter(key="Project Name")
            .first()
        )
        dml_sro_retirement = (
            DatamapLine.objects.filter(datamap=self.datamap)
            .filter(key="SRO Retirement Date")
            .first()
        )
        dml_sro = (
            DatamapLine.objects.filter(datamap=self.datamap).filter(key="SRO").first()
        )

        dml_missing_data = (
            DatamapLine.objects.filter(datamap=self.datamap)
            .filter(key="Missing Data")
            .first()
        )

        return_item_projectname = (
            Return.objects.get(id=self.return_obj.id)
            .return_returnitems.filter(datamapline=dml_project_name)
            .first()
        )
        return_item_srocell = (
            Return.objects.get(id=self.return_obj.id)
            .return_returnitems.filter(datamapline=dml_sro_retirement)
            .first()
        )
        return_item_sro = (
            Return.objects.get(id=self.return_obj.id)
            .return_returnitems.filter(datamapline=dml_sro)
            .first()
        )
        return_item_missing_data = (
            Return.objects.get(id=self.return_obj.id)
            .return_returnitems.filter(datamapline=dml_missing_data)
            .first()
        )

        self.assertEqual(return_item_projectname.datamapline.key, "Project Name")
        self.assertEqual(return_item_projectname.value_str, "Testable Project")

        self.assertEqual(return_item_srocell.datamapline.key, "SRO Retirement Date")
        self.assertEqual(return_item_srocell.value_date, date(2022, 2, 23))

        self.assertEqual(return_item_sro.datamapline.key, "SRO")
        self.assertEqual(return_item_sro.value_str, "John Milton")
        self.assertEqual(return_item_sro.value_int, None)
        self.assertEqual(return_item_sro.value_date, None)

        self.assertEqual(return_item_missing_data.datamapline.key, "Missing Data")
        self.assertIsNone(return_item_missing_data.value_date)
        self.assertIsNone(return_item_missing_data.value_str)
        self.assertIsNone(return_item_missing_data.value_float)
