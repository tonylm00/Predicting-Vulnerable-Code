from unittest.mock import patch, mock_open

import pytest
from Dataset2.Text_Mining.dict_generator import main

class TestMain:
    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cdv_id1", 'folder': "folder1", 'file': "Example.java"}, {}),
        ],
        indirect=True
    )
    def test_case_1(self, mock_file_system, mock_os_functions):
        del mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results']
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2'] = []

        with pytest.raises(FileNotFoundError, match=r"No such directory: '/Predicting-Vulnerable-Code/Dataset2/mining_results'"):
            main()

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cdv_id1", 'folder': "folder1",
              'file': "Example.java"}, {}),  # Tutto ha contenuti
        ],
        indirect=['mock_file_system', 'mock_os_functions']
    )
    def test_case_2(self, mock_file_system, mock_os_functions):
        # 'mining_results' esiste, ma rimuoviamo una repository specifica, ad esempio 'RepositoryMining2'
        # mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results'].remove('RepositoryMining2')
        del mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2']
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results'].remove("RepositoryMining2")

        # Eseguiamo main e verifichiamo che tenti di accedere a 'RepositoryMining2' e sollevi FileNotFoundError
        with pytest.raises(FileNotFoundError,
                           match=r"No such directory: '/Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2'"):
            main()

    @patch('builtins.print')
    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 1}, {})
        ],
        indirect=True
    )
    def test_case_3(self, mock_print, mock_file_system, mock_os_functions):
        with patch('builtins.open', mock_open()) as mocked_open:
            # Execute the code that should write to the file
            main()

            # Retrieve the mock file handle
            handle = mocked_open()

            mocked_open.assert_any_call('text_mining_dict.txt', 'w+')
            handle.write.assert_called_once_with('{}')

            mock_print.assert_any_call("Ci sono :0 chiavi(che) !")


    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id': "file.txt"}, {})
        ],
        indirect=True
    )
    def test_case_4(self, mock_file_system, mock_os_functions):
        with pytest.raises(NotADirectoryError, match=r"Not a directory: 'file.txt'"):
            main()

    @patch('builtins.print')
    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id': "CHECK.txt"}, {})
        ],
        indirect=True
    )
    def test_case_5(self, mock_print, mock_file_system, mock_os_functions):
        with patch('builtins.open', mock_open()) as mocked_open:
            # Execute the code that should write to the file
            main()

            # Retrieve the mock file handle
            handle = mocked_open()

            mocked_open.assert_any_call('text_mining_dict.txt', 'w+')
            handle.write.assert_called_once_with('{}')

            mock_print.assert_any_call("Ci sono :0 chiavi(che) !")

    @patch('builtins.print')
    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 1, 'cvd_id': "cvd_id1"}, {})
        ],
        indirect=True
    )
    def test_case_6(self, mock_print, mock_file_system, mock_os_functions):
        with patch('builtins.open', mock_open()) as mocked_open:
            # Execute the code that should write to the file
            main()

            # Retrieve the mock file handle
            handle = mocked_open()

            mocked_open.assert_any_call('text_mining_dict.txt', 'w+')
            handle.write.assert_called_once_with('{}')

            mock_print.assert_any_call("Ci sono :0 chiavi(che) !")

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'cvd_id': "cvd_id1", 'folder': "file.txt"}, {})
        ],
        indirect=True
    )
    def test_case_7(self, mock_file_system, mock_os_functions):
        with pytest.raises(NotADirectoryError, match=r"Not a directory: 'file.txt'"):
            main()

    @patch('builtins.print')
    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'cvd_id': "cvd_id1", 'folder': ".DS_Store"}, {})
        ],
        indirect=True
    )
    def test_case_8(self, mock_print, mock_file_system, mock_os_functions):
        with patch('builtins.open', mock_open()) as mocked_open:
            # Execute the code that should write to the file
            main()

            # Retrieve the mock file handle
            handle = mocked_open()

            mocked_open.assert_any_call('text_mining_dict.txt', 'w+')
            handle.write.assert_called_once_with('{}')

            mock_print.assert_any_call("Ci sono :0 chiavi(che) !")

    @patch('builtins.print')
    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 1, 'cvd_id': "cvd_id1", 'folder': "folder1"}, {})
        ],
        indirect=True
    )
    def test_case_9(self, mock_print, mock_file_system, mock_os_functions):
        with patch('builtins.open', mock_open()) as mocked_open:
            # Execute the code that should write to the file
            main()

            # Retrieve the mock file handle
            handle = mocked_open()

            mocked_open.assert_any_call('text_mining_dict.txt', 'w+')
            handle.write.assert_called_once_with('{}')

            mock_print.assert_any_call("Ci sono :0 chiavi(che) !")

    @patch('builtins.print')
    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1", 'file':'.DS_Store'}, {})
        ],
        indirect=True
    )
    def test_case_10(self, mock_print, mock_file_system, mock_os_functions):
        with patch('builtins.open', mock_open()) as mocked_open:
            # Execute the code that should write to the file
            main()

            # Retrieve the mock file handle
            handle = mocked_open()

            mocked_open.assert_any_call('text_mining_dict.txt', 'w+')
            handle.write.assert_called_once_with('{}')

            mock_print.assert_any_call("Ci sono :0 chiavi(che) !")

    @patch('builtins.print')
    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'another_directory'}, {})
        ],
        indirect=True
    )
    def test_case_11(self, mock_print, mock_file_system, mock_os_functions):
        with patch('builtins.open', mock_open()) as mocked_open:
            # Execute the code that should write to the file
            main()

            # Retrieve the mock file handle
            handle = mocked_open()

            mocked_open.assert_any_call('text_mining_dict.txt', 'w+')
            handle.write.assert_called_once_with('{}')

            mock_print.assert_any_call("Ci sono :0 chiavi(che) !")

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'Example.java_text_mining.txt'}, {'file_content': ''})
        ],
        indirect=True
    )
    def test_case_12(self, mock_file_system, mock_os_functions):
        with pytest.raises(SyntaxError, match=r"unexpected EOF while parsing"): #dovuto ad ast
            main()

    @patch('builtins.print')
    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'Example.java_text_mining.txt'}, {'file_content': '''{ [13]: 2, 'net': None, None: 1, 'javamelody', 'import': 6, 'java': 4, 'io': 3}'''})
        ],
        indirect=True
    )
    def test_case_13(self, mock_print, mock_file_system, mock_os_functions):
        with pytest.raises(SyntaxError, match=r"invalid syntax"):  # dovuto ad ast
            main()

    @patch('builtins.print')
    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'Example.java_text_mining.txt'}, {'file_content': '''{'package': 1, 'net': 1, 'bull': 1, 'javamelody': 1, 'import': 6, 'java': 4, 'io': 3}'''})
        ],
        indirect=True
    )
    def test_case_14(self, mock_print, mock_file_system, mock_os_functions):
        main()
        expected_file = 'text_mining_dict.txt'
        assert expected_file in mock_file_system[
            '/Predicting-Vulnerable-Code/Dataset2/mining_results'], f"Il file {expected_file} avrebbe dovuto essere creato."

        # Verifica la chiamata alla funzione print
        mock_print.assert_any_call("Ci sono :7 chiavi(che) !")

    @patch('builtins.print')
    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'Example.java_text_mining.txt'}, {
                 'file_content': '''{'package': 1, 'net': 1, 'bull': 1, 'javamelody': 1, 'import': 6, 'java': 4, 'io': 3}''', 'type_error': 'perm_error'})
        ],
        indirect=True
    )
    def test_case_15(self, mock_print, mock_file_system, mock_os_functions):
        with pytest.raises(PermissionError):  # dovuto ad ast
            main()

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'Example.java_text_mining.txt'}, {'file_content': 'non si tratta di un dizionario'})
        ],
        indirect=True
    )
    def test_case_16(self, mock_file_system, mock_os_functions):
        with pytest.raises(SyntaxError, match=r"invalid syntax"):  # dovuto ad ast
            main()

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'Example.java_text_mining.txt'}, {'file_content': '', 'type_error': 'access_error'})
        ],
        indirect=True
    )
    def test_case_17(self, mock_file_system, mock_os_functions):
        with pytest.raises(PermissionError):  # dovuto ad ast
            main()

