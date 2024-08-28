import pytest
from Dataset2.Text_Mining.text_mining import removeNotAlpha, stringTokenizer, removeComments, takeJavaClass, main


class TestRemoveNotAlpha:
    def test_case_1(self):
        tokens = []

        output = removeNotAlpha(tokens)

        assert len(output) == 0, f"Test fallito, la lista risultante {output} non è vuota"

    def test_case_2(self):
        tokens = ["class", "public", "int", "String", "try", "catch", "main", "final", "while", "return"]

        output = removeNotAlpha(tokens)

        assert output == tokens, f"Test fallito, {output} != {tokens}"

    def test_case_3(self):
        tokens = ["main1", "while2", "return4", "if1else", "for3", "abstract4"]

        output = removeNotAlpha(tokens)

        assert len(output) == 0, f"Test fallito: {output} non è vuoto"

    def test_case_4(self):
        tokens = ["class", "public", "int", "String", "try", "catch", "main1", "final", "while2", "return", "if1else",
                  "for3", "abstract4"]

        expected_output = ["class", "public", "int", "String", "try", "catch", "final", "return"]

        actual_output = removeNotAlpha(tokens)

        assert actual_output == expected_output, f"Test fallito: {actual_output} != {expected_output}"

#Non vengono eliminati i commenti multilinea
class TestStringTokenizer:
    def test_case_1(self):
        s = ""
        output = stringTokenizer(s)
        assert output == [], f"Test fallito per stringa vuota. Output ottenuto: {output}"

    def test_case_2(self):
        s = "int main() { return 0; }"
        output = stringTokenizer(s)
        assert output == ["int", "main",
                          "return"], f"Test fallito per stringa senza costanti o commenti. Output ottenuto: {output}"

    #Fallito, non considera i commenti multilinea
    def test_case_3(self):
        s = "// this is a comment\n /* This is another block comment \n that spans multiple lines */"
        output = stringTokenizer(s)
        assert output == [], f"Test fallito per stringa con solo commenti. Output ottenuto: {output}"

    def test_case_4(self):
        s = " \"Testiamo le costanti stringhe\""
        output = stringTokenizer(s)
        assert output == [], f"Test fallito per stringa con solo costanti stringhe. Output ottenuto: {output}"

    def test_case_5(self):
        s = "string main() {// comment \n return \"Test passato\"} "
        output = stringTokenizer(s)
        assert output == ["string", "main",
                          "return"], f"Test fallito per stringa con costanti e commenti. Output ottenuto: {output}"


#I single line comment non vengono rimossi
class TestRemoveComment:
    def test_case_1(self, mock_file_read_permission_error):
        #java_file = io.StringIO(self.java_code)
        with pytest.raises(PermissionError):
            removeComments(mock_file_read_permission_error)

    @pytest.mark.parametrize(
        'mock_file_with_content',
        [""],
        indirect=True
    )
    def test_case_2(self, mock_file_with_content):
        result = removeComments(mock_file_with_content)
        assert result == '', "Expected empty string but got: " + result

    @pytest.mark.parametrize(
        'mock_file_with_content',
        ['public class Test { public static void main(String[] args) { System.out.println("Hello World"); } }'],
        indirect=True
    )
    def test_case_3(self, mock_file_with_content):
        result = removeComments(mock_file_with_content)
        expected_output = 'public class Test { public static void main(String[] args) { System.out.println("Hello World"); } }'
        assert result == expected_output, "Expected unchanged code but got: " + result

    #Fallisce
    @pytest.mark.parametrize(
        'mock_file_with_content',
        ['''
            /* This is a comment */
            // Another comment 
            '''],
        indirect=True
    )
    def test_case_4(self, mock_file_with_content):
        result = removeComments(mock_file_with_content)
        assert result == '', "Expected spaces for removed comments but got: " + result

    #Fallisce
    @pytest.mark.parametrize(
        'mock_file_with_content',
        ['''
            public class Test { 
                /* This is a comment */ 
                public static void main(String[] args) { 
                    // Single line comment
                    System.out.println("Hello World"); /* Inline comment */
                } 
            }
            '''],
        indirect=True
    )
    def test_case_5(self, mock_file_with_content):
        expected_output = '''
            public class Test { 

                public static void main(String[] args) { 
                    System.out.println("Hello World"); 
                } 
            }
            '''
        result = removeComments(mock_file_with_content)
        assert result.strip() == expected_output.strip(), "Expected code without comments but got: " + result

