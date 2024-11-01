import csv
import os

import pytest
import requests

from Dataset2.mining_results_asa.SonarAnalyzer import SonarAnalyzer
from unittest import mock


class TestCreateSonarProperties:
    @mock.patch("os.path.exists", return_value=True)
    def test_case_1(self, sonar_mock, setup):
        base_dir = setup
        sonar_host = "http://127.0.0.1:9000"
        sonar_path = "sonar-scanner.bat"
        user_token = "token"
        commit_dir = "base_dir\\mining_results\\RepositoryMining1\\0\\57f2ccb66946943fbf3b3f2165eac1c8eb6b1523"
        analyzer = SonarAnalyzer(sonar_host, user_token, sonar_path, "output.csv", base_dir)

        with pytest.raises(FileNotFoundError):
            analyzer.create_sonar_properties(None, commit_dir)

    @mock.patch("os.path.exists", return_value=True)
    def test_case_2(self, sonar_mock, setup):
        base_dir = setup
        sonar_host = "http://127.0.0.1:9000"
        sonar_path = "sonar-scanner.bat"
        user_token = "token"
        commit_dir = "base_dir\\mining_results\\RepositoryMining1\\0\\57f2ccb66946943fbf3b3f2165eac1c8eb6b1523"
        analyzer = SonarAnalyzer(sonar_host, user_token, sonar_path, "output.csv", base_dir)
        with pytest.raises(FileNotFoundError):
            analyzer.create_sonar_properties("valid_project_key", commit_dir)

    @mock.patch("os.path.exists", return_value=True)
    def test_case_3(self, mock_open, java_files):
        base_dir = java_files
        sonar_host = "http://127.0.0.1:9000"
        sonar_path = "sonar-scanner.bat"
        user_token = "token"
        analyzer = SonarAnalyzer(sonar_host, user_token, sonar_path, "output.csv", base_dir)

        project_key = "pk"
        commit_dir = "mining_results\\RepositoryMining1\\0\\57f2ccb66946943fbf3b3f2165eac1c8eb6b1523"
        commit_dir = os.path.join(analyzer.base_dir, commit_dir)

        analyzer.create_sonar_properties(project_key, commit_dir)
        assert os.path.exists(os.path.join(commit_dir, "sonar-project.properties"))
        with open(os.path.join(commit_dir, "sonar-project.properties"), mode="r") as file:
            reader = csv.reader(file, delimiter=";")
            rows = sum(1 for _ in reader)
            assert rows > 0


