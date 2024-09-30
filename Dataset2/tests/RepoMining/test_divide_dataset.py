import csv
import io
from unittest import mock

import pytest
from unittest.mock import patch, mock_open, call
from Dataset2.RepoMining.repo_Mining import initialize
from Dataset2.tests.RepoMining.conftest import generate_csv_string


def divide_dataset_to_test():
    import os
    '''
    Divide the entire dataset in small pieces of 50 commits.
    '''
    os.chdir("..")
    cwd = os.getcwd()
    csvfile = open('initial_Dataset.csv', 'r').readlines()
    filename = 1
    if "Dataset_Divided" not in os.listdir():
        os.mkdir("Dataset_Divided")
    os.chdir(cwd + "/Dataset_Divided")
    header = csvfile[0]

    csvfile = csvfile[1:]

    if len(csvfile)==0:
        with open(str(filename) + '.csv', 'w+') as new_file:
            new_file.writelines([header])
    else:
        for i in range(0, len(csvfile)):
            if i % 50 == 0:
                with open(str(filename) + '.csv', 'w+') as new_file:
                    new_file.write(header)
                    new_file.writelines(csvfile[i:i + 50])
                filename += 1

class TestDivideDataset:

    DATASET_NAME = 'initial_Dataset.csv'
    DATASET_HEADERS = 'cve_id,repo_url,commit_id,cls'

    DIR_NAME = 'Dataset_Divided'

    TEST_PATH = 'test/path'


    @patch('os.getcwd', return_value="test/path")
    @patch('os.chdir')
    @pytest.mark.parametrize('mock_op_fail', [DATASET_NAME], indirect=True)
    def test_case_1(self, mock_chdir, mock_getcwd, mock_op_fail):

        with pytest.raises(FileNotFoundError):
            # Call the function
            divide_dataset_to_test()



    @patch('os.getcwd', return_value=TEST_PATH)
    @patch('os.listdir', return_value=[DIR_NAME])
    @patch('os.chdir')
    @patch('os.mkdir')
    @pytest.mark.parametrize('mock_files', [
        {DATASET_NAME: generate_csv_string(0), '1.csv': None}
    ], indirect=True)
    def test_case_2(self, mock_mkdir, mock_chdir, mock_listdir, mock_getcwd, mock_files):

            divide_dataset_to_test()

            mock_mkdir.assert_not_called()
            mock_chdir.assert_called_with(self.TEST_PATH + "/" + self.DIR_NAME)

            mock_files[self.DATASET_NAME].assert_called_with(self.DATASET_NAME, 'r')

            mock_files['1.csv']().writelines.assert_called_with([self.DATASET_HEADERS + '\n'])

    # FAILURE: ONLY 1st CSV contains headers


    @patch('os.getcwd', return_value=TEST_PATH)
    @patch('os.listdir', return_value=[DIR_NAME])
    @patch('os.chdir')
    @patch('os.mkdir')
    @pytest.mark.parametrize('mock_files', [
        {DATASET_NAME: generate_csv_string(50), '1.csv': None}
    ], indirect=True)
    @pytest.mark.parametrize('mock_op_permission_err', [
        '1.csv'
    ], indirect=True)
    def test_case_3(self, mock_mkdir, mock_chdir, mock_listdir, mock_getcwd, mock_op_permission_err, mock_files):

        with pytest.raises(PermissionError):
            divide_dataset_to_test()


    # FALLIMENTO: QUANDO NON HO RECORD MI ASPETTO DIVIDE_DATASET DIR VUOTA
    # ERRORE: 1.CSV CONTIENE GLI HEADER DI INITIAL DATASET (SONO PRESENTI SOLO IN QUESTO FILE)

    @patch('os.getcwd', return_value=TEST_PATH)
    @patch('os.listdir', return_value=[])
    @patch('os.chdir')
    @patch('os.mkdir')
    @pytest.mark.parametrize('mock_files', [
        {DATASET_NAME: generate_csv_string(60), '1.csv': None, '2.csv': None}
    ], indirect=True)
    def test_case_4(self, mock_mkdir, mock_chdir, mock_listdir, mock_getcwd, mock_files):
        divide_dataset_to_test()

        mock_mkdir.assert_called_once_with(self.DIR_NAME)
        mock_chdir.assert_called_with(self.TEST_PATH + "/" + self.DIR_NAME)

        mock_files[self.DATASET_NAME].assert_called_with(self.DATASET_NAME, 'r')

        oracle_datasets = ['1.csv', '2.csv']

        oracle_data = generate_csv_string(60)

        lines = oracle_data.strip().split('\n')  # Use '\r\n' to split lines

        print("BEFORE:", lines)

        lines = [line + "\n" for line in lines[1:]]

        print("AFTER:", lines)

        lines_per_dataset = 50

        print("LUN:", len(oracle_datasets))

        for i in range(len(oracle_datasets)):
            print("START INDEX: ", i)
            start_index = i * lines_per_dataset
            end_index = start_index + lines_per_dataset
            expected_lines = lines[start_index:end_index]

            mock_files[oracle_datasets[i]]().write.assert_called_with(self.DATASET_HEADERS + '\n')
            mock_files[oracle_datasets[i]]().writelines.assert_called_with(expected_lines)









