import configparser
import csv
import os
import pytest


class TestAsaIntegration:
    config = configparser.ConfigParser()
    config.read('..\\System\\config.ini')

    SONAR_TOKEN_TXT = config.get('SonarConfig', 'SONAR_TOKEN')
    SONAR_HOST_TXT = config.get('SonarConfig', 'SONAR_HOST')
    SONAR_PATH_TXT = config.get('SonarConfig', 'SONAR_PATH')

    def test_case_1(self, main_instance):
        with pytest.raises(Exception):
            main_instance.run_ASA("http://ip:9000", self.SONAR_TOKEN_TXT, self.SONAR_PATH_TXT)

    def test_case_2(self, main_instance):
        with pytest.raises(Exception):
            main_instance.run_ASA(self.SONAR_HOST_TXT, "token", self.SONAR_PATH_TXT)

    def test_case_3(self, main_instance):
        with pytest.raises(Exception):
            main_instance.run_ASA(self.SONAR_HOST_TXT, self.SONAR_TOKEN_TXT, "path/to/sonarscanner")

    def test_case_4(self, main_instance_no_base_dir):
        with pytest.raises(Exception):
            main_instance_no_base_dir.run_ASA(self.SONAR_HOST_TXT, self.SONAR_TOKEN_TXT, self.SONAR_PATH_TXT)

    def test_case_5(self, main_instance):
        main_instance.run_ASA(self.SONAR_HOST_TXT, self.SONAR_TOKEN_TXT, self.SONAR_PATH_TXT)

        final_csv_path = main_instance.base_dir / "mining_results_asa" / "csv_ASA_final.csv"
        assert os.path.exists(final_csv_path)

        with open(final_csv_path, mode="r") as file:
            reader = csv.reader(file, delimiter=",")
            rows = sum(1 for _ in reader)
            assert rows == 1

    def test_case_6(self, main_instance, java_files):
        main_instance.run_ASA(self.SONAR_HOST_TXT, self.SONAR_TOKEN_TXT, self.SONAR_PATH_TXT)

        final_csv_path = main_instance.base_dir / "mining_results_asa" / "csv_ASA_final.csv"
        assert os.path.exists(final_csv_path)

        with open(final_csv_path, mode="r") as file:
            reader = csv.reader(file, delimiter=",")
            rows = sum(1 for _ in reader)
            assert rows > 1

    def test_case_7(self, main_instance):
        main_instance.run_ASA(self.SONAR_HOST_TXT, self.SONAR_TOKEN_TXT, self.SONAR_PATH_TXT)

        final_csv_path = main_instance.base_dir / "mining_results_asa" / "csv_ASA_final.csv"
        assert os.path.exists(final_csv_path)

        with open(final_csv_path, mode="r") as file:
            reader = csv.reader(file, delimiter=",")
            rows = sum(1 for _ in reader)
            assert rows == 1