class TestTakeJavaClass:
    # Test Case 1: File inesistente
    @pytest.mark.parametrize('mock_open_file',
                             [{'file_to_fail': 'non_existent_file.java', 'error_type': 'FileNotFoundError'}],
                             indirect=True)
    def test_case_1(self, mock_open_file):
        with pytest.raises(FileNotFoundError):
            takeJavaClass("non_existent_file.java")

    # Test Case 2: File esistente con permessi limitati
    @pytest.mark.parametrize('mock_open_file',
                             [{'file_to_fail': 'restricted_file.java', 'error_type': 'PermissionError'}], indirect=True)
    def test_case_2(self, mock_open_file):
        with pytest.raises(PermissionError):
            takeJavaClass("restricted_file.java")

    # Test Case 3: File esistente e accessibile con contenuto vuoto
    @pytest.mark.parametrize('mock_open_file', [{'file_content': ''}], indirect=True)
    def test_case_3(self, mock_open_file):
        result = takeJavaClass("empty_file.java")
        assert result == {}  # Dizionario vuoto

    # Test Case 4: File esistente e accessibile con parole diverse
    @pytest.mark.parametrize('mock_open_file', [{'file_content': '''void public main'''}], indirect=True)
    def test_case_4(self, mock_open_file):
        result = takeJavaClass("different_words_file.java")
        assert result == {"void": 1, "public": 1, "main": 1}

    # Test Case 5: File esistente e accessibile con parole ripetute
    @pytest.mark.parametrize('mock_open_file', [{'file_content': 'word word2 word int'}], indirect=True)
    def test_case_5(self, mock_open_file):
        result = takeJavaClass("repeated_words_file.java")
        assert result == {"word": 2, "int": 1}

    # Test Case 6: Apertura di una directory
    @pytest.mark.parametrize('mock_open_file', [{'file_to_fail': 'another_directory', 'error_type': 'IsADirectoryError'}], indirect=True)
    def test_case_6(self, mock_open_file):
        with pytest.raises(IsADirectoryError):
            takeJavaClass("another_directory")

