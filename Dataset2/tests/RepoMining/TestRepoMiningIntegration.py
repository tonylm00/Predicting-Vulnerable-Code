import logging
import os
import time

import pytest
from requests.exceptions import MissingSchema
from requests.exceptions import ConnectionError
import requests_cache

from Dataset2.Main import Main
from Dataset2.tests.RepoMining.conftest import generate_csv_string


class TestRepoMiningIntegration:
    DATASET_SIZE_0 = 0
    DATASET_SIZE_TO_50 = 50
    DATASET_SIZE_OVER_50 = 150

    SOURCE_CODE_BEFORE_TEST = source_code_before_to_test = \
         'package basics;\n'\
         'import java.util.Arrays;\n'\
         '\n'\
         'public class BinarySearch {\n'\
         '\t\n'\
         '\tpublic static void main(String[] args) {\n'\
         '\t\t\n'\
         '\t\tint arr[] = {10, 20, 15, 22, 35};\n'\
         '\t\tArrays.sort(arr);\n'\
         '\t\t\n'\
         '\t\tint key = 35;\n'\
         '\t\tint res = Arrays.binarySearch(arr, key);\n'\
         '\t\tif(res >= 0){\n'\
         '\t\t\tSystem.out.println(key + " found at index = "+ res);\n'\
         '\t\t} else {\n'\
         '\t\t\tSystem.out.println(key + " not found");\n'\
         '\t\t} \n'\
         '\t}\n'\
         '}\n'\

    DATASET_NAME = 'test_dataset.csv'

    @pytest.fixture(autouse=True)
    def setup(self):
        base_dir = os.getcwd()
        self.mining_path = os.path.join(base_dir, 'mining_results')
        self.data_path = os.path.join(base_dir, 'Dataset_Divided')
        self.main = Main(base_dir)
        self.log_path = os.path.join(self.mining_path, 'repo_mining.log')

    def test_case_1(self):

        with pytest.raises(FileNotFoundError):
            self.main.run_repo_mining(self.DATASET_NAME)

    @pytest.mark.parametrize('manage_temp_input_files', [
        {DATASET_NAME: generate_csv_string(DATASET_SIZE_OVER_50, True, True, True, False)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided']
    ], indirect=True)
    def test_case_2(self, manage_temp_input_files):
        requests_cache.clear()

        not_exist_mining = not os.path.exists(self.mining_path)

        self.main.run_repo_mining(self.DATASET_NAME)

        with open(self.log_path, 'r') as check_file:
            lines = check_file.readlines()

        assert len(lines) == self.DATASET_SIZE_OVER_50

        for line in lines:
            assert 'https://github.com/spring-projects/not_valid' in line and 'REPO NOT AVAILABLE' in line

        assert not_exist_mining
        assert os.path.exists(self.mining_path)

        logging.shutdown()

    @pytest.mark.parametrize('manage_temp_input_files', [
        {DATASET_NAME: generate_csv_string(DATASET_SIZE_TO_50, False)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results']
    ], indirect=True)
    def test_case_3(self, manage_temp_input_files):
        with pytest.raises(ValueError) as exc_info:
            self.main.run_repo_mining(self.DATASET_NAME)

        assert "Not valid dataset headers" in str(exc_info.value)

    @pytest.mark.parametrize('manage_temp_input_files', [
        {DATASET_NAME: generate_csv_string(0)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['mining_results']
    ], indirect=True)
    def test_case_4(self, manage_temp_input_files):

        not_exist_data = not os.path.exists(self.data_path)

        self.main.run_repo_mining(self.DATASET_NAME)

        assert len(os.listdir(self.mining_path)) == 2
        assert '1.csv' in os.listdir(self.data_path)

        with open(os.path.join(self.data_path, '1.csv')) as file:
            lines = file.readlines()

        assert lines == ['cve_id,repo_url,commit_id\n']
        assert not_exist_data
        assert os.path.exists(self.data_path)

    @pytest.mark.parametrize('manage_temp_input_files', [
        {DATASET_NAME: generate_csv_string(DATASET_SIZE_TO_50, True, False), },
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results'],
    ], indirect=True)
    def test_case_5(self, manage_temp_input_files):

        with pytest.raises(MissingSchema) as exc_info:
            self.main.run_repo_mining(self.DATASET_NAME)

        assert 'Invalid URL' in str(exc_info.value) and "link_not_valid" + '.git' in str(exc_info.value)

    @pytest.mark.parametrize('manage_temp_input_files', [
        {DATASET_NAME: generate_csv_string(DATASET_SIZE_TO_50, True, True, False)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results']
    ], indirect=True)
    def test_case_6(self, manage_temp_input_files):
        with pytest.raises(ConnectionError) as exc_info:
            self.main.run_repo_mining(self.DATASET_NAME)

    @pytest.mark.parametrize('manage_temp_input_files', [
        {DATASET_NAME: generate_csv_string(DATASET_SIZE_OVER_50, True, True, True, False)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results']
    ], indirect=True)
    def test_case_7(self, manage_temp_input_files):
        requests_cache.clear()
        self.main.run_repo_mining(self.DATASET_NAME)

        with open(self.log_path, 'r') as check_file:
                lines = check_file.readlines()

        assert len(lines) == self.DATASET_SIZE_OVER_50

        for line in lines:
            assert 'https://github.com/spring-projects/not_valid' in line and 'REPO NOT AVAILABLE' in line

        logging.shutdown()

    @pytest.mark.parametrize('manage_temp_input_files', [
        {DATASET_NAME: generate_csv_string(DATASET_SIZE_TO_50, True, True, True, True, is_commit_existent=False)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results']
    ], indirect=True)
    def test_case_8(self, manage_temp_input_files):
        requests_cache.clear()

        with open(self.DATASET_NAME, 'r') as data:
            lines = data.readlines()

        print("LINES:", lines)

        self.main.run_repo_mining(self.DATASET_NAME)

        with open(self.log_path, 'r') as check_file:
            lines = check_file.readlines()

        assert 'ERROR:indice: 1 link repo: https://github.com/pingidentity/ldapsdk status: NOT EXIST COMMIT\n' == lines[0]

        logging.shutdown()

    @pytest.mark.parametrize('manage_temp_input_files', [
        {
            DATASET_NAME: generate_csv_string(DATASET_SIZE_TO_50, True, True, True, True, True, False),
            os.path.join(os.getcwd(), 'mining_results', 'repo_mining.log'): 'ERROR: already present\n'
         }
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results']
    ], indirect=True)
    def test_case_9(self, manage_temp_input_files):
        requests_cache.clear()
        self.main.run_repo_mining(self.DATASET_NAME)

        with open(self.log_path, 'r') as check_file:
            lines = check_file.readlines()

        assert 'ERROR: already present\n' == lines[0]
        assert 'ERROR:indice: 1 link repo: https://github.com/apache/poi status: VALUE ERROR! COMMIT HASH NOT EXISTS,' \
               'd72bd78c19dfb7b57395a66ae8d9269d59a87bd2\n' == lines[1]
        assert 'ERROR:indice: 2 link repo: https://github.com/apache/santuario-java status: VALUE ERROR! COMMIT HASH NOT EXISTS,' \
               'a09b9042f7759d094f2d49f40fc7bcf145164b25\n' == lines[2]


        logging.shutdown()

    @pytest.mark.parametrize('manage_temp_input_files', [
        {DATASET_NAME: generate_csv_string(DATASET_SIZE_TO_50, True, True, True, True, True, True, True, True,
                                                    False, True)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results']
    ], indirect=True)
    def test_case_10(self, manage_temp_input_files):
        requests_cache.clear()
        self.main.run_repo_mining(self.DATASET_NAME)

        with open(self.log_path, 'r') as check_file:
            lines = check_file.readlines()

        assert 'ERROR:indice: 1 link repo: https://github.com/apache/flink status: GIT COMMAND ERROR,' \
               'd9931c8af05d0f1f721be9fe920690fe122507ad\n' == lines[0]

        logging.shutdown()

    @pytest.mark.parametrize('manage_temp_input_files', [
        {DATASET_NAME: generate_csv_string(DATASET_SIZE_TO_50, True, True, True, True, True, True, False)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results']
    ], indirect=True)
    def test_case_11(self, manage_temp_input_files):
        requests_cache.clear()

        self.main.run_repo_mining(self.DATASET_NAME)

        with open(self.log_path, 'r') as check_file:
            lines = check_file.readlines()

        assert 'INFO:indice: 1 link repo: https://github.com/bahmutov/test-make-empty-github-commit status: OK!\n' == lines[0]

        logging.shutdown()


    @pytest.mark.parametrize('manage_temp_input_files', [
        {DATASET_NAME: generate_csv_string(DATASET_SIZE_TO_50, True, True, True, True, True, True, True,
                                                    False)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results']
    ], indirect=True)
    def test_case_12(self, manage_temp_input_files):
        requests_cache.clear()

        self.main.run_repo_mining(self.DATASET_NAME)

        with open(self.log_path, 'r') as check_file:
            lines = check_file.readlines()

        assert 'INFO:indice: 1 link repo: https://github.com/vi3k6i5/pandas_basics status: OK!\n' == lines[0]

        logging.shutdown()

    @pytest.mark.parametrize('manage_temp_input_files', [
        {DATASET_NAME: generate_csv_string(DATASET_SIZE_TO_50, True, True, True, True, True, True, True,
                                                    True)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results']
    ], indirect=True)
    def test_case_13(self, manage_temp_input_files):
        requests_cache.clear()

        path_to_repo = os.path.join(self.mining_path, 'RepositoryMining1')
        path_to_id = os.path.join(path_to_repo, str(0))
        path_to_commit = os.path.join(path_to_id, "81a0fa3aa1d6ec2409e0226d3a6c2f5c2d19a41d")

        not_exist_id_dir = not os.path.exists(path_to_id)
        not_exist_commit_dir = not os.path.exists(path_to_commit)

        self.main.run_repo_mining(self.DATASET_NAME)

        with open(self.log_path, 'r') as check_file:
            lines = check_file.readlines()

        assert 'INFO:indice: 1 link repo: https://github.com/winterbe/java8-tutorial status: OK!\n' == lines[0]

        path_to_repo = os.path.join(self.mining_path, 'RepositoryMining1')
        path_to_id = os.path.join(path_to_repo, str(0))
        path_to_commit = os.path.join(path_to_id, "81a0fa3aa1d6ec2409e0226d3a6c2f5c2d19a41d")


        assert not_exist_id_dir
        assert not_exist_commit_dir
        assert os.path.exists(path_to_id)
        assert os.path.exists(path_to_commit)
        assert len(os.listdir(path_to_commit)) == 0

        logging.shutdown()


    @pytest.mark.parametrize('manage_temp_input_files', [
        {DATASET_NAME: generate_csv_string(DATASET_SIZE_TO_50, True, True, True, True, True, True, True, True,
                                                    False)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results']
    ], indirect=True)
    def test_case_14(self, manage_temp_input_files):
        requests_cache.clear()

        path_to_repo = os.path.join(self.mining_path, 'RepositoryMining1')
        path_to_id = os.path.join(path_to_repo, str(0))
        path_to_commit = os.path.join(path_to_id, "8ab4deb1030b4d863f8d8048b892d34f18dfaebe")

        not_exist_id_dir = not os.path.exists(path_to_id)
        not_exist_commit_dir = not os.path.exists(path_to_commit)

        self.main.run_repo_mining(self.DATASET_NAME)


        with open(self.log_path, 'r') as check_file:
            lines = check_file.readlines()

        assert 'INFO:indice: 1 link repo: https://github.com/learning-zone/java-basics status: OK!\n' == lines[0]


        path_to_file_mod = os.path.join(path_to_commit, "BinarySearch.java")

        with open(path_to_file_mod, 'r') as mod_file:
            content = mod_file.read()

        assert not_exist_id_dir
        assert not_exist_commit_dir
        assert os.path.exists(path_to_id)
        assert os.path.exists(path_to_commit)
        assert 'BinarySearch.java' in os.listdir(path_to_commit)
        assert self.SOURCE_CODE_BEFORE_TEST == content

        logging.shutdown()

    def test_case15(self):
        main = Main(3)

        with pytest.raises(TypeError):
            main.run_repo_mining(self.DATASET_NAME)

    def test_case16(self):
        main = Main('test/path<<2?')

        with pytest.raises(OSError):
            main.run_repo_mining(self.DATASET_NAME)

    def test_case17(self):
        main = Main('test/path')

        with pytest.raises(FileNotFoundError):
            main.run_repo_mining(self.DATASET_NAME)







