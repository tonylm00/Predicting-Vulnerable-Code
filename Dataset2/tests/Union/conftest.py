import csv
import os
import tempfile
import pytest

from Dataset2.Union.DatasetCombiner import DatasetCombiner


@pytest.fixture
def base_fixture():
    combiner = DatasetCombiner("output.csv")

    with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='\n', encoding="utf-8") as temp_valid_1, \
            tempfile.NamedTemporaryFile(delete=False, mode='w', newline='\n', encoding="utf-8") as temp_valid_2, \
            tempfile.NamedTemporaryFile(delete=False, mode='w', newline='\n', encoding="utf-8") as temp_invalid, \
            tempfile.NamedTemporaryFile(delete=False, mode='w', newline='\n', encoding="utf-8") as temp_no_name:

        csv.writer(temp_valid_1).writerows([["NameClass", "value1"], ["main.java", 30], ["runner.java", 14]])
        csv.writer(temp_valid_2).writerows([["Name", "value2"], ["main.java", 43], ["exe.java", 300]])
        csv.writer(temp_invalid).writerow(["Not; a CSV; file; \x80content"])
        csv.writer(temp_no_name).writerows([["OtherColumn", "Value1"], ["X", 500], ["Y", 600]])

        valid_csv_1 = temp_valid_1.name
        valid_csv_2 = temp_valid_2.name
        invalid_csv = temp_invalid.name
        no_name_csv = temp_no_name.name

    yield combiner, valid_csv_1, valid_csv_2, invalid_csv, no_name_csv

    os.remove(valid_csv_1)
    os.remove(valid_csv_2)
    os.remove(invalid_csv)
    os.remove(no_name_csv)
