import csv
import shutil
from unittest.mock import mock_open, patch, Mock, MagicMock
import pytest
import os
import io
from git.exc import GitCommandError  # Import GitCommandError from gitpython
import requests
import re
from urllib.parse import urlparse

from requests.exceptions import InvalidURL, MissingSchema

@pytest.fixture
def create_temp_dataset():
    cwd = os.getcwd()
    directory = 'Divided_Dataset'
    filename = "1.csv"

    os.makedirs(directory, exist_ok=True)

    os.chdir(os.path.join(cwd, directory))

    # Create the empty file
    with open(filename, 'w') as file:
        # File is created and opened in write mode, but no content is written.
        pass

    yield

    if os.path.isfile(filename):
        os.remove(filename)

    os.chdir(cwd)

    if os.path.isdir(directory):
        try:
            os.rmdir(directory)
        except OSError as e:
            print(f"Error: {directory} : {e.strerror}")


@pytest.fixture
def process_data(request):

    is_data_empty = request.param

    input_csv_data = ''''''

    if not is_data_empty:
        # CSV data as a string
        input_csv_data = '''cve_id,repo_url,commit_id,cls
        49,https://github.com/apache/openjpa,87a4452be08b4f97274d0ccfac585ae85841e470,pos
        50,https://github.com/apache/camel,22c355bb4ffb500405499d189db30932ca5aac9,pos
        51,https://github.com/apache/struts,01e6b251b4db78bfb7971033652e81d1af4cb3e,pos'''


    # Create a DictReader object from the csv module, not from the string
    csv_file_like = io.StringIO(input_csv_data)
    csv_reader = csv.DictReader(csv_file_like)

    extracted_data = dict()
    for i, row in enumerate(csv_reader):
        extracted_data[i] = row

    yield input_csv_data, extracted_data

@pytest.fixture
def mock_setup_repo_exist(request, process_data):
    repo_exist = request.param

    list_dir = []

    repo_name = 'RepositoryMining2'

    if repo_exist:
        list_dir = [repo_name]

    input_csv_data, extracted_data = process_data
    with patch('os.listdir', return_value=list_dir) as mock_listdir, \
         patch('os.getcwd', return_value='test/path') as mock_cwd, \
         patch('os.mkdir') as mock_mkdir, \
         patch('builtins.open', mock_open(read_data=input_csv_data)) as mock_op, \
         patch('os.chdir') as mock_chdir, \
         patch('Dataset2.RepoMining.repo_Mining.startMiningRepo') as mock_start:
        yield mock_listdir, mock_cwd, mock_mkdir, mock_op, mock_chdir, mock_start, extracted_data


@pytest.fixture
def mock_op_fail(request):
    file_to_fail = request.param

    # Define a mock_open instance without conflicting variable names
    mock = mock_open(read_data='Test data')

    def mock_open_side_effect(file, mode='r'):
        if file == file_to_fail:
            raise FileNotFoundError(f"No such file or directory: '{file}'")
        # Return the mock object for other files
        return mock()

    # Patch 'builtins.open' with our mock side effect
    with patch('builtins.open', mock_open_side_effect) as _mock_open:
        yield mock  # Yield the file name to the test


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

    # Define a mock_open instance without conflicting variable names
    mock = mock_open(read_data='Test data')

    def mock_open_side_effect(file, mode='r'):
        if file == file_to_fail:
            raise PermissionError
        # Return the mock object for other files
        return mock()

    # Patch 'builtins.open' with our mock side effect
    with patch('builtins.open', mock_open_side_effect) as _mock_open:
        yield mock  # Yield the file name to the test


def create_mock_response(status_code, text=''):
    response = requests.Response()
    response.status_code = status_code
    response._content = text.encode('utf-8')  # Setting the response body content
    return response

