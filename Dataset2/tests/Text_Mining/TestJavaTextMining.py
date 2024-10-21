import re
import pytest
from Dataset2.Text_Mining.JavaTextMining import JavaTextMining

class TestJavaTextMining:
    class TestRemoveNotAlpha:
        def test_case_1(self):
            miner = JavaTextMining("path_test")
            tokens = []
            output = miner.removeNotAlpha(tokens)
            assert len(output) == 0, f"Test fallito, la lista risultante {output} non è vuota"

        def test_case_2(self):
            miner = JavaTextMining("path_test")
            tokens = ["class", "public", "int", "String", "try", "catch", "main", "final", "while", "return"]
            output = miner.removeNotAlpha(tokens)
            assert output == tokens, f"Test fallito, {output} != {tokens}"

        def test_case_3(self):
            miner = JavaTextMining("path_test")
            tokens = ["main1", "while2", "return4", "if1else", "for3", "abstract4"]
            output = miner.removeNotAlpha(tokens)
            assert len(output) == 0, f"Test fallito: {output} non è vuoto"

        def test_case_4(self):
            miner = JavaTextMining("path_test")
            tokens = ["class", "public", "int", "String", "try", "catch", "main1", "final", "while2", "return",
                      "if1else", "for3", "abstract4"]

            expected_output = ["class", "public", "int", "String", "try", "catch", "final", "return"]
            actual_output = miner.removeNotAlpha(tokens)
            assert actual_output == expected_output, f"Test fallito: {actual_output} != {expected_output}"

    #corretti i test che fallivano per lo spostamento della logica di eliminazione dei commenti
    class TestStringTokenizer:
        def test_case_1(self):
            miner = JavaTextMining("path_test")
            s = ""
            output = miner.stringTokenizer(s)
            assert output == [], f"Test fallito per stringa vuota. Output ottenuto: {output}"

        def test_case_2(self):
            miner = JavaTextMining("path_test")
            s = "int main() { return 0; }"
            output = miner.stringTokenizer(s)
            assert output == ["int", "main",
                              "return"], f"Test fallito per stringa senza costanti o commenti. Output ottenuto: {output}"

        def test_case_3(self):
            miner = JavaTextMining("path_test")
            s = "// This is a comment\n /* This is another block comment \n that spans multiple lines */"
            output = miner.stringTokenizer(s)
            assert output == ['This', 'is', 'a', 'comment', 'This', 'is', 'another', 'block', 'comment', 'that',
                        'spans', 'multiple', 'lines'], f"Test fallito per stringa con solo commenti. Output ottenuto: {output}"

        def test_case_4(self):
            miner = JavaTextMining("path_test")
            s = " \"Testiamo le costanti stringhe\""
            output = miner.stringTokenizer(s)
            print(output)
            assert output == [], f"Test fallito per stringa con solo costanti stringhe. Output ottenuto: {output}"

        def test_case_5(self):
            miner = JavaTextMining("path_test")
            s = "string main() {// comment \n return \"Test passato\"} "
            output = miner.stringTokenizer(s)
            assert output == ["string", "main", "comment",
                                "return"], f"Test fallito per stringa con costanti e commenti. Output ottenuto: {output}"

        def test_case_6(self):
            miner = JavaTextMining("path_test")
            s = "string main() {// comment \n return \"// Test passato\"} "
            output = miner.stringTokenizer(s)
            assert output == ["string", "main", "comment",
                              "return"], f"Test fallito per stringa con costanti e commenti. Output ottenuto: {output}"

    #corretti i test che fallivano per lo spostamento della logica di eliminazione dei commenti
    class TestRemoveComments:
        def test_case_1(self, mock_file_read_permission_error):
            miner = JavaTextMining("path_test")
            with pytest.raises(PermissionError):
                miner.removeComments(mock_file_read_permission_error)

        @pytest.mark.parametrize(
            'mock_file_with_content',
            [""],
            indirect=True
        )
        def test_case_2(self, mock_file_with_content):
            miner = JavaTextMining("path_test")
            result = miner.removeComments(mock_file_with_content)
            assert result == '', "Expected empty string but got: " + result

        @pytest.mark.parametrize(
            'mock_file_with_content',
            ['public class Test { public static void main(String[] args) { System.out.println("Hello World"); } }'],
            indirect=True
        )
        def test_case_3(self, mock_file_with_content):
            miner = JavaTextMining("path_test")
            result = miner.removeComments(mock_file_with_content)
            expected_output = 'public class Test { public static void main(String[] args) { System.out.println("Hello World"); } }'
            assert result == expected_output, "Expected unchanged code but got: " + result

        # non considera i commenti single line
        @pytest.mark.parametrize(
            'mock_file_with_content',
            ['''
                /* This is a comment */
                // Another comment 
                '''],
            indirect=True
        )
        def test_case_4(self, mock_file_with_content):
            miner = JavaTextMining("path_test")
            result = miner.removeComments(mock_file_with_content)
            assert re.sub(r'\s+', ' ',
                          result).strip() == '', "Expected spaces for removed comments but got: " + result

        # non considera i commenti single line
        @pytest.mark.parametrize(
            'mock_file_with_content',
            ['''
                public class Test { 
                    /* This is a comment */ 
                    public static void main(String[] args) { 
                        // Single line comment
                        System.out.println("Hello World"); /* Inline comment */
                        bool test = true;
                    } 
                }
                '''],
            indirect=True
        )
        def test_case_5(self, mock_file_with_content):
            miner = JavaTextMining("path_test")
            expected_output = '''
                public class Test { 
                    public static void main(String[] args) {
                        System.out.println("Hello World"); 
                        bool test = true;
                    } 
                }
            '''
            result = miner.removeComments(mock_file_with_content)
            assert re.sub(r'\s+', ' ', result).strip() == re.sub(r'\s+', ' ',
                                                                 expected_output).strip(), "Expected code without comments but got: " + result

    class TestTakeJavaClass:
        @pytest.mark.parametrize('mock_open_file',
                                 [{'file_to_fail': 'non_existent_file.java', 'error_type': 'FileNotFoundError'}],
                                 indirect=True)
        def test_case_1(self, mock_open_file):
            miner = JavaTextMining('non_existent_file.java')
            with pytest.raises(FileNotFoundError):
                miner.takeJavaClass()

        # Test Case 2: File esistente con permessi limitati
        @pytest.mark.parametrize('mock_open_file',
                                 [{'file_to_fail': 'restricted_file.java', 'error_type': 'PermissionError'}],
                                 indirect=True)
        def test_case_2(self, mock_open_file):
            miner = JavaTextMining('restricted_file.java')
            with pytest.raises(PermissionError):
                miner.takeJavaClass()

        # Test Case 3: File esistente e accessibile con contenuto vuoto
        @pytest.mark.parametrize('mock_open_file', [{'file_content': ''}], indirect=True)
        def test_case_3(self, mock_open_file):
            miner = JavaTextMining("empty_file.java")
            result = miner.takeJavaClass()
            assert result == {}  # Dizionario vuoto

        # Test Case 4: File esistente e accessibile con parole diverse
        @pytest.mark.parametrize('mock_open_file', [{'file_content': '''void public main'''}], indirect=True)
        def test_case_4(self, mock_open_file):
            miner = JavaTextMining("different_words_file.java")
            result = miner.takeJavaClass()
            assert result == {"void": 1, "public": 1, "main": 1}

        # Test Case 5: File esistente e accessibile con parole ripetute
        @pytest.mark.parametrize('mock_open_file', [{'file_content': 'word word2 word int'}], indirect=True)
        def test_case_5(self, mock_open_file):
            miner = JavaTextMining("repeated_words_file.java")
            result = miner.takeJavaClass()
            assert result == {"word": 2, "int": 1}

        # Test Case 6: Apertura di una directory
        @pytest.mark.parametrize('mock_open_file',
                                 [{'file_to_fail': 'another_directory', 'error_type': 'IsADirectoryError'}],
                                 indirect=True)
        def test_case_6(self, mock_open_file):
            miner = JavaTextMining("another_directory")
            with pytest.raises(IsADirectoryError):
                miner.takeJavaClass()

    class TestMergeDict:
        def test_case_1(self):
            miner = JavaTextMining("path_test")
            dict1 = {"word": 2, "int": 1}
            dict2 = {"word": 1, "public": 1, "main": 1}
            result = miner.mergeDict(dict1, dict2)
            assert result == {"word": 3, "int": 1, "public": 1, "main": 1}

        def test_case_2(self):
            miner = JavaTextMining("path_test")
            dict1 = {"word": 2, "int": 1}
            dict2 = {}
            result = miner.mergeDict(dict1, dict2)
            assert result == {"word": 2, "int": 1}

        def test_case_3(self):
            miner = JavaTextMining("path_test")
            dict1 = {}
            dict2 = {"word": 1, "public": 1, "main": 1}
            result = miner.mergeDict(dict1, dict2)
            assert result == {"word": 1, "public": 1, "main": 1}

        def test_case_4(self):
            miner = JavaTextMining("path_test")
            dict1 = {}
            dict2 = {}
            result = miner.mergeDict(dict1, dict2)
            assert result == {}

        def test_case_5(self):
            miner = JavaTextMining("path_test")
            dict1 = {"word": 2, "int": 1}
            dict2 = "non sono un dizionario"
            with pytest.raises(TypeError):
                miner.mergeDict(dict1, dict2)

    class TestSplitDict:
        def test_case_1(self):
            miner = JavaTextMining("path_test")
            input_dict = {}
            expected_output = {}
            result = miner.splitDict(input_dict)
            assert result == expected_output, f"Expected {expected_output}, but got {result}"

        def test_case_2(self):
            miner = JavaTextMining("path_test")
            input_dict = {
                'CamelCase': 1,
                'SplitThis': 2,
                'AnotherTest': 3
            }
            expected_output = {
                'camel': 1,
                'case': 1,
                'split': 2,
                'this': 2,
                'another': 3,
                'test': 3
            }
            result = miner.splitDict(input_dict)
            assert result == expected_output, f"Expected {expected_output}, but got {result}"

        def test_case_3(self):
            miner = JavaTextMining("path_test")
            input_dict = {
                'lowercase': 1,
                'uppercase': 2,
                'allcaps': 3
            }
            expected_output = {
                'lowercase': 1,
                'uppercase': 2,
                'allcaps': 3
            }
            result = miner.splitDict(input_dict)
            assert result == expected_output, f"Expected {expected_output}, but got {result}"

        def test_case_4(self):
            miner = JavaTextMining("path_test")
            input_dict = {
                'CamelCaseKey': 4,
                'lowercasekey': 2,
                'AnotherCamelCase': 3
            }
            expected_output = {
                'camel': 7,
                'case': 7,
                'key': 4,  # non somma le key presenti nelle parole non camelcase
                'lowercasekey': 2,
                'another': 3
            }
            result = miner.splitDict(input_dict)
            assert result == expected_output, f"Expected {expected_output}, but got {result}"

        def test_case_5(self):
            miner = JavaTextMining("path_test")
            input_dict = {
                'CamelCase': None,
                'AnotherTest': 'string_value',
                'validKey': 5
            }
            expected_output = {'camel': None, 'case': None, 'another': 'string_value', 'test': 'string_value',
                               'valid': 5, 'key': 5}
            output = miner.splitDict(input_dict)
            assert output == expected_output, f"Expected {expected_output}, but got {output}"

        def test_case_6(self):
            miner = JavaTextMining("path_test")
            input_dict = {
                'lowercase': None,
                'uppercase': 2,
                '2': 'ciao'
            }
            expected_output = {
                'lowercase': None,
                'uppercase': 2,
                '2': 'ciao'
            }
            result = miner.splitDict(input_dict)
            assert result == expected_output, f"Expected {expected_output}, but got {result}"

        def test_case_7(self):
            miner = JavaTextMining("path_test")
            input_dict = {
                'CamelCase': None,
                'AnotherCaseTest': 'string_value',
                'validKey': 5
            }
            with pytest.raises(TypeError):
                miner.splitDict(input_dict)

        def test_case_8(self):
            miner = JavaTextMining("path_test")
            input_dict = {
                1: 2,
                'AnotherCaseTest': 3,
                'validKey': 5
            }
            with pytest.raises(TypeError):
                miner.splitDict(input_dict)

        def test_case_9(self):
            miner = JavaTextMining("path_test")
            input_dict = ['ad', 1]
            with pytest.raises(TypeError):
                miner.splitDict(input_dict)