import csv
import os

import pytest
from unittest import mock
from Dataset2.mining_results_asa.SonarAnalyzer import SonarAnalyzer
from Dataset2.Main import Main


@pytest.fixture
def setup(tmp_path):
    base_dir = tmp_path / "base_dir"
    base_dir.mkdir(parents=True, exist_ok=True)

    mining_results_asa_dir = base_dir / "mining_results_asa"
    mining_results_asa_dir.mkdir(parents=True, exist_ok=True)

    project_dir = base_dir / "mining_results" / "RepositoryMining1" / "0" / "57f2ccb66946943fbf3b3f2165eac1c8eb6b1523"
    project_dir.mkdir(parents=True, exist_ok=True)

    yield base_dir


@pytest.fixture
def sonar_analyzer(setup):
    return SonarAnalyzer(
        sonar_host="http://localhost:9000",
        sonar_token="valid_token",
        sonar_path="/path/to/sonarscanner",
        file_name="output.csv",
        base_dir=setup
    )


@pytest.fixture
def sonar_analyzer_issues(java_files):
    return SonarAnalyzer(
        sonar_host="http://localhost:9000",
        sonar_token="valid_token",
        sonar_path="/path/to/sonarscanner",
        file_name="output.csv",
        base_dir=java_files
    )


@pytest.fixture
def no_mining_results_dir(tmp_path):
    base_dir = tmp_path
    base_dir.mkdir(parents=True, exist_ok=True)

    yield base_dir


@pytest.fixture
def no_repo_mining_dir(tmp_path):
    base_dir = tmp_path
    base_dir.mkdir(parents=True, exist_ok=True)

    project_dir = base_dir / "mining_results"
    project_dir.mkdir(parents=True, exist_ok=True)

    yield base_dir


@pytest.fixture
def no_cve_dir(tmp_path):
    base_dir = tmp_path
    base_dir.mkdir(parents=True, exist_ok=True)

    project_dir = base_dir / "mining_results" / "RepositoryMining1"
    project_dir.mkdir(parents=True, exist_ok=True)

    yield base_dir


@pytest.fixture
def java_files(tmp_path):
    base_dir = tmp_path / "base_dir"
    base_dir.mkdir(parents=True, exist_ok=True)

    mining_results_asa_dir = base_dir / "mining_results_asa"
    mining_results_asa_dir.mkdir(parents=True, exist_ok=True)

    project_dir = base_dir / "mining_results" / "RepositoryMining1" / "0" / "57f2ccb66946943fbf3b3f2165eac1c8eb6b1523" / "AbstractMvcView.java"
    project_dir.mkdir(parents=True, exist_ok=True)

    yield base_dir


@pytest.fixture
def output_file_with_issue(sonar_analyzer):
    fieldnames = [
        "severity", "updateDate", "line", "rule", "project", "effort", "message",
        "creationDate", "type", "component", "textRange", "debt", "key", "hash", "status"
    ]
    issue = {
        "severity": "BLOCKER",
        "updateDate": "2024-10-09T15:40:56+0200",
        "line": 319,
        "rule": "java:S6437",
        "project": "RepositoryMining1:1:9137e6cc45922b529fb776c6857647a3935471bb",
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

    with open(os.path.join(sonar_analyzer.base_dir, sonar_analyzer.output_csv), mode="w", newline="\n") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerow(issue)


@pytest.fixture
def sonar_mock():
    with mock.patch("builtins.open", mock.mock_open()) as mock_file:
        yield mock_file


@pytest.fixture
def mock_mining_results(tmp_path):
    base_dir = tmp_path / "base_dir"
    base_dir.mkdir(parents=True, exist_ok=True)

    mining_results_asa_dir = base_dir / "mining_results"
    mining_results_asa_dir.mkdir(parents=True, exist_ok=True)
    return mining_results_asa_dir


# Integration
@pytest.fixture
def main_instance(setup):
    yield Main(base_dir=setup)


@pytest.fixture
def mock_result_csv(setup):
    mining_results_asa_dir = setup / "mining_results_asa"
    print("MiningResultsASADIR: ", mining_results_asa_dir)

    with open(mining_results_asa_dir / "RepositoryMining_ASAResults.csv", "w") as f:
        f.write("severity;updateDate;line;rule;project;effort;message;creationDate;type;component;textRange;debt;key"
                ";hash;status\nN/A;N/A;N/A;N/A;N/A;N/A;N/A;N/A;NO_ISSUES_FOUND;RepositoryMining1:0"
                ":57f2ccb66946943fbf3b3f2165eac1c8eb6b1523:AbstractMvcView.java;N/A;N/A;N/A;N/A;N/A\nBLOCKER;2024-10"
                "-09T15:40:56+0200;319;java:S6437;RepositoryMining1:1:9137e6cc45922b529fb776c6857647a3935471bb;1h"
                ";Revoke and change this password, as it is "
                "compromised.;2024-10-09T15:40:56+0200;VULNERABILITY;RepositoryMining1:1"
                ":9137e6cc45922b529fb776c6857647a3935471bb:JndiLdapContextFactoryTest.java;{'startLine': 319, "
                "'endLine': 319, 'startOffset': 34, 'endOffset': "
                "39};1h;e5b5a9e5-85f2-4ad1-9d77-a1ce37fd15e2;fe91b6223b318860e553b82b45b20812;OPEN")


@pytest.fixture
def mock_empty_result_csv(setup):
    mining_results_asa_dir = setup / "mining_results_asa"
    print("MiningResultsASADIR: ", mining_results_asa_dir)

    with open(mining_results_asa_dir / "RepositoryMining_ASAResults.csv", "w") as f:
        f.write("")
