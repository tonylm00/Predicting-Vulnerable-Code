import os

import pytest
from requests.exceptions import MissingSchema

from Dataset2.RepoMining import repo_Mining
from test_divide_dataset import divide_dataset_to_test as main_divide_dataset
from Dataset2.tests.RepoMining.conftest import generate_csv_string


def main_repo_mining():
    import os
    '''
    The main execution of repo_mining.py
    Call the function for each mini dataset.
    '''
    for count in range(1, 36, 1):
        print("Starting file:")
        print(count)
        repo_Mining.initialize(count)
        print("------------------")
        print("The file:")
        print(count)
        print(" is Ready!!!")
        print("------------------")


class TestRepoMiningIntegration:


    def execute_pipeline(self):
        main_divide_dataset()
        main_repo_mining()

    @pytest.mark.parametrize('manage_temp_input_files', [
        {},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['mining_results']
    ], indirect=True)
    def test_case_1(self, create_temp_file_sys):
        with pytest.raises(FileNotFoundError):
            self.execute_pipeline()

    @pytest.mark.parametrize('manage_temp_input_files', [
        {'initial_Dataset.csv': generate_csv_string(1, True)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results']
    ], indirect=True)
    def test_case_2(self, manage_temp_input_files, create_temp_file_sys):
        with pytest.raises(KeyError) as exc_info:
            self.execute_pipeline()

        assert "repo_url" in str(exc_info.value)

    @pytest.mark.parametrize('manage_temp_input_files', [
        {'initial_Dataset.csv': generate_csv_string(1, False, True)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['mining_results']
    ], indirect=True)
    def test_case_3(self, manage_temp_input_files, create_temp_file_sys):
        cwd = os.getcwd()

        print("OS_LIST_DIR:", os.listdir(cwd))

        with pytest.raises(MissingSchema) as exc_info:
            self.execute_pipeline()


        assert 'Invalid URL' in str(exc_info.value) and "link_not_valid" + '.git' in str(exc_info.value)

        assert os.path.exists(os.path.join(cwd, "Dataset_Divided"))






























