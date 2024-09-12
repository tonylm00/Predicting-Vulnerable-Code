import os

import pytest
from requests.exceptions import MissingSchema
from requests.exceptions import ConnectionError


from Dataset2.RepoMining import repo_Mining
from test_divide_dataset import divide_dataset_to_test as main_divide_dataset
from Dataset2.tests.RepoMining.conftest import generate_csv_string

DATASET_SIZE_0 = 0
DATASET_SIZE_TO_50 = 50
DATASET_SIZE_OVER_50 = 150


SOURCE_CODE_BEFORE_TEST = source_code_before_to_test = '''package basics;
import java.util.Arrays;

public class BinarySearch {
	
	public static void main(String[] args) {
		
		int arr[] = {10, 20, 15, 22, 35};
		Arrays.sort(arr);
		
		int key = 35;
		int res = Arrays.binarySearch(arr, key);
		if(res >= 0){
			System.out.println(key + " found at index = "+ res);
		} else {
			System.out.println(key + " not found");
		} 
	}
}
'''



def main_repo_mining():
    import os
    '''
    The main execution of repo_mining.py
    Call the function for each mini dataset.
    '''
    print("CWD-MAIN:", os.getcwd())
    dataset_divided_path = os.path.join(os.getcwd(), "Dataset_Divided")
    num_repos = len(os.listdir(dataset_divided_path))
    print(num_repos)
    for count in range(1, num_repos+1, 1):
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
        os.chdir('..')
        main_repo_mining()

    @pytest.mark.parametrize('manage_temp_input_files', [
        {},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        []
    ], indirect=True)
    def test_case_ADD(self, create_temp_file_sys):
        with pytest.raises(FileNotFoundError):
            self.execute_pipeline()

    @pytest.mark.parametrize('manage_temp_input_files', [
        {'initial_Dataset.csv': generate_csv_string(0)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['mining_results']
    ], indirect=True)
    def test_case_ADD_SIZE_ZERO(self, create_temp_file_sys):
        start_cwd = os.getcwd()

        os.chdir('..')

        dir_not_exist_before = not os.path.exists(os.path.join(os.getcwd(), "Dataset_Divided"))

        os.chdir(start_cwd)

        self.execute_pipeline()

        os.chdir(start_cwd)
        os.chdir('..')

        dir_exist_after = os.path.exists(os.path.join(os.getcwd(), "Dataset_Divided"))

        check_path = os.path.join(os.getcwd(), "mining_results", "CHECK.txt")

        error_path = os.path.join(os.getcwd(), "mining_results", "ERRORS.txt")


        assert dir_not_exist_before and dir_exist_after
        assert not os.path.exists(check_path)
        assert not os.path.exists(error_path)



    @pytest.mark.parametrize('manage_temp_input_files', [
        {'initial_Dataset.csv': generate_csv_string(1, False)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results']
    ], indirect=True)
    def test_case_2(self, manage_temp_input_files, create_temp_file_sys):
        with pytest.raises(KeyError) as exc_info:
            self.execute_pipeline()

        assert "repo_url" in str(exc_info.value)

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
        {'initial_Dataset.csv': generate_csv_string(DATASET_SIZE_TO_50, False)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results']
    ], indirect=True)
    def test_case_2(self, manage_temp_input_files, create_temp_file_sys):
        with pytest.raises(KeyError) as exc_info:
            self.execute_pipeline()

        assert "repo_url" in str(exc_info.value)

    @pytest.mark.parametrize('manage_temp_input_files', [
        {'initial_Dataset.csv': generate_csv_string(DATASET_SIZE_TO_50, True, False)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['mining_results']
    ], indirect=True)
    def test_case_3(self, manage_temp_input_files, create_temp_file_sys):
        start_cwd = os.getcwd()

        os.chdir('..')

        dir_not_exist_before = not os.path.exists(os.path.join(os.getcwd(), "Dataset_Divided"))

        os.chdir(start_cwd)

        with pytest.raises(MissingSchema) as exc_info:
            self.execute_pipeline()

        os.chdir(start_cwd)
        os.chdir('..')

        dir_exist_after = os.path.exists(os.path.join(os.getcwd(), "Dataset_Divided"))

        assert 'Invalid URL' in str(exc_info.value) and "link_not_valid" + '.git' in str(exc_info.value)

        assert dir_not_exist_before and dir_exist_after

    @pytest.mark.parametrize('manage_temp_input_files', [
        {'initial_Dataset.csv': generate_csv_string(DATASET_SIZE_TO_50, True, True, False)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results']
    ], indirect=True)
    def test_case_4(self, manage_temp_input_files, create_temp_file_sys):

        with pytest.raises(ConnectionError) as exc_info:
            self.execute_pipeline()

    @pytest.mark.parametrize('manage_temp_input_files', [
        {'initial_Dataset.csv': generate_csv_string(DATASET_SIZE_OVER_50, True, True, True, False)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results']
    ], indirect=True)
    def test_case_5(self, manage_temp_input_files, create_temp_file_sys):
        self.execute_pipeline()

        num_repos = int(DATASET_SIZE_OVER_50 // 50)+1

        for repo in range(1,num_repos):

            path_to_test = os.path.join(os.getcwd(), "RepositoryMining" + str(repo), "CHECK.txt")

            if os.path.exists(path_to_test):
                # SPECIFICARE CHECK.TXT DI QUALE REPO
                with open(path_to_test, 'r') as check_file:
                    lines = check_file.readlines()

                for line in lines:
                    assert 'https://github.com/spring-projects/not_valid' in line and 'REPO NOT AVAILABLE' in line

    @pytest.mark.parametrize('manage_temp_input_files', [
        {'initial_Dataset.csv': generate_csv_string(DATASET_SIZE_OVER_50, True, True, True, True, False)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results']
    ], indirect=True)
    def test_case_6(self, manage_temp_input_files, create_temp_file_sys):
        self.execute_pipeline()

        path_to_test_check = os.path.join(os.getcwd(), "mining_results", "RepositoryMining1", "CHECK.txt")

        # SPECIFICARE CHECK.TXT DI QUALE REPO
        with open(path_to_test_check, 'r') as check_file:
            lines = check_file.readlines()

        assert 'link repo: https://github.com/spring-projects/spring-webflow status: NOT EXIST COMMIT' in lines[0]

    @pytest.mark.parametrize('manage_temp_input_files', [
        {'initial_Dataset.csv': generate_csv_string(DATASET_SIZE_OVER_50, True, True, True, True, True, False)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results']
    ], indirect=True)
    def test_case_7(self, manage_temp_input_files, create_temp_file_sys):
        self.execute_pipeline()

        print("CWD-7: ", os.getcwd())

        path_to_test_check = os.path.join(os.getcwd(), "mining_results", "RepositoryMining1", "CHECK.txt")
        path_to_test_error = os.path.join(os.getcwd(), "mining_results", "RepositoryMining1", "ERRORS.txt")

        # SPECIFICARE CHECK.TXT DI QUALE REPO
        with open(path_to_test_check, 'r') as check_file:
            content = check_file.read()
            assert 'link repo: https://github.com/apache/poi status: VALUE ERROR! COMMIT HASH NOT EXISTS' in content
            assert 'link repo: https://github.com/apache/santuario-java status: VALUE ERROR! COMMIT HASH NOT EXISTS' in content

        with open(path_to_test_error, 'r') as error_file:
            content = error_file.read()
            report_str = 'indice: 1 link repo: https://github.com/apache/poi status: VALUE ERROR! COMMIT HASH NOT EXISTS\n' \
                         ',d72bd78c19dfb7b57395a66ae8d9269d59a87bd2indice: 2 link repo: https://github.com/apache/santuario-java ' \
                         'status: VALUE ERROR! COMMIT HASH NOT EXISTS\n,a09b9042f7759d094f2d49f40fc7bcf145164b25'

            assert report_str == content

    @pytest.mark.parametrize('manage_temp_input_files', [
        {'initial_Dataset.csv': generate_csv_string(DATASET_SIZE_OVER_50, True, True, True, True, True, True, True, True, False, True)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results']
    ], indirect=True)
    def test_case_8(self, manage_temp_input_files, create_temp_file_sys):
        self.execute_pipeline()

        path_to_repo_mining = os.path.join(os.getcwd(), "mining_results", "RepositoryMining1")
        path_to_test_check = os.path.join(path_to_repo_mining, "CHECK.txt")
        path_to_test_error = os.path.join(path_to_repo_mining, "ERRORS.txt")

        with open(path_to_test_check, 'r') as check_file:
            lines = check_file.readlines()

        assert 'link repo: https://github.com/apache/flink status: GIT COMMAND ERROR' in lines[0]

        with open(path_to_test_error, 'r') as error_file:
            content = error_file.read()
            report_str = 'indice: 1 link repo: https://github.com/apache/flink status: GIT COMMAND ERROR\n' \
                         ',d9931c8af05d0f1f721be9fe920690fe122507ad'

            assert report_str == content

    @pytest.mark.parametrize('manage_temp_input_files', [
        {'initial_Dataset.csv': generate_csv_string(DATASET_SIZE_OVER_50, True, True, True, True, True, True, False)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results']
    ], indirect=True)
    def test_case_9(self, manage_temp_input_files, create_temp_file_sys):
        self.execute_pipeline()

        path_to_repo_mining = os.path.join(os.getcwd(), "mining_results", "RepositoryMining1")
        path_to_test_check = os.path.join(path_to_repo_mining, "CHECK.txt")
        path_to_test_error = os.path.join(path_to_repo_mining, "ERRORS.txt")

        with open(path_to_test_check, 'r') as check_file:
            lines = check_file.readlines()

        assert 'link repo: https://github.com/bahmutov/test-make-empty-github-commit status: OK!' in lines[0]

        with open(path_to_test_error, 'r') as error_file:
            content = error_file.read()
            assert len(content)==0

        assert os.listdir(path_to_repo_mining) == ['CHECK.txt', 'ERRORS.txt']

    @pytest.mark.parametrize('manage_temp_input_files', [
        {'initial_Dataset.csv': generate_csv_string(DATASET_SIZE_OVER_50, True, True, True, True, True, True, True, False)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results']
    ], indirect=True)
    def test_case_10(self, manage_temp_input_files, create_temp_file_sys):
        self.execute_pipeline()

        path_to_repo_mining = os.path.join(os.getcwd(), "mining_results", "RepositoryMining1")
        path_to_test_check = os.path.join(path_to_repo_mining, "CHECK.txt")
        path_to_test_error = os.path.join(path_to_repo_mining, "ERRORS.txt")

        with open(path_to_test_check, 'r') as check_file:
            lines = check_file.readlines()

        assert 'link repo: https://github.com/vi3k6i5/pandas_basics status: OK!' in lines[0]

        with open(path_to_test_error, 'r') as error_file:
            content = error_file.read()
            assert len(content) == 0

        assert os.listdir(path_to_repo_mining) == ['CHECK.txt', 'ERRORS.txt']

    @pytest.mark.parametrize('manage_temp_input_files', [
        {'initial_Dataset.csv': generate_csv_string(DATASET_SIZE_OVER_50, True, True, True, True, True, True, True, True)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results']
    ], indirect=True)
    def test_case_11(self, manage_temp_input_files, create_temp_file_sys):
        self.execute_pipeline()

        path_to_repo_mining = os.path.join(os.getcwd(), "mining_results", "RepositoryMining1")
        path_to_test_check = os.path.join(path_to_repo_mining, "CHECK.txt")
        path_to_test_error = os.path.join(path_to_repo_mining, "ERRORS.txt")


        with open(path_to_test_check, 'r') as check_file:
            lines = check_file.readlines()

        assert 'link repo: https://github.com/winterbe/java8-tutorial status: OK!' in lines[0]

        with open(path_to_test_error, 'r') as error_file:
            content = error_file.read()
            assert len(content) == 0

        path_to_repo_mining_id = os.path.join(path_to_repo_mining, str(0))
        path_to_repo_mining_commit = os.path.join(path_to_repo_mining_id,"81a0fa3aa1d6ec2409e0226d3a6c2f5c2d19a41d")

        assert str(0) in os.listdir(path_to_repo_mining)
        assert '81a0fa3aa1d6ec2409e0226d3a6c2f5c2d19a41d' in os.listdir(path_to_repo_mining_id)
        assert len(os.listdir(path_to_repo_mining_commit))==0



    @pytest.mark.parametrize('manage_temp_input_files', [
        {'initial_Dataset.csv': generate_csv_string(DATASET_SIZE_TO_50, True, True, True, True, True, True, True, True, False)},
    ], indirect=True)
    @pytest.mark.parametrize('create_temp_file_sys', [
        ['Dataset_Divided', 'mining_results']
    ], indirect=True)
    def test_case_12(self, manage_temp_input_files, create_temp_file_sys):
        self.execute_pipeline()

        path_to_repo_mining = os.path.join(os.getcwd(), "mining_results", "RepositoryMining1")
        path_to_test_check = os.path.join(path_to_repo_mining, "CHECK.txt")
        path_to_test_error = os.path.join(path_to_repo_mining, "ERRORS.txt")

        with open(path_to_test_check, 'r') as check_file:
            lines = check_file.readlines()

        assert 'link repo: https://github.com/learning-zone/java-basics status: OK!' in lines[0]

        with open(path_to_test_error, 'r') as error_file:
            content = error_file.read()
            assert len(content) == 0

        path_to_repo_mining_id = os.path.join(path_to_repo_mining, str(0))
        path_to_repo_mining_commit = os.path.join(path_to_repo_mining_id,"8ab4deb1030b4d863f8d8048b892d34f18dfaebe")
        path_to_file_mod = os.path.join(path_to_repo_mining_commit, "BinarySearch.java")

        with open(path_to_file_mod, 'r') as mod_file:
            content = mod_file.read()


        assert str(0) in os.listdir(path_to_repo_mining)
        assert '8ab4deb1030b4d863f8d8048b892d34f18dfaebe' in os.listdir(path_to_repo_mining_id)
        assert 'BinarySearch.java' in os.listdir(path_to_repo_mining_commit)
        assert SOURCE_CODE_BEFORE_TEST == content






































