
from unittest.mock import mock_open, patch, Mock, MagicMock

import pandas as pd
import pytest

import io

@pytest.fixture
def invalidate_format(request, mock_files):
    file_name = request.param
    data = 'severity\tupdateDate\tcomments\tline\tauthor\tproject\teffort\tmessage\tcreationDate\tstatus\torganization\tcomponent\ttextRange\tdebt\tkey\thash\nMINOR\t2020-07-03T17:57:05+0200\t\t71.0\t\tjava:S2386\tProva_Mining_Second_Part\t15min\t"Make this member ""protected""."\t2020-07-03T17:57:05+0200\tVULNERABILITY\t\tProva_Mining_Second_Part:src/RepositoryMining19/866/17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\tdefault-organization\t{startLine=71.0, endLine=71.0, startOffset=33.0, endOffset=59.0}\t15min\tAXMVa5NrkLspzIj1dA_E\tcef48bca33fc27fd295ef071f478584d\tOPEN\nMINOR\t2020-07-03T17:57:05+0200\t\t564.0\t\tjava:S1148\tProva_Mining_Second_Part\t10min\tUse a logger to log this exception.\t2020-07-03T17:57:05+0200\tVULNERABILITY\t\tProva_Mining_Second_Part:src/RepositoryMining19/866/17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\tdefault-organization\t{startLine=564.0, endLine=564.0, startOffset=14.0, endOffset=29.0}\t10min\tAXMVa5NrkLspzIj1dA_D\t2dc1665d31b37f9aa7408939a0365027\tOPEN\n'

    df = pd.read_csv(io.StringIO(data), sep='\t')

    if df.shape[1] > 10:
        df = df.iloc[:, 10:]

    invalid_content = df.to_csv(sep='\t', index=False).strip()

    mock_files[file_name] = mock_open(read_data=invalid_content)
    yield mock_files

@pytest.fixture
def mock_files(request):
    file_mocks = request.param
    mocks = {file: mock_open(read_data=data) for file, data in file_mocks.items()}

    def mock_open_side_effect(file, mode='r'):
        if file in mocks:
            mock_instance = mocks[file]
            return mock_instance(file, mode)
        default_mock = mock_open(read_data='Default data')
        return default_mock()

    with patch('builtins.open', mock_open_side_effect) as _mock_open:
        yield mocks

@pytest.fixture
def mock_op_permission_err(request):
    file_to_fail = request.param

    mock = mock_open(read_data='Test data')

    def mock_open_side_effect(file, mode='r'):
        if file == file_to_fail:
            raise PermissionError
        return mock()

    with patch('builtins.open', mock_open_side_effect) as _mock_open:
        yield mock


