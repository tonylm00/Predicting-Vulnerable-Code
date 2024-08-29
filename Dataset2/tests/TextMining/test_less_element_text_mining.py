import pytest
from unittest.mock import patch, mock_open
from Dataset2.Text_Mining.less_element_text_mining import initialize, splitCamelCase, writeToFile

class TestInitialize:

    @pytest.mark.parametrize('mock_chdir', [{'path_to_fail': 'mining_results', 'error_type': 'FileNotFoundError'}], indirect=True)
    @pytest.mark.parametrize('mock_getcwd', [{'path_to_return': '/Predicting-Vulnerable-Code/Dataset2/Text_Mining'}], indirect=True)
    def test_case_1(self, mock_chdir, mock_getcwd):
        with pytest.raises(FileNotFoundError):
            initialize()

    @pytest.mark.parametrize('mock_chdir', [{}], indirect=True)
    @pytest.mark.parametrize('mock_listdir', [{}], indirect=True)
    @pytest.mark.parametrize('mock_getcwd', [{'path_to_return': '/Predicting-Vulnerable-Code/Dataset2/Text_Mining'}], indirect=True)
    def test_case_2(self, mock_chdir, mock_listdir, mock_getcwd):
        with patch('builtins.open', mock_open()) as mock_file:
            initialize()

            mock_file.assert_not_called()

    @pytest.mark.parametrize('mock_chdir', [{}], indirect=True)
    @pytest.mark.parametrize('mock_listdir', [{'path_to_return_with_file': True}], indirect=True)
    @pytest.mark.parametrize('mock_getcwd', [{'path_to_return': '/Predicting-Vulnerable-Code/Dataset2/Text_Mining'}],
                             indirect=True)
    @pytest.mark.parametrize('mock_open_file', [{'file_content': '''{'package': 1, 'org': 4, 'apache': 4, 'import': 7, 'AccessControlFilter': 2, 'Logger': 2, 'LoggerFactory': 2, 'HttpServletResponse': 2}'''}], indirect=True)
    def test_case_3(self, mock_chdir, mock_listdir, mock_getcwd, mock_open_file):
        expected_output = {'package': 1, 'org': 4, 'apache': 4, 'import': 7, 'access': 2, 'control': 2, 'factory': 2, 'filter': 2, 'logger': 4, 'http': 2, 'servlet': 2, 'response': 2}
        output = initialize()
        assert expected_output == output, f"Il dizionario restituito è {output} invece di {expected_output}."

    @pytest.mark.parametrize('mock_chdir', [{}], indirect=True)
    @pytest.mark.parametrize('mock_listdir', [{'path_to_return_with_file': True}], indirect=True)
    @pytest.mark.parametrize('mock_getcwd', [{'path_to_return': '/Predicting-Vulnerable-Code/Dataset2/Text_Mining'}],
                             indirect=True)
    @pytest.mark.parametrize('mock_open_file', [{'file_content': '''{'CamelCase': None, 'AnotherTest': 'string_value', 'validKey': 5}'''}],
                             indirect=True)
    def test_case_4(self, mock_chdir, mock_listdir, mock_getcwd, mock_open_file):
        expected_output = {'camel': None, 'case': None, 'another': 'string_value', 'test': 'string_value', 'valid': 5, 'key': 5}
        output = initialize()
        assert expected_output == output, f"Il dizionario restituito è {output} invece di {expected_output}."

    @pytest.mark.parametrize('mock_chdir', [{}], indirect=True)
    @pytest.mark.parametrize('mock_listdir', [{'path_to_return_with_file': True}], indirect=True)
    @pytest.mark.parametrize('mock_getcwd', [{'path_to_return': '/Predicting-Vulnerable-Code/Dataset2/Text_Mining'}],
                             indirect=True)
    @pytest.mark.parametrize('mock_open_file', [{'file_content': ''}],
                             indirect=True)
    def test_case_5(self, mock_chdir, mock_listdir, mock_getcwd, mock_open_file):
        with pytest.raises(SyntaxError):  # ast legge un file vuoto, EOFError
            initialize()

    @pytest.mark.parametrize('mock_chdir', [{}], indirect=True)
    @pytest.mark.parametrize('mock_listdir', [{'path_to_return_with_file': True}], indirect=True)
    @pytest.mark.parametrize('mock_getcwd', [{'path_to_return': '/Predicting-Vulnerable-Code/Dataset2/Text_Mining'}],
                             indirect=True)
    @pytest.mark.parametrize('mock_open_file', [{'file_to_fail': 'text_mining_dict.txt', 'error_type': 'PermissionError'}],
                             indirect=True)
    def test_case_6(self, mock_chdir, mock_listdir, mock_getcwd, mock_open_file):
        with pytest.raises(PermissionError):
            initialize()

    @patch('builtins.print')
    @pytest.mark.parametrize('mock_chdir', [{}], indirect=True)
    @pytest.mark.parametrize('mock_listdir', [{'path_to_return_mixed': True}], indirect=True)
    @pytest.mark.parametrize('mock_getcwd', [{'path_to_return': '/Predicting-Vulnerable-Code/Dataset2/Text_Mining'}],
                             indirect=True)
    def test_case_7(self,  mock_print, mock_chdir, mock_listdir, mock_getcwd):
        initialize()

        assert mock_print.call_count == 4
        mock_print.assert_any_call("File doesn't exist, sorry :(")