class TestRunSonarScanner:

    @mock.patch('os.path.abspath', side_effect=FileNotFoundError("Directory not found."))
    def test_case_1(self, mock_abspath, sonar_analyzer):
        with pytest.raises(FileNotFoundError, match="Directory not found"):
            sonar_analyzer.run_sonar_scanner("valid_project_key", "/non_existent_dir")

    @mock.patch('subprocess.run')
    def test_case_2(self, mock_run, sonar_analyzer):
        mock_run.return_value = mock.Mock(stderr="Error status returned by url")
        sonar_analyzer.logger = mock.Mock()

        with pytest.raises(Exception):
            sonar_analyzer.run_sonar_scanner("invalid_project_key", "/existent_dir")

        sonar_analyzer.logger.error.assert_called()

    @mock.patch('subprocess.run')
    def test_case_3(self, mock_run, sonar_analyzer):
        mock_run.return_value = mock.Mock(stderr="Error status returned by url")
        sonar_analyzer.logger = None

        with pytest.raises(AttributeError):
            sonar_analyzer.run_sonar_scanner("invalid_project_key", "/existent_dir")

    @mock.patch('subprocess.run')
    def test_case_4(self, mock_run, sonar_analyzer):
        mock_run.return_value = mock.Mock(stderr="Connection refused")
        sonar_analyzer.logger = mock.Mock()

        with pytest.raises(Exception, match="SonarQube is not reported to be active."):
            sonar_analyzer.run_sonar_scanner("valid_project_key", "/existent_dir")

        sonar_analyzer.logger.error.assert_called_once_with(
            "SonarQube is not reported to be active. Remember to activate it and check if the host is correct."
        )

    @mock.patch('subprocess.run')
    def test_case_5(self, mock_run, sonar_analyzer):
        mock_run.return_value = mock.Mock(stderr="Error status returned by url")
        sonar_analyzer.logger = mock.Mock()

        with pytest.raises(Exception, match="SonarQube Error. Check if the token entered is correct."):
            sonar_analyzer.run_sonar_scanner("valid_project_key", "/existent_dir")

        sonar_analyzer.logger.error.assert_called_once_with("SonarQube Error. Check if the token entered is correct.")

    @mock.patch('subprocess.run')
    def test_case_6(self, mock_run, sonar_analyzer):
        mock_run.return_value = mock.Mock(stderr="Connection refused")
        sonar_analyzer.logger = mock.Mock()

        with pytest.raises(Exception,
                           match="SonarQube is not reported to be active. Remember to activate it and check if the host is correct."):
            sonar_analyzer.run_sonar_scanner("valid_project_key", "/existent_dir")

        sonar_analyzer.logger.error.assert_called_once_with(
            "SonarQube is not reported to be active. Remember to activate it and check if the host is correct.")

    @mock.patch('subprocess.run', side_effect=FileNotFoundError("SonarScanner not found"))
    def test_case_7(self, mock_run, sonar_analyzer):
        sonar_analyzer.logger = mock.Mock()
        sonar_analyzer.sonar_path = "/non_existent_dir"

        with pytest.raises(Exception, match="SonarScanner not found"):
            sonar_analyzer.run_sonar_scanner("valid_project_key", "/existent_dir")

        sonar_analyzer.logger.error.assert_called_once_with("SonarScanner not found.")

    @mock.patch('subprocess.run')
    def test_case_8(self, mock_run, sonar_analyzer):
        mock_run.return_value = mock.Mock(stderr="", stdout="Analysis successful")
        sonar_analyzer.logger = mock.Mock()

        sonar_analyzer.run_sonar_scanner("valid_project_key", "/existent_dir")

        assert mock_run.called
        sonar_analyzer.logger.error.assert_not_called()


class TestGetAnalysisID:

    def test_case_1(self, sonar_analyzer):
        with pytest.raises(Exception):
            sonar_analyzer.get_analysis_id("invalid_project_key")

    @mock.patch('requests.get')
    def test_case_2(self, mock_get, sonar_analyzer):
        mock_get.return_value = None
        with pytest.raises(Exception):
            sonar_analyzer.get_analysis_id("valid_project_key")

    @mock.patch('requests.get')
    def test_case_3(self, mock_get, sonar_analyzer):
        mock_get.side_effect = requests.ConnectionError
        with pytest.raises(Exception):
            sonar_analyzer.get_analysis_id("valid_project_key")

    @mock.patch('requests.get')
    def test_case_4(self, mock_get, sonar_analyzer):
        mock_response = mock.Mock()
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        sonar_analyzer.sonar_host = "valid_host"
        sonar_analyzer.sonar_token = "valid_token"

        assert sonar_analyzer.get_analysis_id("valid_project_key") is None

    @mock.patch('requests.get')
    def test_case_5(self, mock_get, sonar_analyzer):
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            "queue": [],
            "current": {"id": "1", "status": "SUCCESS"}
        }
        mock_get.return_value = mock_response

        sonar_analyzer.sonar_host = "valid_host"
        sonar_analyzer.sonar_token = "valid_token"

        project_id = sonar_analyzer.get_analysis_id("valid_project_key")

        assert project_id == "1"


class TestCheckAnalysisStatus:
    @mock.patch('requests.get')
    def test_case_1(self, mock_get, sonar_analyzer):
        mock_get.return_value.status_code = 401
        mock_get.return_value.json.return_value = {"task": None}

        result = sonar_analyzer.check_analysis_status("invalid_id")
        assert result is None

    @mock.patch('requests.get')
    def test_case_2(self, mock_get, sonar_analyzer):
        mock_get.side_effect = requests.exceptions.RequestException

        with pytest.raises(Exception):
            sonar_analyzer.check_analysis_status("valid_id")

    @mock.patch('requests.get')
    def test_case_3(self, mock_get, sonar_analyzer):
        mock_get.side_effect = requests.exceptions.RequestException

        with pytest.raises(Exception):
            sonar_analyzer.check_analysis_status("valid_id")

    @mock.patch('requests.get')
    def test_case_4(self, mock_get, sonar_analyzer):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "task": {"status": "SUCCESS"}
        }

        assert sonar_analyzer.check_analysis_status("valid_id") == "SUCCESS"