class TestMain:
    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cdv_id1", 'folder': "folder1", 'file': "Example.java"}, {}),  # Tutto ha contenuti
        ],
        indirect=['mock_file_system', 'mock_os_functions']
    )
    def test_case_1(self, mock_file_system, mock_os_functions):
        del mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results']
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2'] = []

        with pytest.raises(FileNotFoundError, match=r"No such directory: '/Predicting-Vulnerable-Code/Dataset2/mining_results'"):
            main()

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cdv_id1", 'folder': "folder1", 'file': "Example.java"}, {}),  # Tutto ha contenuti
        ],
        indirect=['mock_file_system', 'mock_os_functions']
    )
    def test_case_2(self, mock_file_system, mock_os_functions):
        # 'mining_results' esiste, ma rimuoviamo una repository specifica, ad esempio 'RepositoryMining2'
        #mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results'].remove('RepositoryMining2')
        del mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2']
        mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results'].remove("RepositoryMining2")

        # Eseguiamo main e verifichiamo che tenti di accedere a 'RepositoryMining2' e sollevi FileNotFoundError
        with pytest.raises(FileNotFoundError, match=r"No such directory: '/Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2'"):
            main()

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 1}, {})
        ],
        indirect=True
    )
    def test_case_3(self, mock_file_system, mock_os_functions):

        # Eseguiamo main. In questo caso, main dovrebbe attraversare la directory senza errori, ma non fare nulla.
        main()
        assert mock_file_system['/Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2'] == [], f"è stato creato il file di test_mining"

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id': "file.txt"}, {})
        ],
        indirect=True
    )
    def test_case_4(self, mock_file_system, mock_os_functions):
        with pytest.raises(NotADirectoryError,match=r"Not a directory: 'file.txt'"):
            main()

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id': "CHECK.txt"}, {})
        ],
        indirect=True
    )
    def test_case_5(self, mock_file_system, mock_os_functions):
        main()
        for files in mock_file_system.values():
            for file in files:
                assert not file.endswith("text_mining.txt"), f"File ending with 'text_mining.txt' found: {file}"

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty':1, 'cvd_id': "cvd_id1"}, {})
        ],
        indirect=True
    )
    def test_case_6(self, mock_file_system, mock_os_functions):
        main()
        assert mock_file_system[
                   '/Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id1'] == [], f"è stato creato il file di test_mining"

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

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'cvd_id': "cvd_id1", 'folder': ".DS_Store"}, {})
        ],
        indirect=True
    )
    def test_case_8(self, mock_file_system, mock_os_functions):
        main()
        for files in mock_file_system.values():
            for file in files:
                assert not file.endswith("text_mining.txt"), f"File ending with 'text_mining.txt' found: {file}"

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 1, 'cvd_id': "cvd_id1", 'folder': "folder1"}, {})
        ],
        indirect=True
    )
    def test_case_9(self, mock_file_system, mock_os_functions):
        main()
        assert mock_file_system[
                   '/Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id1/folder1'] == [], f"è stato creato il file di test_mining"

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1", 'file':'Example.java'},
             {'file_content': '''
            public class Test { 
                /* This is a comment */ 
                public static void main(String[] args) { 
                    // Single line comment
                    System.out.println("Hello World"); /* Inline comment */
                } 
            }
            '''}
            )
        ],
        indirect=True
    )
    def test_case_10(self, mock_file_system, mock_os_functions):
        main()

        # Verifichiamo che il file di text mining sia stato creato
        expected_file = 'Example.java_text_mining.txt'
        assert expected_file in mock_file_system[
            '/Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id1/folder1'], f"Il file {expected_file} avrebbe dovuto essere creato."

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'Example.java'},
             {'file_content': '''
                public class Test { 
                    /* This is a comment */ 
                    public static void main(String[] args) { 
                        // Single line comment
                        System.out.println("Hello World"); /* Inline comment */
                    } 
                }
                ''', 'type_error': 'perm_error'}
             )
        ],
        indirect=True
    )
    def test_case_11(self, mock_file_system, mock_os_functions):
        with pytest.raises(PermissionError):
            main()

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'Example.java'},
             {'file_content': '''
                    public class Test { 
                        /* This is a comment */ 
                        public static void main(String[] args) { 
                            // Single line comment
                            System.out.println("Hello World"); /* Inline comment */
                        } 
                    }
                    ''', 'type_error': 'value_error'}
             )
        ],
        indirect=True
    )
    def test_case_12(self, mock_file_system, mock_os_functions):
        with pytest.raises(TypeError):
            main()

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'Example.java'},
             {'file_content': '''
                        public class Test { 
                            /* This is a comment */ 
                            public static void main(String[] args) { 
                                // Single line comment
                                System.out.println("Hello World"); /* Inline comment */
                            } 
                        }
                        ''', 'type_error': 'access_error'}
            )
        ],
        indirect=True
    )
    def test_case_13(self, mock_file_system, mock_os_functions):
        with pytest.raises(PermissionError):
            main()

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': '.DS_Store'},
             {'file_content': '''
                            public class Test { 
                                /* This is a comment */ 
                                public static void main(String[] args) { 
                                    // Single line comment
                                    System.out.println("Hello World"); /* Inline comment */
                                } 
                            }
                            ''', 'type_error': 'access_error'}
             )
        ],
        indirect=True
    )
    def test_case_14(self, mock_file_system, mock_os_functions):
        main()
        for files in mock_file_system.values():
            for file in files:
                assert not file.endswith("text_mining.txt"), f"File ending with 'text_mining.txt' found: {file}"

    @pytest.mark.parametrize(
        'mock_file_system, mock_os_functions',
        [
            ({'repo_empty': 2, 'cvd_id_empty': 2, 'folder_empty': 2, 'cvd_id': "cvd_id1", 'folder': "folder1",
              'file': 'another_folder'},
             {'type_error': 'directory_error'}
             )
        ],
        indirect=True
    )
    def test_case_15(self, mock_file_system, mock_os_functions):
        with pytest.raises(IsADirectoryError):
            main()


