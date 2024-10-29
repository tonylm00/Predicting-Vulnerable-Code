import os
from unittest.mock import patch, mock_open, Mock, call
from urllib.parse import urlparse

import pytest
from requests.exceptions import MissingSchema
from requests.exceptions import ConnectionError


from Dataset2.RepoMining.repo_Mining import startMiningRepo
import requests

class TestStartMiningRepo:

    CHECK_FILE_NAME = 'CHECK.txt'
    ERR_FILE_NAME = 'ERRORS.txt'

    CWD = os.path.join('Dataset', 'tests', 'RepoMining', 'temp')
    MINING_DIR = os.path.join('Dataset', 'tests', 'RepoMining', 'mining_results')

    @patch('os.mkdir')  # Mock os.chdir if needed
    @patch('os.chdir')  # Mock os.chdir if needed
    @pytest.mark.parametrize('mock_files', [
        {CHECK_FILE_NAME: 'File1 content', ERR_FILE_NAME: 'File2 content'}
    ], indirect=True)
    def test_case_1(self, mock_chdir, mock_mkdir, mock_files):
        # content missing cve_id key

        data = dict()

        repoName = "TestRepo"

        startMiningRepo(data, self.CWD, repoName)  # Function that triggers the file operation

        mock_chdir.assert_not_called()

        mock_mkdir.assert_not_called()

        check_file_mock = mock_files[self.CHECK_FILE_NAME]()
        error_file_mock = mock_files[self.ERR_FILE_NAME]()

        check_file_mock.write.assert_not_called()
        error_file_mock.write.assert_not_called()


    @patch('os.mkdir')  # Mock os.chdir if needed
    @patch('os.chdir')  # Mock os.chdir if needed
    @pytest.mark.parametrize('mock_files', [
        {CHECK_FILE_NAME: 'File1 content', ERR_FILE_NAME: 'File2 content'}
    ], indirect=True)
    def test_case_2(self, mock_chdir, mock_mkdir, mock_files):

        #content missing cve_id key
        content = {
            'repo_url': 'https://github.com/spring-projects/spring-webflow',
            'commit_id': '57f2ccb66946943fbf3b3f2165eac1c8eb6b1523',
            'cls': 'pos'
        }

        data = dict()
        data[0] = content

        repoName = "TestRepo"

        with pytest.raises(KeyError) as exc_info:
            startMiningRepo(data, self.CWD, repoName)  # Function that triggers the file operation

        assert 'cve_id' in str(exc_info.value)

        mock_chdir.assert_not_called()

        mock_mkdir.assert_not_called()


    # WHEN THE LINK IS NOT VALID, I GOT MISSINGSCHEMA
    @patch('os.mkdir')
    @patch('os.chdir')
    @pytest.mark.parametrize('mock_files', [
        {CHECK_FILE_NAME: 'File1 content', ERR_FILE_NAME: 'File2 content'}
    ], indirect=True)
    @pytest.mark.parametrize('mock_requests_get', [(False, False, False, False)], indirect=True)
    def test_case_3(self, mock_chdir, mock_mkdir, mock_files, mock_requests_get):

        invalid_url = 'not_url'

        content = {
            'cve_id': '1',
            'repo_url': invalid_url,
            'commit_id': '57f2ccb66946943fbf3b3f2165eac1c8eb6b1523',
            'cls': 'pos'
        }

        data = dict()
        data[0] = content

        repoName = "TestRepo"

        with pytest.raises(MissingSchema) as exc_info:
            startMiningRepo(data, self.CWD, repoName)

        assert 'Invalid URL' in str(exc_info.value) and invalid_url + '.git' in str(exc_info.value)

        mock_chdir.assert_not_called()

        mock_mkdir.assert_not_called()


    # WHEN THE LINK IS VALID BUT IT DOES NOT REFER TO AN EXISTING HOST, I GOT CONNECTIONERROR
    @patch('os.mkdir')
    @patch('os.chdir')
    @pytest.mark.parametrize('mock_files', [
        {CHECK_FILE_NAME: 'File1 content', ERR_FILE_NAME: 'File2 content'}
    ], indirect=True)
    @pytest.mark.parametrize('mock_requests_get', [(True, False, False, False)], indirect=True)
    def test_case_4(self, mock_chdir, mock_mkdir, mock_files, mock_requests_get):

        url_link_not_exist = 'https://github'

        content = {
            'cve_id': 1,
            'repo_url': url_link_not_exist,
            'commit_id': '57f2ccb66946943fbf3b3f2165eac1c8eb6b1523',
            'cls': 'pos'
        }

        data = dict()
        data[0] = content

        repoName = "TestRepo"

        with pytest.raises(ConnectionError) as exc_info:
            startMiningRepo(data, self.CWD, repoName)

        parsed_url = urlparse(url_link_not_exist)
        host_with_port = parsed_url.netloc
        host = host_with_port.split(':')[0]

        mock_chdir.assert_not_called()

        mock_mkdir.assert_not_called()

        assert 'ConnectionError' in str(exc_info) and host in str(exc_info.value)

    @patch('os.mkdir')
    @patch('os.chdir')
    @pytest.mark.parametrize('mock_files', [
        {CHECK_FILE_NAME: 'File1 content', ERR_FILE_NAME: 'File2 content'}
    ], indirect=True)
    @pytest.mark.parametrize('mock_requests_get', [(True, True, False, False)], indirect=True)
    def test_case_5(self, mock_chdir, mock_mkdir, mock_files, mock_requests_get):

        url_repo_not_exist = 'https://github.com/repo_not_found'

        content = {
            'cve_id': 1,
            'repo_url': url_repo_not_exist,
            'commit_id': '57f2ccb66946943fbf3b3f2165eac1c8eb6b1523',
            'cls': 'pos'
        }

        data = {0: content}

        repoName = "TestRepo"

        startMiningRepo(data, self.CWD, repoName)

        statusNR = "REPO NOT AVAILABLE\n"
        str_check = f"indice: 1 link repo: {content['repo_url']} status: {statusNR}"

        mock_requests_get.assert_called_once_with(url_repo_not_exist + ".git")

        mock_chdir.assert_not_called()

        mock_mkdir.assert_not_called()

        check_file_mock = mock_files[self.CHECK_FILE_NAME]()
        error_file_mock = mock_files[self.ERR_FILE_NAME]()

        check_file_mock.write.assert_called_once_with(str_check)
        error_file_mock.write.assert_not_called()



    @patch('os.mkdir')
    @patch('os.chdir')
    @pytest.mark.parametrize('mock_files', [
        {CHECK_FILE_NAME: 'File1 content', ERR_FILE_NAME: 'File2 content'}
    ], indirect=True)
    @pytest.mark.parametrize('mock_requests_get', [(True, True, True, False)], indirect=True)
    def test_case_6(self, mock_chdir, mock_mkdir, mock_files, mock_requests_get):

        url_repo_exist = 'https://github.com/spring-projects/spring-webflow'
        commit_not_exist = '1200fh3'

        content = {
            'cve_id': 1,
            'repo_url': url_repo_exist,
            'commit_id': commit_not_exist,
            'cls': 'pos'
        }

        data = {0: content}

        repoName = "TestRepo"

        startMiningRepo(data, self.CWD, repoName)

        statusNE = "NOT EXIST COMMIT\n"
        str_check = f"indice: 1 link repo: {content['repo_url']} status: {statusNE}"

        mock_requests_get.assert_has_calls([
            call(url_repo_exist + ".git"),
            call(url_repo_exist +"/commit/"+commit_not_exist )
        ])

        mock_chdir.assert_not_called()

        mock_mkdir.assert_not_called()

        check_file_mock = mock_files[self.CHECK_FILE_NAME]()
        error_file_mock = mock_files[self.ERR_FILE_NAME]()

        check_file_mock.write.assert_called_once_with(str_check)
        error_file_mock.write.assert_not_called()

    @patch('os.mkdir')
    @patch('os.chdir')
    @pytest.mark.parametrize('mock_files', [
        {CHECK_FILE_NAME: 'File1 content', ERR_FILE_NAME: 'File2 content'}
    ], indirect=True)
    @pytest.mark.parametrize('mock_requests_get', [(True, True, True, True)], indirect=True)
    @pytest.mark.parametrize('mock_repo_mining', [(False, False, False, False)], indirect=True)
    def test_case_7(self, mock_chdir, mock_mkdir, mock_files, mock_requests_get, mock_repo_mining):

        url_repo_exist_1 = 'https://github.com/apache/poi'
        commit_exist_1 = 'd72bd78c19dfb7b57395a66ae8d9269d59a87bd2'

        url_repo_exist_2 = 'https://github.com/apache/santuario-java'
        commit_exist_2 = 'a09b9042f7759d094f2d49f40fc7bcf145164b25'

        content_1 = {
            'cve_id': 1,
            'repo_url': url_repo_exist_1,
            'commit_id': commit_exist_1,
            'cls': 'pos'
        }

        content_2 = {
            'cve_id': 2,
            'repo_url': url_repo_exist_2,
            'commit_id': commit_exist_2,
            'cls': 'pos'
        }

        data = {0: content_1, 1:content_2}

        repoName = "TestRepo"

        startMiningRepo(data, self.CWD, repoName)

        statusVE = "VALUE ERROR! COMMIT HASH NOT EXISTS\n"
        str_check_1 = f"indice: 1 link repo: {content_1['repo_url']} status: " + statusVE
        str_err_1 = f"indice: 1 link repo: {content_1['repo_url']} status: " + statusVE + "," + commit_exist_1

        str_check_2 = f"indice: 2 link repo: {content_2['repo_url']} status: " + statusVE
        str_err_2 = f"indice: 2 link repo: {content_2['repo_url']} status: " + statusVE + "," + commit_exist_2


        mock_requests_get.assert_has_calls([
            call(url_repo_exist_1 + ".git"),
            call(url_repo_exist_1 +"/commit/"+ commit_exist_1 ),
            call(url_repo_exist_2 + ".git"),
            call(url_repo_exist_2 + "/commit/" + commit_exist_2)
        ])


        mock_repo_mining.assert_has_calls([
            call(url_repo_exist_1 + '.git', commit_exist_1),
            call(url_repo_exist_2 + '.git', commit_exist_2),
        ])

        mock_chdir.assert_not_called()

        mock_mkdir.assert_not_called()

        check_file_mock = mock_files[self.CHECK_FILE_NAME]()
        error_file_mock = mock_files[self.ERR_FILE_NAME]()

        check_file_mock.write.assert_has_calls([
            call(str_check_1),
            call(str_check_2),
        ])
        error_file_mock.write.assert_has_calls([
            call(str_err_1),
            call(str_err_2),
        ])


    @patch('os.chdir')
    @patch('os.mkdir')
    @pytest.mark.parametrize('mock_files', [
        {CHECK_FILE_NAME: 'File1 content', ERR_FILE_NAME: 'File2 content'}
    ], indirect=True)
    @pytest.mark.parametrize('mock_requests_get', [(True, True, True, True)], indirect=True)
    @pytest.mark.parametrize('mock_repo_mining', [(True, False, False, False)], indirect=True)
    def test_case_8(self, mock_mkdir, mock_chdir, mock_files, mock_requests_get, mock_repo_mining):

        url_repo_exist = 'https://github.com/apache/poi'
        commit_exist = 'd72bd78c19dfb7b57395a66ae8d9269d59a87bd2'

        content = {
            'cve_id': 1,
            'repo_url': url_repo_exist,
            'commit_id': commit_exist,
            'cls': 'pos'
        }

        data = {0: content}

        repoName = "TestRepo"

        startMiningRepo(data, self.CWD, repoName)

        statusOK = "OK!\n"
        str_check = f"indice: 1 link repo: {content['repo_url']} status: " + statusOK


        mock_requests_get.assert_has_calls([
            call(url_repo_exist + ".git"),
            call(url_repo_exist +"/commit/"+ commit_exist )
        ])

        mock_repo_mining.assert_called_once_with(url_repo_exist + '.git', commit_exist)

        mock_mkdir.assert_not_called()

        mock_chdir.assert_not_called()

        check_file_mock = mock_files[self.CHECK_FILE_NAME]()
        error_file_mock = mock_files[self.ERR_FILE_NAME]()

        check_file_mock.write.assert_called_once_with(str_check)
        error_file_mock.write.assert_not_called()

    @patch('os.chdir')
    @patch('os.mkdir')
    @pytest.mark.parametrize('mock_files', [
        {CHECK_FILE_NAME: 'File1 content', ERR_FILE_NAME: 'File2 content'}
    ], indirect=True)
    @pytest.mark.parametrize('mock_requests_get', [(True, True, True, True)], indirect=True)
    @pytest.mark.parametrize('mock_repo_mining', [(True, True, False, False)], indirect=True)
    def test_case_9(self, mock_mkdir, mock_chdir, mock_files, mock_requests_get, mock_repo_mining):

        url_repo_exist = 'https://github.com/apache/poi'
        commit_exist = 'd72bd78c19dfb7b57395a66ae8d9269d59a87bd2'

        content = {
            'cve_id': 1,
            'repo_url': url_repo_exist,
            'commit_id': commit_exist,
            'cls': 'pos'
        }

        data = {0: content}

        repoName = "TestRepo"

        startMiningRepo(data, self.CWD, repoName)

        statusOK = "OK!\n"
        str_check = f"indice: 1 link repo: {content['repo_url']} status: " + statusOK


        mock_requests_get.assert_has_calls([
            call(url_repo_exist + ".git"),
            call(url_repo_exist +"/commit/"+ commit_exist )
        ])

        mock_repo_mining.assert_called_once_with(url_repo_exist + '.git', commit_exist)

        mock_mkdir.assert_not_called()

        mock_chdir.assert_not_called()

        check_file_mock = mock_files[self.CHECK_FILE_NAME]()
        error_file_mock = mock_files[self.ERR_FILE_NAME]()

        check_file_mock.write.assert_called_once_with(str_check)
        error_file_mock.write.assert_not_called()

    @patch('os.chdir')
    @patch('os.mkdir')
    @pytest.mark.parametrize('mock_files', [
        {CHECK_FILE_NAME: 'File1 content', ERR_FILE_NAME: 'File2 content', 'file1.java': ''}
    ], indirect=True)
    @pytest.mark.parametrize('mock_requests_get', [(True, True, True, True)], indirect=True)
    @pytest.mark.parametrize('mock_repo_mining', [(True, True, True, False)], indirect=True)
    @pytest.mark.parametrize('mock_os_listdir', [
        {"cve_id": '1', "cve_id_exists": False, "commit_id": 'd72bd78c19dfb7b57395a66ae8d9269d59a87bd2' , "commit_exists": False}
    ]
        , indirect=True)
    def test_case_10(self, mock_mkdir, mock_chdir, mock_files, mock_requests_get, mock_repo_mining, mock_os_listdir):
        mock_list, cve_id, commit_id = mock_os_listdir

        url_repo_exist = 'https://github.com/apache/poi'

        content = {
            'cve_id': cve_id,
            'repo_url': url_repo_exist,
            'commit_id': commit_id,
            'cls': 'pos'
        }

        data = {0: content}

        repoName = "TestRepo"


        startMiningRepo(data, self.CWD, repoName)

        statusOK = "OK!\n"
        str_check = f"indice: 1 link repo: {content['repo_url']} status: " + statusOK


        mock_requests_get.assert_has_calls([
            call(url_repo_exist + ".git"),
            call(url_repo_exist +"/commit/"+ commit_id )
        ])

        mock_repo_mining.assert_called_once_with(url_repo_exist + '.git', commit_id)

        mock_mkdir.assert_has_calls([
            call(cve_id),
            call(commit_id)
        ])

        expected_chdir_calls = [
            call(cve_id),
            call(commit_id),
            call(os.path.join(self.MINING_DIR, repoName))
        ]
        mock_chdir.assert_has_calls(expected_chdir_calls, any_order=False)

        mock_files['file1.java'].assert_not_called()

        check_file_mock = mock_files[self.CHECK_FILE_NAME]()
        error_file_mock = mock_files[self.ERR_FILE_NAME]()

        # Alternatively, you can check if mock_file was called
        check_file_mock.write.assert_called_once_with(str_check)
        error_file_mock.write.assert_not_called()

    @patch('os.chdir')
    @patch('os.mkdir')
    @pytest.mark.parametrize('mock_files', [
        {CHECK_FILE_NAME: 'File1 content', ERR_FILE_NAME: 'File2 content', 'file1.java': ''}
    ], indirect=True)
    @pytest.mark.parametrize('mock_requests_get', [(True, True, True, True)], indirect=True)
    @pytest.mark.parametrize('mock_repo_mining', [(True, True, True, True)], indirect=True)
    @pytest.mark.parametrize('mock_os_listdir', [
        {"cve_id": '1', "cve_id_exists": True, "commit_id": 'd72bd78c19dfb7b57395a66ae8d9269d59a87bd2' , "commit_exists": True}
    ]
        , indirect=True)
    def test_case_11(self, mock_mkdir, mock_chdir, mock_files, mock_requests_get, mock_repo_mining, mock_os_listdir):
        mock_list, cve_id, commit_id = mock_os_listdir

        url_repo_exist = 'https://github.com/apache/poi'

        content = {
            'cve_id': cve_id,
            'repo_url': url_repo_exist,
            'commit_id': commit_id,
            'cls': 'pos'
        }

        data = {0: content}

        repoName = "TestRepo"

        startMiningRepo(data, self.CWD, repoName)

        statusOK = "OK!\n"
        str_check = f"indice: 1 link repo: {content['repo_url']} status: " + statusOK


        mock_requests_get.assert_has_calls([
            call(url_repo_exist + ".git"),
            call(url_repo_exist +"/commit/"+ commit_id )
        ])

        mock_repo_mining.assert_called_once_with(url_repo_exist + '.git', commit_id)

        mock_mkdir.assert_not_called()

        expected_chdir_calls = [
            call(cve_id),
            call(commit_id),
            call(os.path.join(self.MINING_DIR, repoName))
        ]
        mock_chdir.assert_has_calls(expected_chdir_calls, any_order=False)

        file_java_mock = mock_files['file1.java']()

        file_java_mock.write.assert_called_once_with('public class File1 {}')

        check_file_mock = mock_files[self.CHECK_FILE_NAME]()
        error_file_mock = mock_files[self.ERR_FILE_NAME]()

        check_file_mock.write.assert_called_once_with(str_check)
        error_file_mock.write.assert_not_called()

    @patch('os.mkdir')
    @pytest.mark.parametrize('mock_files', [
        {CHECK_FILE_NAME: 'File1 content', ERR_FILE_NAME: 'File2 content', 'file1.java': ''}
    ], indirect=True)
    @pytest.mark.parametrize('mock_requests_get', [(True, True, True, True)], indirect=True)
    @pytest.mark.parametrize('mock_repo_mining', [(True, True, True, True)], indirect=True)
    @pytest.mark.parametrize('mock_os_listdir', [
        {"cve_id": '1', "cve_id_exists": True, "commit_id": 'd72bd78c19dfb7b57395a66ae8d9269d59a87bd2' , "commit_exists": True}
    ]
        , indirect=True)
    @pytest.mark.parametrize('mock_os_chdir', [{'error_path': None}], indirect=True)
    def test_case_12(self, mock_mkdir, mock_files, mock_requests_get, mock_repo_mining, mock_os_listdir, mock_os_chdir):
        mock_list, cve_id, commit_id = mock_os_listdir

        url_repo_exist = 'https://github.com/apache/poi'

        content = {
            'cve_id': cve_id,
            'repo_url': url_repo_exist,
            'commit_id': commit_id,
            'cls': 'pos'
        }

        data = {0: content}

        repoName = 1
        wrong_cwd = 22

        with pytest.raises(TypeError):
            startMiningRepo(data, wrong_cwd, repoName)

        mock_mkdir.assert_not_called()

        expected_chdir_calls = [
            call(cve_id),
            call(commit_id)
        ]

        mock_os_chdir.assert_has_calls(expected_chdir_calls, any_order=False)

    @patch('os.mkdir')
    @pytest.mark.parametrize('mock_files', [
        {CHECK_FILE_NAME: 'File1 content', ERR_FILE_NAME: 'File2 content', 'file1.java': ''}
    ], indirect=True)
    @pytest.mark.parametrize('mock_requests_get', [(True, True, True, True)], indirect=True)
    @pytest.mark.parametrize('mock_repo_mining', [(True, True, True, True)], indirect=True)
    @pytest.mark.parametrize('mock_os_listdir', [
        {"cve_id": '1', "cve_id_exists": True, "commit_id": 'd72bd78c19dfb7b57395a66ae8d9269d59a87bd2' , "commit_exists": True}
    ]
        , indirect=True)
    @pytest.mark.parametrize('mock_os_chdir', [{'error_path': None}], indirect=True)
    def test_case_13(self, mock_mkdir, mock_files, mock_requests_get, mock_repo_mining, mock_os_listdir, mock_os_chdir):
        mock_list, cve_id, commit_id = mock_os_listdir

        url_repo_exist = 'https://github.com/apache/poi'

        content = {
            'cve_id': cve_id,
            'repo_url': url_repo_exist,
            'commit_id': commit_id,
            'cls': 'pos'
        }

        data = {0: content}

        repoName = ':>'
        wrong_cwd = os.path.join("3>", "path")
        oracle_cwd = os.path.join("3>", "mining_results")

        with pytest.raises(OSError) as exc_info:
            startMiningRepo(data, wrong_cwd, repoName)

        assert 'Invalid directory format' in str(exc_info.value)

        mock_mkdir.assert_not_called()

        expected_chdir_calls = [
            call(cve_id),
            call(commit_id),
            call(oracle_cwd + os.sep + repoName)
        ]

        mock_os_chdir.assert_has_calls(expected_chdir_calls, any_order=False)

    @patch('os.mkdir')
    @pytest.mark.parametrize('mock_files', [
        {CHECK_FILE_NAME: 'File1 content', ERR_FILE_NAME: 'File2 content', 'file1.java': ''}
    ], indirect=True)
    @pytest.mark.parametrize('mock_requests_get', [(True, True, True, True)], indirect=True)
    @pytest.mark.parametrize('mock_repo_mining', [(True, True, True, True)], indirect=True)
    @pytest.mark.parametrize('mock_os_listdir', [
        {"cve_id": '1', "cve_id_exists": True, "commit_id": 'd72bd78c19dfb7b57395a66ae8d9269d59a87bd2' , "commit_exists": True}
    ]
        , indirect=True)
    @pytest.mark.parametrize('mock_os_chdir', [{'check_path_exist': False, 'error_path': CWD + "/" + 'test'}], indirect=True)
    def test_case_14(self, mock_mkdir, mock_files, mock_requests_get, mock_repo_mining, mock_os_listdir, mock_os_chdir):
        mock_list, cve_id, commit_id = mock_os_listdir

        url_repo_exist = 'https://github.com/apache/poi'

        content = {
            'cve_id': cve_id,
            'repo_url': url_repo_exist,
            'commit_id': commit_id,
            'cls': 'pos'
        }

        data = {0: content}

        repoName = 'test'

        with pytest.raises(FileNotFoundError):
            startMiningRepo(data, self.CWD, repoName)

        mock_mkdir.assert_not_called()

        expected_chdir_calls = [
            call(cve_id),
            call(commit_id),
            call(self.CWD + "/" + repoName)
        ]

        mock_os_chdir.assert_has_calls(expected_chdir_calls, any_order=False)

    @patch('os.mkdir')
    @patch('os.chdir')
    @pytest.mark.parametrize('mock_files', [
        {'Default': None}
    ], indirect=True)
    @pytest.mark.parametrize('mock_op_permission_err', [CHECK_FILE_NAME], indirect=True)
    def test_case_15(self, mock_chdir, mock_mkdir, mock_op_permission_err, mock_files):

        content = {
            'cve_id': '1',
            'repo_url': 'https://github.com/apache/poi',
            'commit_id': 'd72bd78c19dfb7b57395a66ae8d9269d59a87bd2',
            'cls': 'pos'
        }

        data = {0: content}

        repoName = 'test'


        with pytest.raises(PermissionError):
            startMiningRepo(data, self.CWD, repoName)

        mock_mkdir.assert_not_called()

        mock_chdir.assert_not_called()

    @patch('os.mkdir')
    @patch('os.chdir')
    @pytest.mark.parametrize('mock_files', [
        {'Default': None}
    ], indirect=True)
    @pytest.mark.parametrize('mock_op_permission_err', [ERR_FILE_NAME], indirect=True)
    def test_case_16(self, mock_chdir, mock_mkdir, mock_op_permission_err, mock_files):

        content = {
            'cve_id': '1',
            'repo_url': 'https://github.com/apache/poi',
            'commit_id': 'd72bd78c19dfb7b57395a66ae8d9269d59a87bd2',
            'cls': 'pos'
        }

        data = {0: content}

        repoName = 'test'


        with pytest.raises(PermissionError):
            startMiningRepo(data, self.CWD, repoName)

        mock_mkdir.assert_not_called()

        mock_chdir.assert_not_called()

