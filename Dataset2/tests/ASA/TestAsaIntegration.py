import csv
import os
from unittest import mock
import pytest
from Dataset2.mining_results_asa.SonarAnalyzer import SonarAnalyzer


class TestAsaIntegration:
    @mock.patch.object(SonarAnalyzer, "process_repositories", side_effect=Exception("Host unreachable"))
    def test_case_1(self, mock_process_repositories, main_instance):
        with pytest.raises(Exception):
            main_instance.run_ASA("host", "token", "sonar-scanner.bat")

        mock_process_repositories.assert_called_once()

    @mock.patch.object(SonarAnalyzer, "process_repositories", side_effect=Exception("Host unreachable"))
    def test_case_2(self, mock_process_repositories, main_instance):
        with pytest.raises(Exception):
            main_instance.run_ASA("host", "token", "sonar-scanner.bat")

        mock_process_repositories.assert_called_once()

    @mock.patch.object(SonarAnalyzer, "process_repositories", side_effect=Exception("Host unreachable"))
    def test_case_3(self, mock_process_repositories, main_instance):
        with pytest.raises(Exception):
            main_instance.run_ASA("host", "token", "sonar-scanner.bat")

        mock_process_repositories.assert_called_once()

    @mock.patch.object(SonarAnalyzer, "process_repositories", side_effect=Exception("Host unreachable"))
    def test_case_4(self, mock_process_repositories, main_instance):
        with pytest.raises(Exception):
            main_instance.run_ASA("host", "token", "sonar-scanner.bat")

        mock_process_repositories.assert_called_once()

    @mock.patch.object(SonarAnalyzer, "process_repositories")
    def test_case_5(self, mock_process_repositories, main_instance, mock_empty_result_csv):
        main_instance.run_ASA("host", "token", "sonar-scanner.bat")

        final_csv_path = main_instance.base_dir / "mining_results_asa" / "csv_ASA_final.csv"
        assert os.path.exists(final_csv_path)

        with open(final_csv_path, mode="r") as file:
            reader = csv.reader(file, delimiter=",")
            rows = sum(1 for _ in reader)
            assert rows == 1

    @mock.patch.object(SonarAnalyzer, "process_repositories")
    def test_case_6(self, mock_process_repositories, main_instance, mock_result_csv):
        main_instance.run_ASA("host", "token", "sonar-scanner.bat")

        final_csv_path = main_instance.base_dir / "mining_results_asa" / "csv_ASA_final.csv"
        assert os.path.exists(final_csv_path)

        with open(final_csv_path, mode="r") as file:
            reader = csv.reader(file, delimiter=",")
            rows = sum(1 for _ in reader)
            assert rows > 1

    @mock.patch.object(SonarAnalyzer, "process_repositories")
    def test_case_7(self, mock_process_repositories, main_instance):
        with pytest.raises(FileNotFoundError):
            main_instance.run_ASA("host", "token", "sonar-scanner.bat")

        mock_process_repositories.assert_called_once()
