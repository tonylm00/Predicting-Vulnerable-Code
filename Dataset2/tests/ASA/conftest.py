
from unittest.mock import mock_open, patch, Mock, MagicMock

import pandas as pd
import pytest
import os
import shutil
import io

BACK_UP_DIR = 'temp_files'
NAME_DIR = 'ASA'
TEST_DIR = 'tests'

RES_NEG_NAME = 'RepositoryMining_ASAResults_neg.csv'
RES_POS_NAME = 'RepositoryMining_ASAResults_pos.csv'

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
def invalidate_json_format(request, mock_files):
    file_name = request.param
    data = 'severity\tupdateDate\tcomments\tline\tauthor\tproject\teffort\tmessage\tcreationDate\tstatus' \
           '\torganization\tcomponent\ttextRange\tdebt\tkey\thash\nMINOR\t2020-07-03T17:57:05+0200\t\t71.0' \
           '\t\tjava:S2386\tProva_Mining_Second_Part\t15min\t"Make this member ""protected""."\t2020-07-03T17:57:05+0200' \
           '\tVULNERABILITY' \
           '\tProva_Mining_Second_Part:src/RepositoryMining19/866/17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java' \
           '\tdefault-organization\t{startLine=71.0, endLine=71.0, startOffset=33.0, endOffset=59.0}\t15min' \
           '\tAXMVa5NrkLspzIj1dA_E\tcef48bca33fc27fd295ef071f478584d\tOPEN\nMINOR\t2020-07-03T17:57:05+0200\t' \
           '\t564.0\t\tjava:S1148\tProva_Mining_Second_Part\t10min\tUse a logger to log this exception.' \
           '\t2020-07-03T17:57:05+0200\tVULNERABILITY\t' \
           '\tProva_Mining_Second_Part:src/RepositoryMining19/866/17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java' \
           '\tdefault-organization\t{startLine=564.0, endLine=564.0, startOffset=14.0, endOffset=29.0}\t10min' \
           '\tAXMVa5NrkLspzIj1dA_D\t2dc1665d31b37f9aa7408939a0365027\tOPEN\n'

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

@pytest.fixture
def mock_op_fail(request, mock_files):
    # This will reuse the mock_files fixture
    file_to_fail = request.param  # File that should raise FileNotFoundError

    # Override the specific file to raise FileNotFoundError
    failing_mock = mock_open()  # Create a mock instance
    failing_mock.side_effect = FileNotFoundError(f"Mocked file {file_to_fail} not found.")

    # Update the mock_files dictionary to use the failing mock for the specific file
    mock_files[file_to_fail] = failing_mock

    def mock_open_side_effect(file, mode='r'):
        if file in mock_files:
            return mock_files[file](file, mode)
        # Fallback if not in mocks
        default_mock = mock_open(read_data='Default data')
        return default_mock()

    with patch('builtins.open', mock_open_side_effect):
        yield mock_files

#INTEGRATION FIXTURE

@pytest.fixture
def setup_dir():
    cwd = os.getcwd()
    print("CWD:", cwd)
    if NAME_DIR not in cwd:
        test_path = os.path.join(os.getcwd(), "Dataset2", TEST_DIR, NAME_DIR)
        print("TEST_PATH:", test_path)
        os.chdir(test_path)

    yield

    os.chdir(cwd)
    print(f"Changed directory to '{cwd}'.")

@pytest.fixture
def remove_result_file(request, setup_dir):

    yield

    result_file_names = request.param

    for result_file_name in result_file_names:

        # Construct the full file path if needed, e.g., if you have the file in a subdirectory
        file_path = os.path.join(os.getcwd(), result_file_name)

        # Check if the file exists
        if os.path.exists(file_path):
            # Remove the file
            os.remove(file_path)
            print(f"File '{result_file_name}' has been removed.")
        else:
            print(f"File '{result_file_name}' does not exist.")

@pytest.fixture
def prepare_content_data(request):
    feature_neg_dict, feature_pos_dict = request.param

    HEADER = '''severity\tupdateDate\tcomments\tline\tauthor\trule\tproject\teffort\tmessage\tcreationDate\ttype\ttags\tcomponent\tflows\torganization\ttextRange\tdebt\tkey\thash\tstatus'''

    DATA = '''\nMINOR\t2020-07-03T17:57:05+0200\t\t71.0\t\trule_to_change\tProva_Mining_Second_Part\t15min\t"Make this member ""protected""."\t2020-07-03T17:57:05+0200\tVULNERABILITY\t\tProva_Mining_Second_Part:src/RepositoryMining19/866/component_to_change\tdefault-organization\t{startLine=71.0, endLine=71.0, startOffset=33.0, endOffset=59.0}\t15min\tAXMVa5NrkLspzIj1dA_E\tcef48bca33fc27fd295ef071f478584d\tOPEN'''

    INVALID_DATA = HEADER + '''\nMINOR\t2020-07-03T17:57:05+0200\t\t71.0\t\tjava:S2386\tProva_Mining_Second_Part\t15min'''

    content = []

    i=0
    for dict in [feature_neg_dict, feature_pos_dict]:
        if 'is_invalid' in dict.keys() and dict['is_invalid']:
            content.append(INVALID_DATA)
        else:
            number_of_records = dict['number_of_records']
            content.append(HEADER)
            if number_of_records >0:
                content[i]+= DATA
                if number_of_records > 1:
                    if not dict['is_rule_repeated']:
                        content[i] = content[i].replace('rule_to_change', 'java:S2386')
                    content[i] += DATA
                content[i] = content[i].replace('rule_to_change', 'java:S2385')
                content[i] = content[i].replace('component_to_change', dict['component'])

                if 'no_vuln' in dict.keys() and dict['no_vuln']:
                    content[i] = content[i].replace('VULNERABILITY', "BUG")
        i+=1


    yield {RES_NEG_NAME: content[0], RES_POS_NAME:content[1]}


@pytest.fixture
def manage_temp_input_files(request, prepare_content_data, setup_dir):
    content_dict = prepare_content_data
    file_names = request.param

    for file_name in file_names:
        if file_name in content_dict.keys():
            with open(file_name, "w") as file:
                file.write(content_dict[file_name])

    yield

    for file_name in file_names:
        # Construct the full file path if needed, e.g., if you have the file in a subdirectory
        file_path = os.path.join(os.getcwd(), file_name)

        if os.path.exists(file_path):
            # Remove the file
            os.remove(file_path)
            print(f"File '{file_name}' has been removed.")
        else:
            print(f"File '{file_name}' does not exist.")










