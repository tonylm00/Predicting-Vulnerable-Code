from unittest.mock import patch, mock_open
import pytest
from Dataset2.Text_Mining.dict_generator import main

class TestMainDict:
    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cdv_id1", 'folder': "folder1", 'file': "Example.java"}, {}),
        ],
        indirect=True
    )
    def test_case_1(self, mock_file_system, mock_os_functions):
        del mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results']
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2'] = set()

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
        mock_chdir, mock_open = mock_os_functions

        # Execute the code that should write to the file
        main()

        mock_open.assert_any_call('text_mining_dict.txt', 'w+', 'utf-8') # aggiunto 'utf-8'
        mock_open().write.assert_called_once_with('{}')

        mock_print.assert_any_call("Ci sono :0 chiavi(che) !")
        assert mock_chdir.call_count == 70

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
        mock_chdir, mock_open = mock_os_functions
        # Execute the code that should write to the file
        main()


        mock_open.assert_any_call('text_mining_dict.txt', 'w+', 'utf-8') # aggiunto 'utf-8'
        mock_open().write.assert_called_once_with('{}')
        mock_print.assert_any_call("Ci sono :0 chiavi(che) !")
        assert mock_chdir.call_count == 70

    @patch('builtins.print')
    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 1, 'cvd_id': "cvd_id1"}, {})
        ],
        indirect=True
    )
    def test_case_6(self, mock_print, mock_file_system, mock_os_functions):
        mock_chdir, mock_open = mock_os_functions
        # Execute the code that should write to the file
        main()

        mock_open.assert_any_call('text_mining_dict.txt', 'w+', 'utf-8') # aggiunto 'utf-8'
        mock_open().write.assert_called_once_with('{}')

        mock_print.assert_any_call("Ci sono :0 chiavi(che) !")
        assert mock_chdir.call_count == 138

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
        mock_chdir, mock_open = mock_os_functions
        # Execute the code that should write to the file
        main()

        mock_open.assert_any_call('text_mining_dict.txt', 'w+', 'utf-8') # aggiunto 'utf-8'
        mock_open().write.assert_called_once_with('{}')

        mock_print.assert_any_call("Ci sono :0 chiavi(che) !")
        assert mock_chdir.call_count == 138

    @patch('builtins.print')
    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 1, 'cvd_id': "cvd_id1", 'folder': "folder1"}, {})
        ],
        indirect=True
    )
    def test_case_9(self, mock_print, mock_file_system, mock_os_functions):
        mock_chdir, mock_open = mock_os_functions
        # Execute the code that should write to the file
        main()

        mock_open.assert_any_call('text_mining_dict.txt', 'w+', 'utf-8') # aggiunto 'utf-8'
        mock_open().write.assert_called_once_with('{}')

        mock_print.assert_any_call("Ci sono :0 chiavi(che) !")
        assert mock_chdir.call_count == 206

    @patch('builtins.print')
    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1", 'file':'.DS_Store'}, {})
        ],
        indirect=True
    )
    def test_case_10(self, mock_print, mock_file_system, mock_os_functions):
        mock_chdir, mock_open = mock_os_functions
        # Execute the code that should write to the file
        main()

        mock_open.assert_any_call('text_mining_dict.txt', 'w+', 'utf-8') # aggiunto 'utf-8'
        mock_open().write.assert_called_once_with('{}')

        mock_print.assert_any_call("Ci sono :0 chiavi(che) !")
        assert mock_chdir.call_count == 206

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
        mock_chdir, mock_open = mock_os_functions
        # Execute the code that should write to the file
        main()

        mock_open.assert_any_call('text_mining_dict.txt', 'w+', 'utf-8') # aggiunto 'utf-8'
        mock_open().write.assert_called_once_with('{}')

        mock_print.assert_any_call("Ci sono :0 chiavi(che) !")
        assert mock_chdir.call_count == 206

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'text_mining.txtdirectory'}, {'file_to_fail': 'text_mining.txtdirectory', 'type_error': 'directory_error'})
        ],
        indirect=True
    )
    def test_case_12(self, mock_file_system, mock_os_functions):
        with pytest.raises(IsADirectoryError):
            main()

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'Example.java_text_mining.txt'}, {'file_contents': {'Example.java_text_mining.txt': ''}})
        ],
        indirect=True
    )
    def test_case_13(self, mock_file_system, mock_os_functions):
        with pytest.raises(SyntaxError, match=r"unexpected EOF while parsing"): #dovuto ad ast
            main()

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'Example.java_text_mining.txt'}, {'file_contents': {'Example.java_text_mining.txt': '''{ [13]: 2, 'net': None, None: 1, 'javamelody', 'import': 6, 'java': 4, 'io': 3}'''}})
        ],
        indirect=True
    )
    def test_case_14(self, mock_file_system, mock_os_functions):
        with pytest.raises(SyntaxError, match=r"invalid syntax"):
            main()

    # Abbiamo compreso che dict_generator non crea un dizionario di tutte le parole con la frequenza delle parole in tutti i file ma solo dell'ultimo file in cui era presente la parola
    @patch('builtins.print')
    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'Example.java_text_mining.txt'}, {'file_contents': {'Example.java_text_mining.txt': '''{'package': 1, 'net': 1, 'bull': 1, 'javamelody': 1, 'import': 6, 'java': 4, 'io': 3}'''}})
        ],
        indirect=True
    )
    def test_case_15(self, mock_print, mock_file_system, mock_os_functions):
        main()
        expected_file = 'text_mining_dict.txt'
        assert expected_file in mock_file_system[
            '/Predicting-Vulnerable-Code/Dataset2/mining_results'], f"Il file {expected_file} avrebbe dovuto essere creato."
        mock_chdir, mock_open = mock_os_functions

        mock_open().write.assert_called_once_with("{'package': 1, 'net': 1, 'bull': 1, 'javamelody': 1, 'import': 6, 'java': 4, 'io': 3}")

        # Verifica la chiamata alla funzione print
        mock_print.assert_any_call("Ci sono :7 chiavi(che) !")
        assert mock_chdir.call_count == 206


    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'Example.java_text_mining.txt'}, {
                 'file_contents': {'Example.java_text_mining.txt': '''{'package': 1, 'net': 1, 'bull': 1, 'javamelody': 1, 'import': 6, 'java': 4, 'io': 3}'''}, 'file_to_fail': 'text_mining_dict.txt', 'type_error': 'perm_error'})
        ],
        indirect=True
    )
    def test_case_16(self, mock_file_system, mock_os_functions):
        with pytest.raises(PermissionError):  # dovuto ad ast
            main()

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'Example.java_text_mining.txt'}, {'file_contents': {'Example.java_text_mining.txt': 'non si tratta di un dizionario'}})
        ],
        indirect=True
    )
    def test_case_17(self, mock_file_system, mock_os_functions):
        with pytest.raises(SyntaxError, match=r"invalid syntax"):  # dovuto ad ast
            main()

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'Example.java_text_mining.txt'}, {'file_contents': {'Example.java_text_mining.txt':'''{'package': 1, 'net': 1, 'bull': 1, 'javamelody': 1, 'import': 6, 'java': 4, 'io': 3}'''}, 'file_to_fail': 'Example.java_text_mining.txt', 'type_error': 'access_error'})
        ],
        indirect=True
    )
    def test_case_18(self, mock_file_system, mock_os_functions):
        with pytest.raises(PermissionError):
            main()

