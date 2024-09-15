import pytest
from unittest.mock import patch, call
from Dataset2.Text_Mining.creator_csv_for_TextMining import main

class TestMainCSV:
    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cdv_id1", 'folder': "folder1",
              'file': "Example.java"}, {}),
        ],
        indirect=True
    )
    def test_case_1(self, mock_file_system, mock_os_functions):
        del mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results']
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2'] = set()

        with pytest.raises(FileNotFoundError,
                           match=r"No such directory: '/Predicting-Vulnerable-Code/Dataset2/mining_results'"):
            main()

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cdv_id1", 'folder': "folder1",
              'file': "Example.txt"}, {}),
        ],
        indirect=True
    )
    def test_case_2(self, mock_file_system, mock_os_functions):
        with pytest.raises(FileNotFoundError,
                           match=r"No such file: 'FilteredTextMining.txt'"):
            main()

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cdv_id1", 'folder': "folder1",
              'file': "Example.java"}, {
                 'file_contents': {
                     'FilteredTextMining.txt': ''}}),
        ],
        indirect=True
    )
    def test_case_3(self, mock_file_system, mock_os_functions):
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results'].add("FilteredTextMining.txt")

        with pytest.raises(SyntaxError,
                           match=r"unexpected EOF while parsing"):
            main()

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cdv_id1", 'folder': "folder1",
              'file': "Example.java"}, {
                 'file_contents': {
                     'FilteredTextMining.txt': '["prova","prova1"]'}}),
        ],
        indirect=True
    )
    def test_case_4(self, mock_file_system, mock_os_functions):
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results'].add("FilteredTextMining.txt")

        with pytest.raises(AttributeError):
            main()

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cdv_id1", 'folder': "folder1",
              'file': "Example.java"}, {
                 'file_contents': {
                     'FilteredTextMining.txt': '''{'package': 723, 'org': 16, 'apache': 32, 'shiro': 24, 'web': 1650, 'util': 986, 'import': 584}'''}}),
        ],
        indirect=True
    )
    def test_case_5(self, mock_file_system, mock_os_functions):
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results'].add("FilteredTextMining.txt")
        del mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2']
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results'].remove("RepositoryMining2")

        # Eseguiamo main e verifichiamo che tenti di accedere a 'RepositoryMining2' e sollevi FileNotFoundError
        with pytest.raises(FileNotFoundError,
                           match=r"No such directory: '/Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2'"):
            main()

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 1}, {
                 'file_contents': {
                     'FilteredTextMining.txt': '''{'package': 723, 'org': 16, 'apache': 32, 'shiro': 24, 'web': 1650, 'util': 986, 'import': 584}'''}})
        ],
        indirect=True
    )
    def test_case_6(self, mock_file_system, mock_os_functions):
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results'].add("FilteredTextMining.txt")
        mock_chdir, mock_open = mock_os_functions
        main()
        text_mining_absent = all("text_mining.txt" not in call[0][0] for call in mock_open.call_args_list)
        assert text_mining_absent, "La sottostringa 'text_mining.txt' è presente nelle chiamate a open."
        assert mock_chdir.call_count == 70
        assert mock_open().write.call_args_list == [call('NameClass'), call(' ,apache'), call(' ,import'), call(' ,org'), call(' ,package'), call(' ,shiro'), call(' ,util'), call(' ,web'), call(' ,class'), call('\n\n')]

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id': "errore.txt"}, {
                 'file_contents': {
                     'FilteredTextMining.txt': '''{'package': 723, 'org': 16, 'apache': 32, 'shiro': 24, 'web': 1650, 'util': 986, 'import': 584}'''}})
        ],
        indirect=True
    )
    def test_case_7(self, mock_file_system, mock_os_functions):
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results'].add("FilteredTextMining.txt")
        with pytest.raises(NotADirectoryError, match=r"Not a directory: 'errore.txt'"):
            main()
        mock_chdir, mock_open = mock_os_functions
        assert mock_chdir.call_count == 4

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id': "CHECK.txt"}, {
                 'file_contents': {
                     'FilteredTextMining.txt': '''{'package': 723, 'org': 16, 'apache': 32, 'shiro': 24, 'web': 1650, 'util': 986, 'import': 584}'''}})
        ],
        indirect=True
    )
    def test_case_8(self, mock_file_system, mock_os_functions):
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results'].add("FilteredTextMining.txt")
        mock_chdir, mock_open = mock_os_functions
        main()
        text_mining_absent = all("text_mining.txt" not in call[0][0] for call in mock_open.call_args_list)
        assert text_mining_absent, "La sottostringa 'text_mining.txt' è presente nelle chiamate a open."
        assert mock_chdir.call_count == 70
        assert mock_open().write.call_args_list == [call('NameClass'), call(' ,apache'), call(' ,import'), call(' ,org'), call(' ,package'), call(' ,shiro'), call(' ,util'), call(' ,web'), call(' ,class'), call('\n\n')]


    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 1, 'cvd_id': "cvd_id1"}, {
                 'file_contents': {
                     'FilteredTextMining.txt': '''{'package': 723, 'org': 16, 'apache': 32, 'shiro': 24, 'web': 1650, 'util': 986, 'import': 584}'''}})
        ],
        indirect=True
    )
    def test_case_9(self, mock_file_system, mock_os_functions):
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results'].add("FilteredTextMining.txt")
        mock_chdir, mock_open = mock_os_functions
        main()
        text_mining_absent = all("text_mining.txt" not in call[0][0] for call in mock_open.call_args_list)
        assert text_mining_absent, "La sottostringa 'text_mining.txt' è presente nelle chiamate a open."
        assert mock_chdir.call_count == 138
        assert mock_open().write.call_args_list == [call('NameClass'), call(' ,apache'), call(' ,import'), call(' ,org'), call(' ,package'), call(' ,shiro'), call(' ,util'), call(' ,web'), call(' ,class'), call('\n\n')]

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'cvd_id': "cvd_id1", 'folder': "errore.txt"}, {
                 'file_contents': {
                     'FilteredTextMining.txt': '''{'package': 723, 'org': 16, 'apache': 32, 'shiro': 24, 'web': 1650, 'util': 986, 'import': 584}'''}})
        ],
        indirect=True
    )
    def test_case_10(self, mock_file_system, mock_os_functions):
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results'].add("FilteredTextMining.txt")
        with pytest.raises(NotADirectoryError, match=r"Not a directory: 'errore.txt'"):
            main()
        mock_chdir, mock_open = mock_os_functions
        assert mock_chdir.call_count == 5

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'cvd_id': "cvd_id1", 'folder': ".DS_Store"}, {
                 'file_contents': {
                     'FilteredTextMining.txt': '''{'package': 723, 'org': 16, 'apache': 32, 'shiro': 24, 'web': 1650, 'util': 986, 'import': 584}'''}})
        ],
        indirect=True
    )
    def test_case_11(self, mock_file_system, mock_os_functions):
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results'].add("FilteredTextMining.txt")
        mock_chdir, mock_open = mock_os_functions
        main()
        text_mining_absent = all("text_mining.txt" not in call[0][0] for call in mock_open.call_args_list)
        assert text_mining_absent, "La sottostringa 'text_mining.txt' è presente nelle chiamate a open."
        assert mock_chdir.call_count == 138
        assert mock_open().write.call_args_list == [call('NameClass'), call(' ,apache'), call(' ,import'), call(' ,org'), call(' ,package'), call(' ,shiro'), call(' ,util'), call(' ,web'), call(' ,class'), call('\n\n')]

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 1, 'cvd_id': "cvd_id1", 'folder': "folder1"}, {
                 'file_contents': {
                     'FilteredTextMining.txt': '''{'package': 723, 'org': 16, 'apache': 32, 'shiro': 24, 'web': 1650, 'util': 986, 'import': 584}'''}})
        ],
        indirect=True
    )
    def test_case_12(self, mock_file_system, mock_os_functions):
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results'].add("FilteredTextMining.txt")
        mock_chdir, mock_open = mock_os_functions
        main()
        text_mining_absent = all("text_mining.txt" not in call[0][0] for call in mock_open.call_args_list)
        assert text_mining_absent, "La sottostringa 'text_mining.txt' è presente nelle chiamate a open."
        assert mock_chdir.call_count == 206
        assert mock_open().write.call_args_list == [call('NameClass'), call(' ,apache'), call(' ,import'), call(' ,org'), call(' ,package'), call(' ,shiro'), call(' ,util'), call(' ,web'), call(' ,class'), call('\n\n')]

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1", 'file': 'Example.java_text_mining.txt'}, {
                 'file_contents': {
                     'FilteredTextMining.txt': '''{'package': 723, 'java': 16, 'apache': 32, 'sdk': 24, 'web': 1650, 'util': 986, 'import': 584, 'com': 180, 'static': 70}''',
                 'Example.java_text_mining.txt': '''{'package': 1, 'com': 18, 'apache': 5, 'sdk': 2, 'import': 23, 'java': 6, 'util': 13}'''}})
        ],
        indirect=True
    )
    def test_case_13(self, mock_file_system, mock_os_functions):
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results'].add("FilteredTextMining.txt")
        _, mock_open = mock_os_functions
        main()

        write_calls = mock_open().write.call_args_list
        actual_string = ''.join(call[0][0] for call in write_calls)

        # Definisci la stringa di output attesa
        expected_string = ('NameClass ,apache ,com ,import ,java ,package ,sdk ,static ,util ,web '
         ',class\n'
         '\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, pos\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, pos\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, pos\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, pos\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, pos\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, pos\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, pos\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, pos\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, pos\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, pos\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, pos\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, pos\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, pos\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, pos\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, pos\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, pos\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, pos\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, neg\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, neg\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, neg\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, neg\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, neg\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, neg\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, neg\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, neg\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, neg\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, neg\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, neg\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, neg\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, neg\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, neg\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, neg\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, neg\n'
         'folder1/Example.java_,5,18,23,6,1,2,0,13,0, neg\n')

        assert actual_string == expected_string
        text_mining_substring_present = any("text_mining.txt" in call[0][0] for call in mock_open.call_args_list)
        assert text_mining_substring_present, "La sottostringa 'text_mining.txt' non è presente nelle chiamate a open."

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'Example.java_text_mining.txt'}, {
                 'file_contents': {
                     'FilteredTextMining.txt': '''{'package': 723, 'java': 16, 'apache': 32, 'sdk': 24, 'web': 1650, 'util': 986, 'import': 584, 'com': 180, 'static': 70}''',
                     'Example.java_text_mining.txt': '''{'package': 1, 'com': 18, 'apache': 5, 'sdk': 2, 'import': 23, 'java': 6, 'util': 13}'''},
                 'file_to_fail': 'csv_mining_final.csv', 'type_error': 'perm_error'})
        ],
        indirect=True
    )
    def test_case_14(self, mock_file_system, mock_os_functions):
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results'].add("FilteredTextMining.txt")
        with pytest.raises(PermissionError):  # dovuto ad ast
            main()

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'Example.java_text_mining.txt'}, {
                 'file_contents': {
                     'FilteredTextMining.txt': '''{'package': 723, 'java': 16, 'apache': 32, 'sdk': 24, 'web': 1650, 'util': 986, 'import': 584, 'com': 180, 'static': 70}''',
                     'Example.java_text_mining.txt': '''{}'''}})
        ],
        indirect=True
    )
    def test_case_15(self, mock_file_system, mock_os_functions):
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results'].add("FilteredTextMining.txt")
        _, mock_open = mock_os_functions
        main()
        write_calls = mock_open().write.call_args_list
        actual_string = ''.join(call[0][0] for call in write_calls)

        # Definisci la stringa di output attesa
        expected_string = ('NameClass ,apache ,com ,import ,java ,package ,sdk ,static ,util ,web '
         ',class\n'
         '\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, pos\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, pos\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, pos\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, pos\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, pos\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, pos\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, pos\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, pos\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, pos\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, pos\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, pos\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, pos\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, pos\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, pos\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, pos\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, pos\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, pos\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, neg\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, neg\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, neg\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, neg\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, neg\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, neg\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, neg\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, neg\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, neg\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, neg\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, neg\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, neg\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, neg\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, neg\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, neg\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, neg\n'
         'folder1/Example.java_,0,0,0,0,0,0,0,0,0, neg\n')

        assert actual_string == expected_string

        text_mining_substring_present = any("text_mining.txt" in call[0][0] for call in mock_open.call_args_list)
        assert text_mining_substring_present, "La sottostringa 'text_mining.txt' non è presente nelle chiamate a open."

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'Example.java_text_mining.txt'}, {
                 'file_contents': {
                     'FilteredTextMining.txt': '''{'package': 723, 'java': 16, 'apache': 32, 'sdk': 24, 'web': 1650, 'util': 986, 'import': 584, 'com': 180, 'static': 70}''',
                     'Example.java_text_mining.txt': '''[1,2,3]'''}})
        ],
        indirect=True
    )
    def test_case_16(self, mock_file_system, mock_os_functions):
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results'].add("FilteredTextMining.txt")
        mock_chdir, mock_open = mock_os_functions
        print(mock_open.call_args_list)
        with pytest.raises(TypeError):
            main()
        text_mining_substring_present = any("text_mining.txt" in call[0][0] for call in mock_open.call_args_list)
        assert text_mining_substring_present, "La sottostringa 'text_mining.txt' non è presente nelle chiamate a open."

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'Example.java_text_mining.txt'}, {
                 'file_contents': {
                     'FilteredTextMining.txt': '''{'package': 723, 'org': 16, 'apache': 32, 'shiro': 24, 'web': 1650, 'util': 986, 'import': 584}'''}, 'file_to_fail': 'Example.java_text_mining.txt', 'type_error': 'access_error'})
        ],
        indirect=True
    )
    def test_case_17(self, mock_file_system, mock_os_functions):
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results'].add("FilteredTextMining.txt")
        mock_chdir, mock_open = mock_os_functions
        with pytest.raises(PermissionError):
            main()
        text_mining_absent = all("text_mining.txt" not in call[0][0] for call in mock_open.call_args_list)
        assert text_mining_absent, "La sottostringa 'text_mining.txt' è presente nelle chiamate a open."
        assert mock_chdir.call_count == 5

    @patch('builtins.print')
    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': '.DS_Store'}, {
                 'file_contents': {'FilteredTextMining.txt': '''{'package': 723, 'org': 16, 'apache': 32, 'shiro': 24, 'web': 1650, 'util': 986, 'import': 584}'''}})
        ],
        indirect=True
    )
    def test_case_18(self, mock_print, mock_file_system, mock_os_functions):
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results'].add("FilteredTextMining.txt")
        mock_chdir, mock_open = mock_os_functions
        main()
        text_mining_absent = all("text_mining.txt" not in call[0][0] for call in mock_open.call_args_list)
        assert text_mining_absent, "La sottostringa 'text_mining.txt' è presente nelle chiamate a open."
        assert mock_chdir.call_count == 206
        mock_print.assert_any_call(".DS_Store occured")
        assert mock_open().write.call_args_list == [call('NameClass'), call(' ,apache'), call(' ,import'), call(' ,org'), call(' ,package'), call(' ,shiro'), call(' ,util'), call(' ,web'), call(' ,class'), call('\n\n')]

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'another_folder'}, {
                 'file_contents': {
                     'FilteredTextMining.txt': '''{'package': 723, 'org': 16, 'apache': 32, 'shiro': 24, 'web': 1650, 'util': 986, 'import': 584}'''}})
        ],
        indirect=True
    )
    def test_case_19(self, mock_file_system, mock_os_functions):
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results'].add("FilteredTextMining.txt")
        mock_chdir, mock_open = mock_os_functions
        main()
        text_mining_absent = all("text_mining.txt" not in call[0][0] for call in mock_open.call_args_list)
        assert text_mining_absent, "La sottostringa 'text_mining.txt' è presente nelle chiamate a open."
        assert mock_chdir.call_count == 206
        assert mock_open().write.call_args_list == [call('NameClass'), call(' ,apache'), call(' ,import'), call(' ,org'), call(' ,package'), call(' ,shiro'), call(' ,util'), call(' ,web'), call(' ,class'), call('\n\n')]