import os
import pytest
from Dataset2.Union.Union_TM_SM import Union


class TestUnionIntegration:

    def test_case_1(self, fixture_both_csv, base_fixture):
        _, _, union_dir_path = base_fixture

        Union.main()

        output_file = union_dir_path / "union_SM_TM.csv"
        assert output_file.exists()

        written_data = output_file.read_text()
        expected_output = (
            "NameClass,a1,a2,a3,a4,a5,a6,a7,a8,a9,m1,m2,m3,m4,m5,m6,m7,m8,class\n"
            "tony.java,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,10,11,pos,pos\n"
        )

        assert written_data.strip() == expected_output.strip()

    def test_case_2(self, base_fixture, fixture_only_sm):
        _, _, union_dir_path = base_fixture

        with pytest.raises(FileNotFoundError):
            Union.main()

        output_file = union_dir_path / "union_SM_TM.csv"
        assert output_file.exists()

        written_data = output_file.read_text()
        expected_output = ''

        assert written_data.strip() == expected_output.strip()

    def test_case_3(self, base_fixture, fixture_tm_not_valid_sm):
        _, _, union_dir_path = base_fixture

        Union.main()

        output_file = union_dir_path / "union_SM_TM.csv"
        assert output_file.exists()

        written_data = output_file.read_text()
        expected_output = "NameClass,a1,a2,a3,a4,a5,a6,a7,a8,a9,m1,m2,m3,m4,m5,m6,m7,m8,class"

        assert written_data.strip() == expected_output.strip()

    def test_case_4(self, fixture_both_csv_empty, base_fixture):
        _, _, union_dir_path = base_fixture

        os.chdir(union_dir_path)
        Union.main()

        output_file = union_dir_path / "union_SM_TM.csv"
        assert output_file.exists()

        written_data = output_file.read_text()
        expected_output = ''

        assert written_data.strip() == expected_output.strip()

    def test_case_5(self, base_fixture, fixture_only_tm):
        _, _, union_dir_path = base_fixture

        with pytest.raises(FileNotFoundError):
            Union.main()

        output_file = union_dir_path / "union_SM_TM.csv"
        assert output_file.exists()

        written_data = output_file.read_text()
        expected_output = ''

        assert written_data.strip() == expected_output.strip()

    def test_case_6(self, base_fixture, fixture_tm_sm_not_valid):
        _, _, union_dir_path = base_fixture

        Union.main()

        output_file = union_dir_path / "union_SM_TM.csv"
        assert output_file.exists()

        written_data = output_file.read_text()
        expected_output = "NameClass,a1,a2,a3,a4,a5,a6,a7,a8,a9,m1,m2,m3,m4,m5,m6,m7,m8,class"

        assert written_data.strip() == expected_output.strip()

    def test_case_7(self, base_fixture, fixture_both_csv_headers):
        _, _, union_dir_path = base_fixture

        Union.main()

        output_file = union_dir_path / "union_SM_TM.csv"
        assert output_file.exists()

        written_data = output_file.read_text()
        expected_output = 'NameClass,a1,a2,a3,a4,a5,a6,a7,a8,a9,m1,m2,m3,m4,m5,m6,m7,m8,class'

        assert written_data.strip() == expected_output.strip()

    def test_case_8(self, base_fixture):
        _, _, union_dir_path = base_fixture

        with pytest.raises(FileNotFoundError):
            Union.main()

        output_file = union_dir_path / "union_SM_TM.csv"
        assert output_file.exists()

        written_data = output_file.read_text()
        expected_output = ""

        assert written_data.strip() == expected_output.strip()

    def test_case_9(self, fixture_empty_tm, base_fixture):
        _, _, union_dir_path = base_fixture

        Union.main()

        output_file = union_dir_path / "union_SM_TM.csv"
        assert output_file.exists()

        written_data = output_file.read_text()
        assert written_data.strip() == ''

    def test_case_10(self, fixture_empty_sm, base_fixture):
        _, _, union_dir_path = base_fixture

        Union.main()

        output_file = union_dir_path / "union_SM_TM.csv"
        assert output_file.exists()

        written_data = output_file.read_text()
        assert written_data.strip() == 'NameClass,a1,a2,a3,a4,a5,a6,a7,a8,a9,class'
