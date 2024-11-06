import os

import numpy as np
import pandas as pd
import pytest
from unittest.mock import patch, mock_open, MagicMock

from Dataset2.Main import Main


@pytest.fixture
def mock_listdir_fixture(request):
    directories = request.param.get('directories', {})
    error_path = request.param.get('error_path', None)

    # Funzione mock per os.listdir
    def mock_listdir(path):
        if path == error_path:
            raise FileNotFoundError(f"The directory '{path}' was not found.")
        elif path in directories:
            return directories[path]
        else:
            raise FileNotFoundError(f"The directory '{path}' does not exist in the mock.")

    with patch('os.listdir', side_effect=mock_listdir):
        yield


@pytest.fixture
def mock_isdir_fixture(request):
    isdir_map = request.param.get('isdir_map', {})

    # Funzione mock per os.path.isdir
    def mock_isdir(path):
        return isdir_map.get(path, False)

    with patch('os.path.isdir', side_effect=mock_isdir):
        yield


@pytest.fixture
def mock_open_fixture(request):
    file_contents = request.param.get('file_contents', {}) if hasattr(request, 'param') else {}
    file_to_fail = request.param.get('file_to_fail', None)
    exception_type = request.param.get('exception_type', None)

    m_open = mock_open()

    def custom_open(file_name, mode='r', *args, **kwargs):
        file_basename = os.path.basename(file_name)
        print(file_basename, file_to_fail)
        if file_basename == file_to_fail:
            if 'w' in mode or 'a' in mode:  # Se aperto in modalità scrittura o append
                if exception_type == 'ValueError':
                    raise ValueError(f"Errore di valore durante la scrittura su {file_name}")
            if exception_type == 'PermissionError':
                raise PermissionError(f"Permesso negato per il file {file_name}")
            if exception_type == 'AccessError':
                raise PermissionError(f"Permesso negato per il file {file_name}")

        if 'r' in mode and file_basename in file_contents:
            mock_file = m_open(file_name, mode, *args, **kwargs)
            mock_file.read = MagicMock(return_value=file_contents[file_basename])
            return mock_file
        else:
            return m_open(file_name, mode, *args, **kwargs)

    with patch("builtins.open", custom_open):
        yield m_open


@pytest.fixture
def mock_path_join_fixture(request):
    def mock_join(*args):
        # Concatenare gli argomenti con il separatore '/'
        return "/".join(args)

    with patch('os.path.join', side_effect=mock_join):
        yield


@pytest.fixture
def mock_joblib_load(request):
    fail_path = request.param.get('fail_path')
    predict_error = request.param.get('predict_error', False)
    encoder_error = request.param.get('encoder_error', False)
    with patch('joblib.load') as mocked_load:
        def side_effect(path):
            if path == fail_path:
                raise FileNotFoundError(f"File not found: {path}")
            elif path == 'vocab.pkl':
                return ['Feature1', 'Feature2']  # Ritorna un vocabolario fittizio
            elif path == 'model.pkl':
                mock_model = MagicMock()
                if predict_error:
                    mock_model.predict.side_effect = ValueError("Prediction Error")
                else:
                    mock_model.predict.return_value = [0, 1]  # Mock della predizione
                return mock_model
            elif path == 'encoder.pkl':
                mock_encoder = MagicMock()
                if encoder_error:
                    mock_encoder.inverse_transform.side_effect = ValueError("Encoding Error")
                else:
                    mock_encoder.inverse_transform.return_value = np.array(['pos', 'neg'])
                return mock_encoder
            elif not path.endswith('.pkl'):
                raise ValueError("File must end with .pkl")
            else:
                return MagicMock()  # Ritorna un mock generico per altri file validi

        mocked_load.side_effect = side_effect
        yield mocked_load


@pytest.fixture
def mock_read_csv(request):
    fail_path = request.param.get('fail_path', None)
    content = request.param.get('content', None)

    with patch('pandas.read_csv') as mocked_read_csv:
        def side_effect(path):
            if path == fail_path:
                raise FileNotFoundError(f"File not found: {path}")
            if not path.endswith('.csv'):
                raise ValueError("File must end with .csv")
            if content != None:
                return pd.DataFrame({content})
            return pd.DataFrame({'Name': ['Test1', 'Test2'], 'Feature1': [1, 2], 'Feature2': [0, 1]})

        mocked_read_csv.side_effect = side_effect
        yield mocked_read_csv


@pytest.fixture
def mock_os():
    with patch('os.makedirs') as mocked_makedirs, \
            patch('os.path.dirname', return_value="mock_dir") as mocked_dirname:
        yield mocked_makedirs, mocked_dirname


@pytest.fixture
def mock_to_csv():
    with patch('pandas.DataFrame.to_csv') as mocked_to_csv:
        yield mocked_to_csv


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
def main_instance(setup):
    yield Main(base_dir=setup)


@pytest.fixture
def mock_result_csv(setup):
    mining_results_asa_dir = setup / "mining_results_asa"

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

    with open(mining_results_asa_dir / "RepositoryMining_ASAResults.csv", "w") as f:
        f.write("")