class TestSplitCamelCase:
    def test_case_1(self):
        input_dict = {}
        expected_output = {}
        result = splitCamelCase(input_dict)
        assert result == expected_output, f"Expected {expected_output}, but got {result}"

    def test_case_2(self):
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
        result = splitCamelCase(input_dict)
        assert result == expected_output, f"Expected {expected_output}, but got {result}"

    def test_case_3(self):
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
        result = splitCamelCase(input_dict)
        assert result == expected_output, f"Expected {expected_output}, but got {result}"

    def test_case_4(self):
        input_dict = {
            'CamelCaseKey': 4,
            'lowercasekey': 2,
            'AnotherCamelCase': 3
        }
        expected_output = {
            'camel': 7,
            'case': 7,
            'key': 4, #non somma le key presenti nelle parole non camelcase
            'lowercasekey': 2,
            'another': 3
        }
        result = splitCamelCase(input_dict)
        assert result == expected_output, f"Expected {expected_output}, but got {result}"

    def test_case_5(self):
        input_dict = {
            'CamelCase': None,
            'AnotherTest': 'string_value',
            'validKey': 5
        }
        expected_output = {'camel': None, 'case': None, 'another': 'string_value', 'test': 'string_value', 'valid': 5, 'key': 5}
        output = splitCamelCase(input_dict)
        assert output == expected_output, f"Expected {expected_output}, but got {output}"

    def test_case_6(self):
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
        result = splitCamelCase(input_dict)
        assert result == expected_output, f"Expected {expected_output}, but got {result}"

    def test_case_7(self):
        input_dict = {
            'CamelCase': None,
            'AnotherCaseTest': 'string_value',
            'validKey': 5
        }
        with pytest.raises(TypeError):
            splitCamelCase(input_dict)


    def test_case_8(self):
        input_dict = {
             1: 2,
            'AnotherCaseTest': 3,
            'validKey': 5
        }
        with pytest.raises(TypeError):
            splitCamelCase(input_dict)

    def test_case_9(self):
        input_dict = ['ad', 1]
        with pytest.raises(TypeError):
            splitCamelCase(input_dict)



class TestWriteToFile:
    @pytest.mark.parametrize('mock_open_file', [{'file_to_fail': 'FilteredTextMining.txt', 'error_type': 'PermissionError'}], indirect=True)
    def test_case_1(self, mock_open_file):
        with pytest.raises(PermissionError):
            writeToFile({'key': 2, 'import': 4})

    @pytest.mark.parametrize('mock_open_file', [{}], indirect=True)
    def test_case_2(self, mock_open_file):
        writeToFile({'key': 2, 'import': 4})
        mock_open_file.assert_called_once_with('FilteredTextMining.txt', 'w+')
        mock_open_file().write.assert_called_once_with("{'key': 2, 'import': 4}")

    @pytest.mark.parametrize('mock_open_file', [{'file_to_fail': 'FilteredTextMining.txt', 'error_on_write': PermissionError}], indirect=True)
    def test_case_3(self, mock_open_file):
        with pytest.raises(PermissionError):
            writeToFile({'key': 2, 'import': 4})

        mock_open_file.assert_called_once_with('FilteredTextMining.txt', 'w+')

    @pytest.mark.parametrize('mock_open_file', [{}], indirect=True)
    def test_case_4(self, mock_open_file):
        writeToFile({})
        mock_open_file.assert_called_once_with('FilteredTextMining.txt', 'w+')
        mock_open_file().write.assert_called_once_with("{}")

    @pytest.mark.parametrize('mock_open_file',
                             [{'file_to_fail': 'FilteredTextMining.txt', 'error_on_write': PermissionError}],
                             indirect=True)
    def test_case_5(self, mock_open_file):
        with pytest.raises(PermissionError):
            writeToFile({})

        mock_open_file.assert_called_once_with('FilteredTextMining.txt', 'w+')

    @pytest.mark.parametrize('mock_open_file', [{}], indirect=True)
    def test_case_6(self, mock_open_file):
        writeToFile({
            1: None,
            'uppercase': 2,
            '2': 'ciao'
        })
        mock_open_file.assert_called_once_with('FilteredTextMining.txt', 'w+')
        mock_open_file().write.assert_called_once_with("{1: None, 'uppercase': 2, '2': 'ciao'}")

    @pytest.mark.parametrize('mock_open_file',
                             [{'file_to_fail': 'FilteredTextMining.txt', 'error_on_write': PermissionError}],
                             indirect=True)
    def test_case_7(self, mock_open_file):
        with pytest.raises(PermissionError):
            writeToFile({
            1: None,
            'uppercase': 2,
            '2': 'ciao'
        })

        mock_open_file.assert_called_once_with('FilteredTextMining.txt', 'w+')

    @pytest.mark.parametrize('mock_open_file', [{}], indirect=True)
    def test_case_8(self, mock_open_file):
        writeToFile(['prova', 'tipologia', 'diversa'])
        mock_open_file.assert_called_once_with('FilteredTextMining.txt', 'w+')
        mock_open_file().write.assert_called_once_with("['prova', 'tipologia', 'diversa']")

    @pytest.mark.parametrize('mock_open_file',
                             [{'file_to_fail': 'FilteredTextMining.txt', 'error_on_write': PermissionError}],
                             indirect=True)
    def test_case_9(self, mock_open_file):
        with pytest.raises(PermissionError):
            writeToFile(['prova', 'tipologia', 'diversa'])

        mock_open_file.assert_called_once_with('FilteredTextMining.txt', 'w+')