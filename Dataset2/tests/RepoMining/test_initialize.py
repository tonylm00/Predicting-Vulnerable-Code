import csv
import io
from unittest import mock

import pytest
from unittest.mock import patch, mock_open, call
from Dataset2.RepoMining.repo_Mining import initialize

class TestInitialize:

    MINI_DATASET_NAME = 2


    @patch('builtins.open', new_callable=mock_open)
    @patch('os.listdir', return_value = ['RepositoryMining' + str(MINI_DATASET_NAME)])
    @patch('os.getcwd')
    @patch('os.mkdir')
    @patch('os.chdir')
    def test_case_1(self, mock_chdir, mock_mkdir, mock_getcwd, mock_listdir, mock_open, setup_dir):

        # Setup mocks
        mock_getcwd.return_value = 'Dataset2/tests/RepoMining'

        mock_open.side_effect = OSError

        with pytest.raises(OSError):
            # Call the function
            initialize('3<ddd-tc.txt')

        expected_chdir_calls = [
            call('..'),
            call('Dataset_Divided'),
        ]
        mock_chdir.assert_has_calls(expected_chdir_calls, any_order=False)

        mock_mkdir.assert_not_called()




    @patch('os.listdir', return_value = ['RepositoryMining' + str(MINI_DATASET_NAME)])
    @patch('os.getcwd')
    @patch('os.mkdir')
    @patch('os.chdir')
    @pytest.mark.parametrize('mock_op_fail', ['45.csv'], indirect=True)
    def test_case_2(self, mock_chdir, mock_mkdir, mock_getcwd, mock_lisdir, mock_op_fail, setup_dir):

        # Setup mocks
        mock_getcwd.return_value = 'Dataset2/tests/RepoMining'
        mock_open.side_effect = FileNotFoundError

        with pytest.raises(FileNotFoundError):
            # Call the function
            initialize(45)

        expected_chdir_calls = [
            call('..'),
            call('Dataset_Divided'),
        ]
        mock_chdir.assert_has_calls(expected_chdir_calls, any_order=False)

        mock_mkdir.assert_not_called()

    @patch('os.listdir', return_value = ['RepositoryMining' + str(MINI_DATASET_NAME)])
    @patch('os.getcwd')
    @patch('os.mkdir')
    @patch('os.chdir')
    @pytest.mark.parametrize('mock_op_fail', ['2.csv'], indirect=True)
    def test_case_3(self, mock_chdir, mock_mkdir, mock_getcwd, mock_listdir, mock_op_fail, setup_dir):

        # Setup mocks
        mock_getcwd.return_value = 'Dataset2/tests/RepoMining'
        mock_open.side_effect = FileNotFoundError

        with pytest.raises(FileNotFoundError):
            # Call the function
            initialize(2)

        expected_chdir_calls = [
            call('..'),
            call('Dataset_Divided'),
        ]
        mock_chdir.assert_has_calls(expected_chdir_calls, any_order=False)

        mock_mkdir.assert_not_called()

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.listdir', return_value=['RepositoryMining' + str(MINI_DATASET_NAME)])
    @patch('os.getcwd')
    @patch('os.mkdir')
    @pytest.mark.parametrize('mock_chdir_fail', ['mining_results'], indirect=True)
    def test_case_ADD(self, mock_mkdir, mock_getcwd, mock_listdir, mock_open, mock_chdir_fail, setup_dir):
        # Setup mocks
        mock_getcwd.return_value = 'Dataset2/tests/RepoMining'

        # Expecting a FileNotFoundError when trying to chdir to 'mining_results'
        with pytest.raises(FileNotFoundError):
            # Call the function you're testing
            initialize(2)

        # Check that the expected calls were made to `os.chdir`
        expected_chdir_calls = [
            call('..'),
            call('Dataset_Divided'),
            call('..')
        ]

        # Assert that os.chdir was called with the expected calls
        mock_chdir_fail.assert_has_calls(expected_chdir_calls, any_order=False)

    #@pytest.mark.xfail
    @patch('Dataset2.RepoMining.repo_Mining.startMiningRepo')
    @patch('os.listdir', return_value = ['RepositoryMining' + str(MINI_DATASET_NAME)])
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.getcwd')
    @patch('os.mkdir')
    @patch('os.chdir')
    def test_case_4(self, mock_chdir, mock_mkdir, mock_getcwd, mock_open, mock_listdir, mock_start_mining, setup_dir):

        invalid_csv_content = ''';repo_url;commit_id;cls
        0,https://github.com/spring-projects/spring-webflow,57f2ccb66946943fbf3b3f2165eac1c8eb6b1523,pos
        1,https://github.com/pingidentity/ldapsdk,8471904a02438c03965d21367890276bc25fa5a6,pos,,extra_field
        2,https://github.com/apache/camel,57d01e2fc8923263df896e9810329ee5b7f9b69,pos
        3,https://github.com/jenkinsci/jenkins,d7ea3f40efedd50541a57b943d5f7bbed046d091
        4,https://github.com/apache/tomcat,2835bb4e030c1c741ed0847bb3b9c3822e4fbc8a,pos
        '''

        # Setup mocks
        mock_getcwd.return_value = 'Dataset2/tests/RepoMining/test_initialize.py'
        mock_open.read_data = invalid_csv_content


        # Call the function under test

        initialize(self.MINI_DATASET_NAME)

        expected_chdir_calls = [
            call('..'),
            call('Dataset_Divided'),
            call('..'),
            call('mining_results'),
        ]

        mock_chdir.assert_has_calls(expected_chdir_calls, any_order=False)

        mock_mkdir.assert_not_called()



    @pytest.mark.parametrize('process_data', [False], indirect=True)
    @pytest.mark.parametrize('mock_setup_repo_exist', [True], indirect=True)
    def test_case_5(self, mock_setup_repo_exist, process_data, setup_dir):
        mock_listdir, mock_cwd, mock_mkdir, mock_op, mock_chdir, mock_start, extracted_data = mock_setup_repo_exist

        # Call the function to test
        initialize('2')

        # Check if the necessary directories were created
        mock_mkdir.assert_not_called()

        expected_chdir_calls = [
            call('..'),
            call('Dataset_Divided'),
            call('..'),
            call('mining_results'),
        ]
        mock_chdir.assert_has_calls(expected_chdir_calls, any_order=False)

        # Verify that startMiningRepo was called with the correct parameters
        mock_start.assert_called_with(extracted_data, mock_cwd.return_value, 'RepositoryMining2')

    @pytest.mark.parametrize('process_data', [True], indirect=True)
    @pytest.mark.parametrize('mock_setup_repo_exist', [False], indirect=True)
    def test_case_6(self, mock_setup_repo_exist, process_data, setup_dir):
        mock_listdir, mock_cwd, mock_mkdir, mock_op, mock_chdir, mock_start, extracted_data = mock_setup_repo_exist

        # Call the function to test
        initialize('2')

        # Check if the necessary directories were created
        mock_mkdir.assert_called_with('RepositoryMining2')

        expected_chdir_calls = [
            call('..'),
            call('Dataset_Divided'),
            call('..'),
            call('mining_results'),
        ]
        mock_chdir.assert_has_calls(expected_chdir_calls, any_order=False)

        # Verify that startMiningRepo was called with the correct parameters
        mock_start.assert_called_with(extracted_data, mock_cwd.return_value, 'RepositoryMining2')

