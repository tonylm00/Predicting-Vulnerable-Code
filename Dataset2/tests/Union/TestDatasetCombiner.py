import os
from pathlib import Path
import pytest
import pandas as pd


class TestDatasetCombiner:
    def test_case_1(self, base_fixture):
        combiner, csv_valid_1, _, _, _ = base_fixture
        with pytest.raises(ValueError):
            combiner.merge(csv_valid_1)

    def test_case_2(self, base_fixture):
        combiner, csv_valid_1, _, csv_invalid_format, _ = base_fixture
        with pytest.raises(KeyError):
            combiner.merge(csv_valid_1, csv_invalid_format)

    def test_case_3(self, base_fixture):
        combiner, csv_valid_1, csv_valid_2, _, _ = base_fixture
        combiner.merge(csv_valid_1, csv_valid_2)

        result_df = pd.read_csv("output.csv")
        expected_df = pd.DataFrame({
            'Name': ['exe.java', 'main.java', 'runner.java'],
            'value1': [0.0, 30.0, 14.0],
            'value2': [300.0, 43.0, 0.0],
        })
        pd.testing.assert_frame_equal(result_df, expected_df)

        file_path = Path("output.csv")
        file_path.exists()
        os.remove(file_path)

    def test_case_4(self, base_fixture):
        combiner, csv_valid_1, _, _, csv_no_name = base_fixture
        with pytest.raises(KeyError):
            combiner.merge(csv_valid_1, csv_no_name)
