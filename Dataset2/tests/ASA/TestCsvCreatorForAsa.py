import pytest
from Dataset2.mining_results_asa.CsvCreatorForAsa import CsvCreatorForASA


class TestProcessVulnerabilities:

    def test_case_1(self):
        creator = CsvCreatorForASA("final.csv", {}, None)
        with pytest.raises(TypeError):
            creator.process_vulnerabilities()

    def test_case_2(self):
        creator = CsvCreatorForASA("final.csv", {}, "non una lista")
        with pytest.raises(TypeError):
            creator.process_vulnerabilities()

    def test_case_3(self):
        creator = CsvCreatorForASA("final.csv", {}, [])
        creator.process_vulnerabilities()
        assert creator.big_dict == {}

    def test_case_4(self):
        vulnerabilities = [
            {"component": "ClassA", "rule": "rule1"},
            {"component": "ClassA", "rule": "rule1"},
            {"component": "ClassB", "rule": "rule2"}
        ]
        creator = CsvCreatorForASA("final.csv", {}, vulnerabilities)
        creator.process_vulnerabilities()

        expected_dict = {
            "ClassA": {"rule1": 2},
            "ClassB": {"rule2": 1}
        }
        assert creator.big_dict == expected_dict


class TestWriteFinalCsv:

    def test_case_1(self):
        creator = CsvCreatorForASA("/path/file.csv", {}, [])
        with pytest.raises(FileNotFoundError):
            creator.write_final_csv()

    def test_case_2(self, tmpdir):
        file_path = tmpdir.join("final.csv")
        creator = CsvCreatorForASA(str(file_path), {}, [])
        creator.write_final_csv()

        with open(file_path, "r") as f:
            content = f.read()
        assert content == "Name\n"

    def test_case_3(self, tmpdir):
        file_path = tmpdir.join("final.csv")
        creator = CsvCreatorForASA(str(file_path), {"rule1": 0, "rule2": 0}, [])
        creator.write_final_csv()

        with open(file_path, "r") as f:
            content = f.read()
        assert content == "Name,rule1,rule2\n"

    def test_case_4(self, tmpdir):
        file_path = tmpdir.join("final.csv")

        vulnerabilities = [
            {"component": "ClassA", "rule": "rule1"},
        ]

        creator = CsvCreatorForASA(str(file_path), {}, vulnerabilities)
        creator.write_final_csv()

        with open(file_path, "r") as f:
            content = f.read()

        assert content == "Name\n"

    def test_case_5(self, tmpdir):
        file_path = tmpdir.join("final.csv")
        creator = CsvCreatorForASA(
            str(file_path),
            {"rule1": 0, "rule2": 0},
            []
        )
        creator.big_dict = {
            "ClassA": {"rule1": 2, "rule2": 1},
            "ClassB": {"rule2": 1}
        }

        creator.write_final_csv()
        with open(file_path, "r") as f:
            content = f.read()

        expected_content = (
            "Name,rule1,rule2\n"
            "ClassA,2,1\n"
            "ClassB,0,1\n"
        )

        assert content == expected_content