class TestGetProjectIssues:

    @mock.patch('requests.get')
    @mock.patch.object(SonarAnalyzer, 'wait_for_analysis_completion', return_value=False)
    @mock.patch.object(SonarAnalyzer, 'get_analysis_id', return_value=None)
    def test_case_1(self, mock_get, mock_wait, mock_get_id, sonar_analyzer):
        result = sonar_analyzer.get_project_issues("id")
        assert result == []

    @mock.patch('requests.get')
    @mock.patch.object(SonarAnalyzer, 'wait_for_analysis_completion', return_value=False)
    @mock.patch.object(SonarAnalyzer, 'get_analysis_id', return_value=None)
    def test_case_2(self, mock_get, mock_wait, mock_get_id, sonar_analyzer):
        sonar_analyzer.logger = None
        with pytest.raises(AttributeError):
            sonar_analyzer.get_project_issues("valid_id")

    @mock.patch('requests.get')
    @mock.patch.object(SonarAnalyzer, 'wait_for_analysis_completion', return_value=False)
    @mock.patch.object(SonarAnalyzer, 'get_analysis_id', return_value=None)
    def test_case_3(self, mock_get, mock_wait, mock_get_id, sonar_analyzer):
        sonar_analyzer.sonar_host = None
        result = sonar_analyzer.get_project_issues("valid_id")
        assert result == []

    @mock.patch('requests.get')
    @mock.patch.object(SonarAnalyzer, 'wait_for_analysis_completion', return_value=False)
    @mock.patch.object(SonarAnalyzer, 'get_analysis_id', return_value=None)
    def test_case_4(self, mock_get, mock_wait, mock_get_id, sonar_analyzer):
        sonar_analyzer.sonar_token = None
        result = sonar_analyzer.get_project_issues("valid_id")
        assert result == []

    @mock.patch('requests.get')
    def test_case_5(self, mock_get, sonar_analyzer):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "issues": [{"id": "issue1"}, {"id": "issue2"}]
        }

        result = sonar_analyzer.get_project_issues("valid_id")
        assert result == [{"id": "issue1"}, {"id": "issue2"}]