@pytest.fixture
def mock_requests_get(request):
    # Retrieve parameters
    is_link_valid, link_exist, repo_exist, commit_exist = request.param

    url_regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    # Determine the error or response based on parameters
    def side_effect(url, *args, **kwargs):
        if re.match(url_regex, url) and '/commit' in url:
            if commit_exist:
                return create_mock_response(202, 'OK')
            else:
                return create_mock_response(404, 'OK')

        if url.startswith(('http://', 'https://')):
            if re.match(url_regex, url):
                if link_exist:
                    if repo_exist:
                        return create_mock_response(202, 'OK')
                    else:
                        return create_mock_response(404, 'OK')
                else:
                    parsed_url = urlparse(url)
                    host_with_port = parsed_url.netloc
                    host = host_with_port.split(':')[0]
                    raise requests.exceptions.ConnectionError("Failed to resolve " + host)
            else:
                raise InvalidURL('Invalid URL \'' + url + "\'")
        else:
            raise MissingSchema('Invalid URL \'' + url + "\'")


    with patch('requests.get', side_effect=side_effect) as mock:
        yield mock

@pytest.fixture
def mock_repo_mining(request):
    # Retrieve parameters
    is_commit_defined, is_mod_present, is_java_file_present, is_scb_present = request.param

    # Determine the error or response based on parameters
    def side_effect(url, *args, **kwargs):
        if not is_commit_defined:
            raise ValueError()
        else:
            mock_commit1 = MagicMock()
            mock_commit1.commit_id = 'commit1'
            mock_commit1.author_date = '2024-01-01'
            mock_commit1.modifications = []
            if is_mod_present:
                mod_filename = ''
                mod_source_code_before = None
                if is_java_file_present:
                    mod_filename = 'file1.java'
                else:
                    mod_filename = 'file1.py'

                if is_scb_present:
                    mod_source_code_before = 'public class File1 {}'

                # Create a mock modification instance with attributes
                m = MagicMock()
                m.filename = mod_filename
                m.source_code_before = mod_source_code_before

                # Append the modification to the commit's modifications list
                mock_commit1.modifications.append(m)

                # Create a mock repository mining instance
            mock_repo_mining_instance = Mock()
            mock_repo_mining_instance.traverse_commits.return_value = [mock_commit1]

            return mock_repo_mining_instance


    with patch('Dataset2.RepoMining.repo_Mining.RepositoryMining', side_effect=side_effect) as mock:
        yield mock

# Define the mock function with parameters
def mock_listdir(directory, cve_id, cve_id_exists, commit_id, commit_exists):
    if directory == '':
        return [cve_id] if cve_id_exists else []
    elif directory == cve_id:
        return [commit_id] if commit_exists else []
    elif directory == commit_id:
        return []  # Commit directories are empty initially
    return []

# Define the parameterized fixture
@pytest.fixture
def mock_os_listdir(request):
    params = request.param
    cve_id = params["cve_id"]
    cve_id_exists = params["cve_id_exists"]
    commit_id = params["commit_id"]
    commit_exists = params["commit_exists"]

    call_count = 0

    def side_effect(directory=None):
        nonlocal call_count
        call_count += 1

        # Define behavior based on call count
        if call_count == 1:
            return [cve_id] if cve_id_exists else []
        elif call_count == 2:
            return [commit_id] if commit_exists else []
        else:
            return []  # For subsequent calls

    with patch('os.listdir', side_effect=side_effect) as mock_listdir:
        yield mock_listdir, cve_id, commit_id



# Define the function to check if a directory name is admissible
def is_admissible_directory_name(name):
    # Define reserved names for Windows
    reserved_names = {
        'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    }

    # Check for reserved names
    if name.upper() in reserved_names:
        return False

    # Check for invalid characters
    invalid_chars = r'[<>:"/\\|?*]'
    if re.search(invalid_chars, name):
        return False

    # Check for length restrictions
    if len(name) > 255:
        return False

    # Check for leading or trailing spaces
    if name != name.strip():
        return False

    return True


def custom_chdir_side_effect(directory, path_exist):
    if not path_exist:
        raise FileNotFoundError("Directory does not exist")

    if isinstance(directory, str):
        if not is_admissible_directory_name(directory):
            raise OSError("Invalid directory format")
        # If valid and path exists, simulate normal behavior
    else:
        # Raise TypeError if the directory is not a string
        raise TypeError("Directory must be a string")


# Define the fixture to patch os.chdir with parameters
@pytest.fixture
def mock_os_chdir(request):
    params = request.param
    path_exist = params.get("check_path_exist", True)

    with patch('os.chdir', side_effect=lambda directory: custom_chdir_side_effect(directory, path_exist)) as mock_chdir:
        yield mock_chdir