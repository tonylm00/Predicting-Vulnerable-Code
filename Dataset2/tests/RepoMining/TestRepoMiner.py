import csv
import io
import logging
import os
from unittest import mock
from urllib.parse import urlparse

import pytest
from unittest.mock import patch, mock_open, call, MagicMock

from git import GitCommandError
from requests.exceptions import MissingSchema
from requests.exceptions import ConnectionError


from Dataset2.RepoMining.RepoMiner import RepoMiner
from Dataset2.tests.RepoMining.conftest import custom_analyze_side_effect, custom_dir_side_effect, path_valid


class TestRepoMiner:

    class TestInitialize:

        MINI_DATASET_NAME = 2
        BASE_DIR = 'test/path'
        BASE_DIR_ERROR = 'test/non-exist-path'
        DATA_DIR_PATH = BASE_DIR + '/' + 'Dataset_Divided'
        MINING_DIR_PATH = BASE_DIR + '/' + 'mining_results'
        FILE_PATH = DATA_DIR_PATH + '/' + str(MINI_DATASET_NAME) + '.csv'
        FILE_ERROR_PATH = BASE_DIR_ERROR + '/' + 'Dataset_Divided' + '/' + str(MINI_DATASET_NAME) + '.csv'
        REPO_PATH = MINING_DIR_PATH + '/' + 'RepositoryMining' + str(MINI_DATASET_NAME)
        INVALID_CONTENT = ''';repo_url;commit_id;cls
                    0,https://github.com/spring-projects/spring-webflow,57f2ccb66946943fbf3b3f2165eac1c8eb6b1523,pos
                    1,https://github.com/pingidentity/ldapsdk,8471904a02438c03965d21367890276bc25fa5a6,pos,,extra_field
                    2,https://github.com/apache/camel,57d01e2fc8923263df896e9810329ee5b7f9b69,pos
                    3,https://github.com/jenkinsci/jenkins,d7ea3f40efedd50541a57b943d5f7bbed046d091
                    4,https://github.com/apache/tomcat,2835bb4e030c1c741ed0847bb3b9c3822e4fbc8a,pos
                    '''


        @pytest.mark.parametrize('mock_op_fail', [None], indirect=True)
        @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
        def test_case_1(self, mock_join, mock_op_fail):
            miner = RepoMiner(self.BASE_DIR)

            with pytest.raises(OSError):
                miner.initialize_repo_mining('3<ddd-tc.txt')


        @pytest.mark.parametrize('mock_op_fail', [FILE_PATH], indirect=True)
        @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
        def test_case_2(self, mock_join, mock_op_fail):

            miner = RepoMiner(self.BASE_DIR)

            with pytest.raises(FileNotFoundError):
                miner.initialize_repo_mining(self.MINI_DATASET_NAME)

        @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
        @patch('os.makedirs')
        @patch('os.mkdir')
        @pytest.mark.parametrize('process_data', [3], indirect=True)
        @pytest.mark.parametrize('mock_os_path_exists', [
            {MINING_DIR_PATH: False, REPO_PATH: True}
        ], indirect=True)
        def test_case_3(self, mock_mkdir, mock_makedirs, mock_join, mock_os_path_exists, mock_data_to_mine):
            mock_op, mock_start, extracted_data = mock_data_to_mine

            miner = RepoMiner(self.BASE_DIR)
            miner.initialize_repo_mining(self.MINI_DATASET_NAME)

            mock_makedirs.assert_called_once_with(self.MINING_DIR_PATH, exist_ok=True)

            mock_mkdir.assert_has_calls([], any_order=True)

            mock_op.assert_called_once_with(self.FILE_PATH, mode='r')

            # Verify that startMiningRepo was called with the correct parameters
            mock_start.assert_called_once_with(extracted_data, self.REPO_PATH)

        @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
        @patch('os.path.exists', return_value=False)
        @patch('os.makedirs')
        @pytest.mark.parametrize('mock_files', [
            {FILE_PATH: INVALID_CONTENT}
        ], indirect=True)
        def test_case_4(self, mock_makedirs, mock_exists, mock_join, mock_files):

            miner = RepoMiner(self.BASE_DIR)

            with pytest.raises(ValueError):
                miner.initialize_repo_mining(self.MINI_DATASET_NAME)

            mock_makedirs.assert_called_once_with(self.MINING_DIR_PATH, exist_ok=True)

            mock_files[self.FILE_PATH].assert_called_once_with(self.FILE_PATH, 'r')

        @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
        @patch('os.makedirs')
        @patch('os.mkdir')
        @pytest.mark.parametrize('process_data', [3], indirect=True)
        @pytest.mark.parametrize('mock_os_path_exists', [
            {MINING_DIR_PATH: True, REPO_PATH: True}
        ], indirect=True)
        def test_case_5(self, mock_mkdir, mock_makedirs, mock_join, mock_os_path_exists, mock_data_to_mine):
            mock_op, mock_start, extracted_data = mock_data_to_mine

            miner = RepoMiner(self.BASE_DIR)
            miner.initialize_repo_mining(self.MINI_DATASET_NAME)

            mock_makedirs.assert_called_once_with(self.MINING_DIR_PATH, exist_ok=True)

            mock_mkdir.assert_has_calls([], any_order=True)

            mock_op.assert_called_once_with(self.FILE_PATH, mode='r')

            # Verify that startMiningRepo was called with the correct parameters
            mock_start.assert_called_once_with(extracted_data, self.REPO_PATH)

        # Test case without `mock_files`
        @patch('os.path.join', side_effect=lambda *args: '/'.join(args))  # Mock os.path.join
        @patch('os.makedirs')  # Mock os.makedirs
        @patch('os.mkdir')  # Mock os.mkdir
        @pytest.mark.parametrize('process_data', [0], indirect=True)  # Indirect parameterized fixture
        @pytest.mark.parametrize('mock_os_path_exists', [
            {MINING_DIR_PATH: True, REPO_PATH: False}  # Path existence settings
        ], indirect=True)
        def test_case_6(self, mock_mkdir, mock_makedirs, mock_join, mock_os_path_exists,
                        mock_data_to_mine):
            mock_op, mock_start, extracted_data = mock_data_to_mine

            miner = RepoMiner(self.BASE_DIR)
            miner.initialize_repo_mining(self.MINI_DATASET_NAME)

            mock_makedirs.assert_called_once_with(self.MINING_DIR_PATH, exist_ok=True)
            mock_mkdir.assert_called_once_with(self.REPO_PATH)

            mock_op.assert_called_once_with(self.FILE_PATH, mode='r')

            # Verify that startMiningRepo was called with the correct parameters
            mock_start.assert_called_once_with(extracted_data, self.REPO_PATH)

        # Test case without `mock_files`
        @patch('os.path.join', side_effect=lambda *args: '/'.join(args))  # Mock os.path.join
        @patch('os.makedirs')  # Mock os.makedirs
        @patch('os.mkdir')  # Mock os.mkdir
        @pytest.mark.parametrize('process_data', [0], indirect=True)  # Indirect parameterized fixture
        @pytest.mark.parametrize('mock_os_path_exists', [
            {MINING_DIR_PATH: True, REPO_PATH: True}  # Path existence settings
        ], indirect=True)
        def test_case_7(self, mock_mkdir, mock_makedirs, mock_join, mock_os_path_exists,
                        mock_data_to_mine):
            mock_op, mock_start, extracted_data = mock_data_to_mine

            miner = RepoMiner(self.BASE_DIR)
            miner.initialize_repo_mining(self.MINI_DATASET_NAME)

            mock_makedirs.assert_called_once_with(self.MINING_DIR_PATH, exist_ok=True)
            mock_mkdir.assert_not_called()

            mock_op.assert_called_once_with(self.FILE_PATH, mode='r')

            # Verify that startMiningRepo was called with the correct parameters
            mock_start.assert_called_once_with(extracted_data, self.REPO_PATH)

        # Test case without `mock_files`
        @patch('os.path.join', side_effect=lambda *args: '/'.join(args))  # Mock os.path.join
        @patch('os.makedirs')  # Mock os.makedirs
        @patch('os.mkdir')  # Mock os.mkdir
        @pytest.mark.parametrize('process_data', [1], indirect=True)  # Indirect parameterized fixture
        @pytest.mark.parametrize('mock_os_path_exists', [
            {MINING_DIR_PATH: True, REPO_PATH: True}  # Path existence settings
        ], indirect=True)
        def test_case_8(self, mock_mkdir, mock_makedirs, mock_join, mock_os_path_exists,
                        mock_data_to_mine):
            mock_op, mock_start, extracted_data = mock_data_to_mine

            miner = RepoMiner(self.BASE_DIR)
            miner.initialize_repo_mining(self.MINI_DATASET_NAME)


            mock_makedirs.assert_called_once_with(self.MINING_DIR_PATH, exist_ok=True)
            mock_mkdir.assert_not_called()

            mock_op.assert_called_with(self.FILE_PATH, mode='r')

            # Verify that startMiningRepo was called with the correct parameters
            mock_start.assert_called_with(extracted_data, self.REPO_PATH)

        @pytest.mark.parametrize('mock_op_fail', [None], indirect=True)
        @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
        def test_case_9(self, mock_join, mock_op_fail):
            miner = RepoMiner("test/path<-4c")

            with pytest.raises(OSError):
                miner.initialize_repo_mining(self.MINI_DATASET_NAME)

        @pytest.mark.parametrize('mock_op_fail', [FILE_ERROR_PATH], indirect=True)
        @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
        def test_case_10(self, mock_join, mock_op_fail):
            miner = RepoMiner(self.BASE_DIR_ERROR)

            with pytest.raises(FileNotFoundError):
                miner.initialize_repo_mining(self.MINI_DATASET_NAME)

    class TestStartMiningRepo:
        BASE_DIR = 'test/path'
        MINING_DIR_PATH = BASE_DIR + '/' + 'mining_results'
        REPO_PATH = MINING_DIR_PATH + '/' + 'RepositoryMining1'

        @patch('logging.getLogger')
        @patch('logging.basicConfig')
        def test_case_1(self, mock_config, mock_logger):
            # content missing cve_id key

            data = dict()

            miner = RepoMiner(self.BASE_DIR)
            miner.start_mining_repo(data, self.REPO_PATH)  # Function that triggers the file operation

            mock_logger().info.assert_not_called()
            mock_logger().error.assert_not_called()

        @patch('logging.getLogger')
        @patch('logging.basicConfig')
        def test_case_2(self, mock_config, mock_logger):
            # content missing cve_id key
            content = {
                'repo_url': 'https://github.com/spring-projects/spring-webflow',
                'commit_id': '57f2ccb66946943fbf3b3f2165eac1c8eb6b1523'
            }

            data = dict()
            data[0] = content

            miner = RepoMiner(self.BASE_DIR)
            with pytest.raises(KeyError) as exc_info:
                miner.start_mining_repo(data, self.REPO_PATH)

            assert 'cve_id' in str(exc_info.value)

            mock_logger().info.assert_not_called()
            mock_logger().error.assert_not_called()

        # WHEN THE LINK IS NOT VALID, I GOT MISSINGSCHEMA
        @patch('logging.getLogger')
        @patch('logging.basicConfig')
        @pytest.mark.parametrize('mock_requests_get', [(False, False, False, False)], indirect=True)
        def test_case_3(self, mock_config, mock_logger, mock_requests_get):
            invalid_url = 'not_url'

            content_1 = {
                'cve_id': '1',
                'repo_url': invalid_url,
                'commit_id': '57f2ccb66946943fbf3b3f2165eac1c8eb6b1523'
            }

            content_2 = {
                'cve_id': '2',
                'repo_url': invalid_url,
                'commit_id': '57f2ccb66946943fbf3b3f2165eac1c8eb6b1523'
            }

            data = {0: content_1, 1:content_2}

            miner = RepoMiner(self.BASE_DIR)

            with pytest.raises(MissingSchema) as exc_info:
                miner.start_mining_repo(data, self.REPO_PATH)

            assert 'Invalid URL' in str(exc_info.value) and invalid_url + '.git' in str(exc_info.value)

            mock_config.assert_called_once_with(
                filename=os.path.join(miner.mining_result_path, 'repo_mining.log'),
                level=logging.CRITICAL,
                format='%(levelname)s:%(message)s'
            )

        @patch('logging.getLogger')
        @patch('logging.basicConfig')
        @pytest.mark.parametrize('mock_requests_get', [(True, False, False, False)], indirect=True)
        def test_case_4(self, mock_config, mock_logger, mock_requests_get):
            url_link_not_exist = 'https://github'

            content_1 = {
                'cve_id': '1',
                'repo_url': url_link_not_exist,
                'commit_id': '57f2ccb66946943fbf3b3f2165eac1c8eb6b1523'
            }

            content_2 = {
                'cve_id': '2',
                'repo_url': url_link_not_exist,
                'commit_id': '57f2ccb66946943fbf3b3f2165eac1c8eb6b1523'
            }

            data = {0: content_1, 1:content_2}

            miner = RepoMiner(self.BASE_DIR)

            with pytest.raises(ConnectionError) as exc_info:
                miner.start_mining_repo(data, self.REPO_PATH)

            parsed_url = urlparse(url_link_not_exist)
            host_with_port = parsed_url.netloc
            host = host_with_port.split(':')[0]

            assert 'ConnectionError' in str(exc_info) and host in str(exc_info.value)

        @patch('logging.getLogger')
        @patch('logging.basicConfig')
        @pytest.mark.parametrize('mock_requests_get', [(True, True, False, False)], indirect=True)
        def test_case_5(self, mock_config, mock_logger, mock_requests_get):

            url_repo_not_exist_1 = 'https://github.com/repo_not_found_1'
            url_repo_not_exist_2 = 'https://github.com/repo_not_found_2'

            content_1 = {
                'cve_id': '1',
                'repo_url': url_repo_not_exist_1,
                'commit_id': '57f2ccb66946943fbf3b3f2165eac1c8eb6b1523'
            }

            content_2 = {
                'cve_id': '2',
                'repo_url': url_repo_not_exist_2,
                'commit_id': '57f2ccb66946943fbf3b3f2165eac1c8eb6b1523'
            }

            data = {0: content_1, 1:content_2}

            miner = RepoMiner(self.BASE_DIR)
            miner.start_mining_repo(data, self.REPO_PATH)

            statusNR = "REPO NOT AVAILABLE\n"
            str_log_1 = f"indice: 1 link repo: {content_1['repo_url']} status: {statusNR}"
            str_log_2 = f"indice: 2 link repo: {content_2['repo_url']} status: {statusNR}"

            assert mock_requests_get.call_count == 2
            expected_request_calls = [call(url_repo_not_exist_1 + ".git"), call(url_repo_not_exist_2 + ".git")]
            mock_requests_get.assert_has_calls(expected_request_calls, any_order=False)

            assert mock_logger().error.call_count == 2
            expected_logger_calls = [call(str_log_1), call(str_log_2)]
            mock_logger().error.assert_has_calls(expected_logger_calls)

        @patch('logging.getLogger')
        @patch('logging.basicConfig')
        @pytest.mark.parametrize('mock_requests_get', [(True, True, True, False)], indirect=True)
        def test_case_6(self, mock_config, mock_logger, mock_requests_get):
            url_repo_exist = 'https://github.com/spring-projects/spring-webflow'
            commit_not_exist_1 = '1200fh3'
            commit_not_exist_2 = '1200fh3'

            content_1 = {
                'cve_id': '1',
                'repo_url': url_repo_exist,
                'commit_id': commit_not_exist_1
            }

            content_2 = {
                'cve_id': '2',
                'repo_url': url_repo_exist,
                'commit_id': commit_not_exist_2
            }

            data = {0: content_1, 1:content_2}

            miner = RepoMiner(self.BASE_DIR)
            miner.start_mining_repo(data, self.REPO_PATH)

            statusNE = "NOT EXIST COMMIT\n"
            str_log_1= f"indice: 1 link repo: {content_1['repo_url']} status: {statusNE}"
            str_log_2 = f"indice: 2 link repo: {content_2['repo_url']} status: {statusNE}"

            assert mock_requests_get.call_count == 4
            mock_requests_get.assert_has_calls([
                call(url_repo_exist + ".git"),
                call(url_repo_exist + "/commit/" + commit_not_exist_1),
                call(url_repo_exist + ".git"),
                call(url_repo_exist + "/commit/" + commit_not_exist_1)
            ])

            assert mock_logger().error.call_count == 2
            expected_logger_calls = [call(str_log_1), call(str_log_2)]
            mock_logger().error.assert_has_calls(expected_logger_calls)

        @patch('logging.getLogger')
        @patch('logging.basicConfig')
        @pytest.mark.parametrize('mock_requests_get', [(True, True, True, True)], indirect=True)
        @pytest.mark.parametrize('mock_repo_mining', [(False, False, False, False)], indirect=True)
        def test_case_7(self, mock_config, mock_logger, mock_requests_get, mock_repo_mining):
            mock_repo_mining, mock_commit = mock_repo_mining
            url_repo_exist_1 = 'https://github.com/apache/poi'
            commit_exist_1 = 'd72bd78c19dfb7b57395a66ae8d9269d59a87bd2'

            url_repo_exist_2 = 'https://github.com/apache/santuario-java'
            commit_exist_2 = 'a09b9042f7759d094f2d49f40fc7bcf145164b25'

            content_1 = {
                'cve_id': '1',
                'repo_url': url_repo_exist_1,
                'commit_id': commit_exist_1
            }

            content_2 = {
                'cve_id': '2',
                'repo_url': url_repo_exist_2,
                'commit_id': commit_exist_2
            }

            data = {0: content_1, 1:content_2}

            miner = RepoMiner(self.BASE_DIR)
            miner.start_mining_repo(data, self.REPO_PATH)

            statusVE = "VALUE ERROR! COMMIT HASH NOT EXISTS"
            str_log_1 = f"indice: 1 link repo: {content_1['repo_url']} status: " + statusVE + "," + commit_exist_1
            str_log_2 = f"indice: 2 link repo: {content_2['repo_url']} status: " + statusVE + "," + commit_exist_2

            assert mock_requests_get.call_count == 4
            mock_requests_get.assert_has_calls([
                call(url_repo_exist_1 + ".git"),
                call(url_repo_exist_1 + "/commit/" + commit_exist_1),
                call(url_repo_exist_2 + ".git"),
                call(url_repo_exist_2 + "/commit/" + commit_exist_2)
            ])

            assert mock_repo_mining.call_count == 2
            mock_repo_mining.assert_has_calls([
                call(url_repo_exist_1 + '.git', commit_exist_1),
                call(url_repo_exist_2 + '.git', commit_exist_2),
            ])

            assert mock_logger().error.call_count == 2
            expected_logger_calls = [call(str_log_1), call(str_log_2)]
            mock_logger().error.assert_has_calls(expected_logger_calls)

        @patch('logging.getLogger')
        @patch('logging.basicConfig')
        @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
        @patch('Dataset2.RepoMining.RepoMiner.RepoMiner.analyze_commit')
        @pytest.mark.parametrize('mock_requests_get', [(True, True, True, True)], indirect=True)
        @pytest.mark.parametrize('mock_repo_mining', [(True, False, False, False)], indirect=True)
        def test_case_8(self, mock_analyze, mock_join, mock_config, mock_logger, mock_requests_get, mock_repo_mining):
            mock_repo_mining, mock_commit = mock_repo_mining

            cve_id_1 = '1'
            url_repo_exist_1 = 'https://github.com/apache/poi'
            commit_exist_1 = 'd72bd78c19dfb7b57395a66ae8d9269d59a87bd2'

            cve_id_2 = '2'
            url_repo_exist_2 = 'https://github.com/spring-projects/spring-webflow'
            commit_exist_2 = '48b2ccb65946620fbf3b1e2165eac1c9eb6b1413'

            content_1 = {
                'cve_id': cve_id_1,
                'repo_url': url_repo_exist_1,
                'commit_id': commit_exist_1
            }

            content_2 = {
                'cve_id': cve_id_2,
                'repo_url': url_repo_exist_2,
                'commit_id': commit_exist_2
            }

            cve_path_1 = self.REPO_PATH + '/' + cve_id_1
            commit_path_1 = cve_path_1 + '/' + commit_exist_1

            cve_path_2 = self.REPO_PATH + '/' + cve_id_2
            commit_path_2 = cve_path_2 + '/' + commit_exist_2

            data = {0: content_1, 1: content_2}

            miner = RepoMiner(self.BASE_DIR)
            miner.start_mining_repo(data, self.REPO_PATH)

            statusOK = "OK!\n"
            str_log_1 = f"indice: 1 link repo: {content_1['repo_url']} status: " + statusOK
            str_log_2 = f"indice: 2 link repo: {content_2['repo_url']} status: " + statusOK

            assert mock_requests_get.call_count == 4
            mock_requests_get.assert_has_calls([
                call(url_repo_exist_1 + ".git"),
                call(url_repo_exist_1 + "/commit/" + commit_exist_1),
                call(url_repo_exist_2 + ".git"),
                call(url_repo_exist_2 + "/commit/" + commit_exist_2)
            ])

            assert mock_repo_mining.call_count == 2
            mock_repo_mining.assert_has_calls([
                call(url_repo_exist_1 + '.git', commit_exist_1),
                call(url_repo_exist_2 + '.git', commit_exist_2),
            ])

            assert mock_analyze.call_count == 2
            mock_analyze.assert_has_calls([
                call(mock_commit, cve_path_1, commit_path_1),
                call(mock_commit, cve_path_2, commit_path_2)
            ])

            assert mock_logger().info.call_count == 2
            expected_logger_calls = [call(str_log_1), call(str_log_2)]
            mock_logger().info.assert_has_calls(expected_logger_calls)

            mock_logger().error.assert_not_called()

        @patch('logging.getLogger')
        @patch('logging.basicConfig')
        @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
        @patch('Dataset2.RepoMining.RepoMiner.RepoMiner.analyze_commit')
        @pytest.mark.parametrize('mock_requests_get', [(True, True, True, True)], indirect=True)
        @pytest.mark.parametrize('mock_repo_mining', [(True, True, False, False)], indirect=True)
        def test_case_9(self, mock_analyze, mock_join, mock_config, mock_logger, mock_requests_get, mock_repo_mining):
            mock_repo_mining, mock_commit = mock_repo_mining

            cve_id_1 = '1'
            url_repo_exist_1 = 'https://github.com/apache/poi'
            commit_exist_1 = 'd72bd78c19dfb7b57395a66ae8d9269d59a87bd2'

            cve_id_2 = '2'
            url_repo_exist_2 = 'https://github.com/spring-projects/spring-webflow'
            commit_exist_2 = '48b2ccb65946620fbf3b1e2165eac1c9eb6b1413'

            content_1 = {
                'cve_id': cve_id_1,
                'repo_url': url_repo_exist_1,
                'commit_id': commit_exist_1
            }

            content_2 = {
                'cve_id': cve_id_2,
                'repo_url': url_repo_exist_2,
                'commit_id': commit_exist_2
            }

            cve_path_1 = self.REPO_PATH + '/' + cve_id_1
            commit_path_1 = cve_path_1 + '/' + commit_exist_1

            cve_path_2 = self.REPO_PATH + '/' + cve_id_2
            commit_path_2 = cve_path_2 + '/' + commit_exist_2

            data = {0: content_1, 1: content_2}

            miner = RepoMiner(self.BASE_DIR)
            miner.start_mining_repo(data, self.REPO_PATH)

            statusOK = "OK!\n"
            str_log_1 = f"indice: 1 link repo: {content_1['repo_url']} status: " + statusOK
            str_log_2 = f"indice: 2 link repo: {content_2['repo_url']} status: " + statusOK

            assert mock_requests_get.call_count == 4
            mock_requests_get.assert_has_calls([
                call(url_repo_exist_1 + ".git"),
                call(url_repo_exist_1 + "/commit/" + commit_exist_1),
                call(url_repo_exist_2 + ".git"),
                call(url_repo_exist_2 + "/commit/" + commit_exist_2)
            ])

            assert mock_repo_mining.call_count == 2
            mock_repo_mining.assert_has_calls([
                call(url_repo_exist_1 + '.git', commit_exist_1),
                call(url_repo_exist_2 + '.git', commit_exist_2),
            ])

            assert mock_analyze.call_count == 2
            mock_analyze.assert_has_calls([
                call(mock_commit, cve_path_1, commit_path_1),
                call(mock_commit, cve_path_2, commit_path_2)
            ])

            assert mock_logger().info.call_count == 2
            expected_logger_calls = [call(str_log_1), call(str_log_2)]
            mock_logger().info.assert_has_calls(expected_logger_calls)

            mock_logger().error.assert_not_called()

        @patch('logging.getLogger')
        @patch('logging.basicConfig')
        @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
        @patch('Dataset2.RepoMining.RepoMiner.RepoMiner.analyze_commit')
        @pytest.mark.parametrize('mock_requests_get', [(True, True, True, True)], indirect=True)
        @pytest.mark.parametrize('mock_repo_mining', [(True, True, True, False)], indirect=True)
        def test_case_10(self, mock_analyze, mock_join, mock_config, mock_logger, mock_requests_get, mock_repo_mining):
            mock_repo_mining, mock_commit = mock_repo_mining

            cve_id_1 = '1'
            url_repo_exist_1 = 'https://github.com/apache/poi'
            commit_exist_1 = 'd72bd78c19dfb7b57395a66ae8d9269d59a87bd2'

            cve_id_2 = '2'
            url_repo_exist_2 = 'https://github.com/spring-projects/spring-webflow'
            commit_exist_2 = '48b2ccb65946620fbf3b1e2165eac1c9eb6b1413'

            content_1 = {
                'cve_id': cve_id_1,
                'repo_url': url_repo_exist_1,
                'commit_id': commit_exist_1
            }

            content_2 = {
                'cve_id': cve_id_2,
                'repo_url': url_repo_exist_2,
                'commit_id': commit_exist_2
            }

            cve_path_1 = self.REPO_PATH + '/' + cve_id_1
            commit_path_1 = cve_path_1 + '/' + commit_exist_1

            cve_path_2 = self.REPO_PATH + '/' + cve_id_2
            commit_path_2 = cve_path_2 + '/' + commit_exist_2

            data = {0: content_1, 1: content_2}

            miner = RepoMiner(self.BASE_DIR)
            miner.start_mining_repo(data, self.REPO_PATH)

            statusOK = "OK!\n"
            str_log_1 = f"indice: 1 link repo: {content_1['repo_url']} status: " + statusOK
            str_log_2 = f"indice: 2 link repo: {content_2['repo_url']} status: " + statusOK

            assert mock_requests_get.call_count == 4
            mock_requests_get.assert_has_calls([
                call(url_repo_exist_1 + ".git"),
                call(url_repo_exist_1 + "/commit/" + commit_exist_1),
                call(url_repo_exist_2 + ".git"),
                call(url_repo_exist_2 + "/commit/" + commit_exist_2)
            ])

            assert mock_repo_mining.call_count == 2
            mock_repo_mining.assert_has_calls([
                call(url_repo_exist_1 + '.git', commit_exist_1),
                call(url_repo_exist_2 + '.git', commit_exist_2),
            ])

            assert mock_analyze.call_count == 2
            mock_analyze.assert_has_calls([
                call(mock_commit, cve_path_1, commit_path_1),
                call(mock_commit, cve_path_2, commit_path_2)
            ])

            assert mock_logger().info.call_count == 2
            expected_logger_calls = [call(str_log_1), call(str_log_2)]
            mock_logger().info.assert_has_calls(expected_logger_calls)

            mock_logger().error.assert_not_called()

        @patch('logging.getLogger')
        @patch('logging.basicConfig')
        @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
        @patch('Dataset2.RepoMining.RepoMiner.RepoMiner.analyze_commit')
        @pytest.mark.parametrize('mock_requests_get', [(True, True, True, True)], indirect=True)
        @pytest.mark.parametrize('mock_repo_mining', [(True, True, True, True)], indirect=True)
        def test_case_11(self, mock_analyze, mock_join, mock_config, mock_logger, mock_requests_get, mock_repo_mining):
            mock_repo_mining, mock_commit = mock_repo_mining

            cve_id_1 = '1'
            url_repo_exist_1 = 'https://github.com/apache/poi'
            commit_exist_1 = 'd72bd78c19dfb7b57395a66ae8d9269d59a87bd2'

            cve_id_2 = '2'
            url_repo_exist_2 = 'https://github.com/spring-projects/spring-webflow'
            commit_exist_2 = '48b2ccb65946620fbf3b1e2165eac1c9eb6b1413'

            content_1 = {
                'cve_id': cve_id_1,
                'repo_url': url_repo_exist_1,
                'commit_id': commit_exist_1
            }

            content_2 = {
                'cve_id': cve_id_2,
                'repo_url': url_repo_exist_2,
                'commit_id': commit_exist_2
            }

            cve_path_1 = self.REPO_PATH + '/' + cve_id_1
            commit_path_1 = cve_path_1 + '/' + commit_exist_1

            cve_path_2 = self.REPO_PATH + '/' + cve_id_2
            commit_path_2 = cve_path_2 + '/' + commit_exist_2

            data = {0: content_1, 1: content_2}

            miner = RepoMiner(self.BASE_DIR)
            miner.start_mining_repo(data, self.REPO_PATH)

            statusOK = "OK!\n"
            str_log_1 = f"indice: 1 link repo: {content_1['repo_url']} status: " + statusOK
            str_log_2 = f"indice: 2 link repo: {content_2['repo_url']} status: " + statusOK

            assert mock_requests_get.call_count == 4
            mock_requests_get.assert_has_calls([
                call(url_repo_exist_1 + ".git"),
                call(url_repo_exist_1 + "/commit/" + commit_exist_1),
                call(url_repo_exist_2 + ".git"),
                call(url_repo_exist_2 + "/commit/" + commit_exist_2)
            ])

            assert mock_repo_mining.call_count == 2
            mock_repo_mining.assert_has_calls([
                call(url_repo_exist_1 + '.git', commit_exist_1),
                call(url_repo_exist_2 + '.git', commit_exist_2),
            ])

            assert mock_analyze.call_count == 2
            mock_analyze.assert_has_calls([
                call(mock_commit, cve_path_1, commit_path_1),
                call(mock_commit, cve_path_2, commit_path_2)
            ])

            assert mock_logger().info.call_count == 2
            expected_logger_calls = [call(str_log_1), call(str_log_2)]
            mock_logger().info.assert_has_calls(expected_logger_calls)

            mock_logger().error.assert_not_called()

        @patch('logging.getLogger')
        @patch('logging.basicConfig')
        @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
        @patch('Dataset2.RepoMining.RepoMiner.RepoMiner.analyze_commit')
        @pytest.mark.parametrize('mock_requests_get', [(True, True, True, True)], indirect=True)
        @pytest.mark.parametrize('mock_repo_mining', [(True, True, True, False)], indirect=True)
        def test_case_12(self, mock_analyze, mock_join, mock_config, mock_logger, mock_requests_get, mock_repo_mining):
            mock_repo_mining, mock_commit = mock_repo_mining

            cve_id_1 = '1'
            url_repo_exist_1 = 'https://github.com/apache/poi'
            commit_exist_1 = 'd72bd78c19dfb7b57395a66ae8d9269d59a87bd2'

            cve_id_2 = '2'
            url_repo_exist_2 = 'https://github.com/spring-projects/spring-webflow'
            commit_exist_2 = '48b2ccb65946620fbf3b1e2165eac1c9eb6b1413'

            content_1 = {
                'cve_id': cve_id_1,
                'repo_url': url_repo_exist_1,
                'commit_id': commit_exist_1
            }

            content_2 = {
                'cve_id': cve_id_2,
                'repo_url': url_repo_exist_2,
                'commit_id': commit_exist_2
            }

            data = {0: content_1, 1: content_2}

            miner = RepoMiner(self.BASE_DIR)

            with pytest.raises(TypeError):
                miner.start_mining_repo(data, 3)

            assert mock_requests_get.call_count == 2
            mock_requests_get.assert_has_calls([
                call(url_repo_exist_1 + ".git"),
                call(url_repo_exist_1 + "/commit/" + commit_exist_1)
            ])

            assert mock_repo_mining.call_count == 1
            mock_repo_mining.assert_has_calls([
                call(url_repo_exist_1 + '.git', commit_exist_1)
            ])

            mock_analyze.assert_not_called()

        @patch('logging.getLogger')
        @patch('logging.basicConfig')
        @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
        @patch('Dataset2.RepoMining.RepoMiner.RepoMiner.analyze_commit', side_effect=custom_analyze_side_effect)
        @pytest.mark.parametrize('mock_requests_get', [(True, True, True, True)], indirect=True)
        @pytest.mark.parametrize('mock_repo_mining', [(True, True, True, False)], indirect=True)
        def test_case_13(self, mock_analyze, mock_join, mock_config, mock_logger, mock_requests_get, mock_repo_mining):
            mock_repo_mining, mock_commit = mock_repo_mining

            cve_id_1 = '1'
            url_repo_exist_1 = 'https://github.com/apache/poi'
            commit_exist_1 = 'd72bd78c19dfb7b57395a66ae8d9269d59a87bd2'

            cve_id_2 = '2'
            url_repo_exist_2 = 'https://github.com/spring-projects/spring-webflow'
            commit_exist_2 = '48b2ccb65946620fbf3b1e2165eac1c9eb6b1413'

            content_1 = {
                'cve_id': cve_id_1,
                'repo_url': url_repo_exist_1,
                'commit_id': commit_exist_1
            }

            content_2 = {
                'cve_id': cve_id_2,
                'repo_url': url_repo_exist_2,
                'commit_id': commit_exist_2
            }

            data = {0: content_1, 1: content_2}

            miner = RepoMiner(self.BASE_DIR)

            wrong_repo_name = 'test/path/mining_results/r3po<<4'
            wrong_cve_id_path = wrong_repo_name + '/' + cve_id_1
            wrong_commit_path = wrong_cve_id_path + '/' + commit_exist_1

            with pytest.raises(OSError):
                miner.start_mining_repo(data, wrong_repo_name)

            assert mock_requests_get.call_count == 2
            mock_requests_get.assert_has_calls([
                call(url_repo_exist_1 + ".git"),
                call(url_repo_exist_1 + "/commit/" + commit_exist_1)
            ])

            assert mock_repo_mining.call_count == 1
            mock_repo_mining.assert_has_calls([
                call(url_repo_exist_1 + '.git', commit_exist_1)
            ])

            assert mock_analyze.call_count == 1
            mock_analyze.assert_has_calls([
                call(mock_commit, wrong_cve_id_path, wrong_commit_path)
            ])

        @patch('logging.getLogger')
        @patch('logging.basicConfig')
        @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
        @patch('Dataset2.RepoMining.RepoMiner.RepoMiner.analyze_commit', side_effect=custom_analyze_side_effect)
        @pytest.mark.parametrize('mock_requests_get', [(True, True, True, True)], indirect=True)
        @pytest.mark.parametrize('mock_repo_mining', [(True, True, True, False)], indirect=True)
        def test_case_14(self, mock_analyze, mock_join, mock_config, mock_logger, mock_requests_get, mock_repo_mining):
            mock_repo_mining, mock_commit = mock_repo_mining

            cve_id_1 = '1'
            url_repo_exist_1 = 'https://github.com/apache/poi'
            commit_exist_1 = 'd72bd78c19dfb7b57395a66ae8d9269d59a87bd2'

            cve_id_2 = '2'
            url_repo_exist_2 = 'https://github.com/spring-projects/spring-webflow'
            commit_exist_2 = '48b2ccb65946620fbf3b1e2165eac1c9eb6b1413'

            content_1 = {
                'cve_id': cve_id_1,
                'repo_url': url_repo_exist_1,
                'commit_id': commit_exist_1
            }

            content_2 = {
                'cve_id': cve_id_2,
                'repo_url': url_repo_exist_2,
                'commit_id': commit_exist_2
            }

            cve_path_1 = self.REPO_PATH + '/' + cve_id_1
            commit_path_1 = cve_path_1 + '/' + commit_exist_1

            cve_path_2 = self.REPO_PATH + '/' + cve_id_2
            commit_path_2 = cve_path_2 + '/' + commit_exist_2

            data = {0: content_1, 1: content_2}

            miner = RepoMiner(self.BASE_DIR)

            with pytest.raises(FileNotFoundError):
                miner.start_mining_repo(data, self.REPO_PATH)

            assert mock_requests_get.call_count == 2
            mock_requests_get.assert_has_calls([
                call(url_repo_exist_1 + ".git"),
                call(url_repo_exist_1 + "/commit/" + commit_exist_1)
            ])

            assert mock_repo_mining.call_count == 1
            mock_repo_mining.assert_has_calls([
                call(url_repo_exist_1 + '.git', commit_exist_1)
            ])

            assert mock_analyze.call_count == 1
            mock_analyze.assert_has_calls([
                call(mock_commit, cve_path_1, commit_path_1)
            ])

        @patch('logging.getLogger')
        @patch('logging.basicConfig')
        @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
        @patch('Dataset2.RepoMining.RepoMiner.RepoMiner.analyze_commit', side_effect=custom_analyze_side_effect)
        @pytest.mark.parametrize('mock_requests_get', [(True, True, True, True)], indirect=True)
        @pytest.mark.parametrize('mock_repo_mining', [(True, True, True, False)], indirect=True)
        def test_case_15(self, mock_analyze, mock_join, mock_config, mock_logger, mock_requests_get, mock_repo_mining):
            mock_repo_mining, mock_commit = mock_repo_mining

            cve_id_1 = '1'
            url_repo_exist_1 = 'https://github.com/apache/poi'
            commit_exist_1 = 'd72bd78c19dfb7b57395a66ae8d9269d59a87bd2'

            cve_id_2 = '2'
            url_repo_exist_2 = 'https://github.com/spring-projects/spring-webflow'
            commit_exist_2 = '48b2ccb65946620fbf3b1e2165eac1c9eb6b1413'

            content_1 = {
                'cve_id': cve_id_1,
                'repo_url': url_repo_exist_1,
                'commit_id': commit_exist_1
            }

            content_2 = {
                'cve_id': cve_id_2,
                'repo_url': url_repo_exist_2,
                'commit_id': commit_exist_2
            }

            cve_path_1 = self.REPO_PATH + '/' + cve_id_1
            commit_path_1 = cve_path_1 + '/' + commit_exist_1

            cve_path_2 = self.REPO_PATH + '/' + cve_id_2
            commit_path_2 = cve_path_2 + '/' + commit_exist_2

            data = {0: content_1, 1: content_2}

            miner = RepoMiner('test<<p4')

            with pytest.raises(OSError):
                miner.start_mining_repo(data, self.REPO_PATH)

            assert mock_requests_get.call_count == 2
            mock_requests_get.assert_has_calls([
                call(url_repo_exist_1 + ".git"),
                call(url_repo_exist_1 + "/commit/" + commit_exist_1)
            ])

            assert mock_repo_mining.call_count == 1
            mock_repo_mining.assert_has_calls([
                call(url_repo_exist_1 + '.git', commit_exist_1)
            ])

            assert mock_analyze.call_count == 1
            mock_analyze.assert_has_calls([
                call(mock_commit, cve_path_1, commit_path_1)
            ])

        @patch('logging.getLogger')
        @patch('logging.basicConfig')
        @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
        @patch('Dataset2.RepoMining.RepoMiner.RepoMiner.analyze_commit', side_effect=custom_analyze_side_effect)
        @pytest.mark.parametrize('mock_requests_get', [(True, True, True, True)], indirect=True)
        @pytest.mark.parametrize('mock_repo_mining', [(True, True, True, False)], indirect=True)
        def test_case_16(self, mock_analyze, mock_join, mock_config, mock_logger, mock_requests_get, mock_repo_mining):
            mock_repo_mining, mock_commit = mock_repo_mining

            cve_id_1 = '1'
            url_repo_exist_1 = 'https://github.com/apache/poi'
            commit_exist_1 = 'd72bd78c19dfb7b57395a66ae8d9269d59a87bd2'

            cve_id_2 = '2'
            url_repo_exist_2 = 'https://github.com/spring-projects/spring-webflow'
            commit_exist_2 = '48b2ccb65946620fbf3b1e2165eac1c9eb6b1413'

            content_1 = {
                'cve_id': cve_id_1,
                'repo_url': url_repo_exist_1,
                'commit_id': commit_exist_1
            }

            content_2 = {
                'cve_id': cve_id_2,
                'repo_url': url_repo_exist_2,
                'commit_id': commit_exist_2
            }

            cve_path_1 = self.REPO_PATH + '/' + cve_id_1
            commit_path_1 = cve_path_1 + '/' + commit_exist_1

            cve_path_2 = self.REPO_PATH + '/' + cve_id_2
            commit_path_2 = cve_path_2 + '/' + commit_exist_2

            data = {0: content_1, 1: content_2}

            miner = RepoMiner(self.BASE_DIR)

            with pytest.raises(FileNotFoundError):
                miner.start_mining_repo(data, self.REPO_PATH)

            assert mock_requests_get.call_count == 2
            mock_requests_get.assert_has_calls([
                call(url_repo_exist_1 + ".git"),
                call(url_repo_exist_1 + "/commit/" + commit_exist_1)
            ])

            assert mock_repo_mining.call_count == 1
            mock_repo_mining.assert_has_calls([
                call(url_repo_exist_1 + '.git', commit_exist_1)
            ])

            assert mock_analyze.call_count == 1
            mock_analyze.assert_has_calls([
                call(mock_commit, cve_path_1, commit_path_1)
            ])





