class TestSaveIssuesToCsv:

    def test_case_1(self, sonar_analyzer):
        issues = []

        project_dir = sonar_analyzer.base_dir / "mining_results" / "RepositoryMining1" / "1" / "57f2ccb66946943fbf3b3f2165eac1c8eb6b1523"

        with pytest.raises(FileNotFoundError):
            sonar_analyzer.save_issues_to_csv(issues, project_dir)

    def test_case_2(self, sonar_analyzer):
        issues = []

        project_dir = sonar_analyzer.base_dir / "mining_results" / "RepositoryMining1" / "0" / "57f2ccb66946943fbf3b3f2165eac1c8eb6b1523"
        output_csv = os.path.join(sonar_analyzer.base_dir, sonar_analyzer.output_csv)

        if os.path.exists(output_csv):
            os.remove(output_csv)

        assert not os.path.exists(output_csv)

        sonar_analyzer.save_issues_to_csv(issues, project_dir)
        assert os.path.exists(output_csv)

        fieldnames = ["severity", "updateDate", "line", "rule", "project", "effort", "message", "creationDate", "type",
                      "component", "textRange", "debt", "key", "hash", "status"]

        with open(output_csv, mode="r") as file:
            reader = csv.DictReader(file, delimiter=";")
            assert reader.fieldnames == fieldnames

    def test_case_3(self, sonar_analyzer):
        issues = []
        project_dir = sonar_analyzer.base_dir / "mining_results" / "RepositoryMining1" / "0" / "57f2ccb66946943fbf3b3f2165eac1c8eb6b1523"
        output_csv = os.path.join(sonar_analyzer.base_dir, sonar_analyzer.output_csv)

        java_file_path = project_dir / "ExampleClass.java"

        # Creazione dir e file java
        os.makedirs(project_dir, exist_ok=True)
        with open(java_file_path, mode="w") as java_file:
            java_file.write("""
        public class ExampleClass {
            public static void main(String[] args) {
                System.out.println("Hello, World!");
            }
        }
        """)

        assert not os.path.exists(output_csv)
        sonar_analyzer.save_issues_to_csv(issues, project_dir)

        with open(output_csv, mode="r") as file:
            reader = csv.reader(file, delimiter=";")
            rows_before = sum(1 for _ in reader)
            assert rows_before == 2

    def test_case_4(self, sonar_analyzer, output_file_with_issue):
        issues = []
        project_dir = sonar_analyzer.base_dir / "mining_results" / "RepositoryMining1" / "0" / "57f2ccb66946943fbf3b3f2165eac1c8eb6b1523"
        output_csv = os.path.join(sonar_analyzer.base_dir, sonar_analyzer.output_csv)

        java_file_path = project_dir / "ExampleClass.java"

        # Creazione dir e file java
        os.makedirs(project_dir, exist_ok=True)
        with open(java_file_path, mode="w") as java_file:
            java_file.write("""
        public class ExampleClass {
            public static void main(String[] args) {
                System.out.println("Hello, World!");
            }
        }
        """)
        with open(output_csv, mode="r") as file:
            reader = csv.reader(file, delimiter=";")
            rows_before = sum(1 for _ in reader)
            assert rows_before == 2

        assert os.path.exists(output_csv)
        sonar_analyzer.save_issues_to_csv(issues, project_dir)

        with open(output_csv, mode="r") as file:
            reader = csv.reader(file, delimiter=";")
            rows_after = sum(1 for _ in reader)
            assert rows_after == 3

    def test_case_5(self, sonar_analyzer):
        issues = [{
            "severity": "BLOCKER",
            "updateDate": "2024-10-09T15:40:56+0200",
            "line": 215,
            "rule": "java:S6437",
            "project": "RepositoryMining1:0:9137e6cc45922b529fb776c6857647a3935471bb",
            "effort": "1h",
            "message": "Revoke and change this password, as it is compromised.",
            "creationDate": "2024-10-09T15:40:56+0200",
            "type": "VULNERABILITY",
            "component": "RepositoryMining1:1:9137e6cc45922b529fb776c6857647a3935471bb:JndiLdapContextFactoryTest.java",
            "textRange": "{'startLine': 319, 'endLine': 319, 'startOffset': 34, 'endOffset': 39}",
            "debt": "1h",
            "key": "e5b5a9e5-85f2-4ad1-9d77-a1ce37fd15e2",
            "hash": "fe91b6223b318860e553b82b45b20812",
            "status": "OPEN"
        }]

        project_dir = sonar_analyzer.base_dir / "mining_results" / "RepositoryMining1" / "0" / "57f2ccb66946943fbf3b3f2165eac1c8eb6b1523"
        output_csv = os.path.join(sonar_analyzer.base_dir, sonar_analyzer.output_csv)
        assert not os.path.exists(output_csv)

        sonar_analyzer.save_issues_to_csv(issues, project_dir)

        with open(output_csv, mode="r") as file:
            reader = csv.reader(file, delimiter=";")
            rows = sum(1 for _ in reader)
            assert rows == 2

    def test_case_6(self, sonar_analyzer, output_file_with_issue):
        issue = {
            "severity": "BLOCKER",
            "updateDate": "2024-10-09T15:40:56+0200",
            "line": 215,
            "rule": "java:S6437",
            "project": "RepositoryMining1:0:9137e6cc45922b529fb776c6857647a3935471bb",
            "effort": "1h",
            "message": "Revoke and change this password, as it is compromised.",
            "creationDate": "2024-10-09T15:40:56+0200",
            "type": "VULNERABILITY",
            "component": "RepositoryMining1:1:9137e6cc45922b529fb776c6857647a3935471bb:JndiLdapContextFactoryTest.java",
            "textRange": "{'startLine': 319, 'endLine': 319, 'startOffset': 34, 'endOffset': 39}",
            "debt": "1h",
            "key": "e5b5a9e5-85f2-4ad1-9d77-a1ce37fd15e2",
            "hash": "fe91b6223b318860e553b82b45b20812",
            "status": "OPEN"
        }

        issues = [issue]

        project_dir = sonar_analyzer.base_dir / "mining_results" / "RepositoryMining1" / "0" / "57f2ccb66946943fbf3b3f2165eac1c8eb6b1523"
        output_csv = os.path.join(sonar_analyzer.base_dir, sonar_analyzer.output_csv)
        assert os.path.exists(output_csv)

        with open(output_csv, mode="r") as file:
            reader = csv.reader(file, delimiter=";")
            rows = sum(1 for _ in reader)
            assert rows == 2

        sonar_analyzer.save_issues_to_csv(issues, project_dir)

        with open(output_csv, mode="r") as file:
            reader = csv.reader(file, delimiter=";")
            rows = sum(1 for _ in reader)
            assert rows == 3


class TestProcessRepositories:

    def test_case_1(self, sonar_analyzer, no_mining_results_dir):
        sonar_analyzer.base_dir = no_mining_results_dir
        with pytest.raises(FileNotFoundError):
            sonar_analyzer.process_repositories()

    def test_case_2(self, sonar_analyzer, no_repo_mining_dir):
        sonar_analyzer.base_dir = no_repo_mining_dir
        sonar_analyzer.process_repositories()

        output_csv = os.path.join(sonar_analyzer.base_dir, sonar_analyzer.output_csv)
        assert not os.path.exists(output_csv)

    def test_case_3(self, sonar_analyzer, no_cve_dir):
        sonar_analyzer.base_dir = no_cve_dir
        sonar_analyzer.process_repositories()

        output_csv = os.path.join(sonar_analyzer.base_dir, sonar_analyzer.output_csv)
        assert not os.path.exists(output_csv)

    def test_case_4(self, sonar_analyzer):
        with pytest.raises(Exception):
            sonar_analyzer.process_repositories()

    def test_case_5(self, sonar_analyzer, java_files):
        sonar_analyzer.base_dir = java_files
        with pytest.raises(Exception):
            sonar_analyzer.process_repositories()

    @mock.patch.object(SonarAnalyzer, 'create_sonar_properties')
    @mock.patch.object(SonarAnalyzer, 'run_sonar_scanner')
    @mock.patch.object(SonarAnalyzer, 'get_project_issues')
    def test_case_6(self, mock_get_project_issues, mock_run_sonar_scanner,
                    mock_create_sonar_properties, sonar_analyzer_issues):
        mock_get_project_issues.return_value = []
        sonar_analyzer_issues.process_repositories()

        output_csv = os.path.join(sonar_analyzer_issues.base_dir, sonar_analyzer_issues.output_csv)
        assert os.path.exists(output_csv)

        with open(output_csv, mode="r") as file:
            rows = sum(1 for _ in file)
            assert rows == 2

    @mock.patch.object(SonarAnalyzer, 'create_sonar_properties')
    @mock.patch.object(SonarAnalyzer, 'run_sonar_scanner')
    @mock.patch.object(SonarAnalyzer, 'get_project_issues')
    def test_case_7(self, mock_get_project_issues, mock_run_sonar_scanner,
                    mock_create_sonar_properties, sonar_analyzer_issues):
        output_csv = os.path.join(sonar_analyzer_issues.base_dir, sonar_analyzer_issues.output_csv)

        assert not os.path.exists(output_csv)

        mock_get_project_issues.return_value = [{
            "severity": "BLOCKER",
            "updateDate": "2024-10-09T15:40:56+0200",
            "line": 215,
            "rule": "java:S6437",
            "project": "RepositoryMining1:0:9137e6cc45922b529fb776c6857647a3935471bb",
            "effort": "1h",
            "message": "Revoke and change this password, as it is compromised.",
            "creationDate": "2024-10-09T15:40:56+0200",
            "type": "VULNERABILITY",
            "component": "RepositoryMining1:1:9137e6cc45922b529fb776c6857647a3935471bb:JndiLdapContextFactoryTest.java",
            "textRange": "{'startLine': 319, 'endLine': 319, 'startOffset': 34, 'endOffset': 39}",
            "debt": "1h",
            "key": "e5b5a9e5-85f2-4ad1-9d77-a1ce37fd15e2",
            "hash": "fe91b6223b318860e553b82b45b20812",
            "status": "OPEN"
        }]

        sonar_analyzer_issues.process_repositories()

        assert os.path.exists(output_csv)

        with open(output_csv, mode="r") as file:
            rows = sum(1 for _ in file)
            assert rows == 2
