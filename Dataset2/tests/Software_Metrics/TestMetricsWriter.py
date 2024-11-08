from unittest.mock import patch, MagicMock, mock_open
import pytest
from Dataset2.Software_Metrics.MetricsWriter import MetricsWriter

class TestMetricsWriter:
    class TestWriteHeader:
        def test_case_1(self):
            writer = MetricsWriter(None)
            with pytest.raises(TypeError):
                writer.write_header()

        @patch("builtins.print")
        def test_case_2(self, mock_print):
            writer = MetricsWriter("")
            writer.write_header()
            mock_print.assert_any_call("Errore durante l'apertura del file: [Errno 2] No such file or directory: ''")

        @patch("builtins.open", new_callable=mock_open)
        @patch("builtins.print")
        def test_case_3(self, mock_print, mock_file):
            writer = MetricsWriter("test.csv")
            mock_file.side_effect = PermissionError("Permission denied")

            writer.write_header()
            mock_print.assert_any_call("Errore durante l'apertura del file: Permission denied")


        @patch("builtins.open", new_callable=mock_open)
        @patch("csv.DictWriter")
        def test_case_4(self,  mock_dictwriter, mock_file):
            mock_writer = MagicMock()
            mock_dictwriter.return_value = mock_writer

            writer = MetricsWriter("test.csv")
            writer.write_header()

            mock_file.assert_called_once_with('test.csv', mode='w', newline='', encoding='utf-8')
            mock_dictwriter.assert_called_once_with(mock_file(), fieldnames=['Kind', 'Name', 'CountLineCode', 'CountDeclClass', 'CountDeclFunction', 'CountLineCodeDecl', 'SumEssential', 'SumCyclomaticStrict', 'MaxEssential', 'MaxCyclomaticStrict', 'MaxNesting'])
            mock_writer.writeheader.assert_called_once()

        @patch("builtins.open", new_callable=mock_open)
        @patch("csv.DictWriter")
        def test_case_5(self, mock_dictwriter, mock_file):
            mock_writer = MagicMock()
            mock_dictwriter.return_value = mock_writer

            writer = MetricsWriter("test.txt")
            writer.write_header()

            mock_file.assert_called_once_with('test.txt', mode='w', newline='', encoding='utf-8')
            mock_dictwriter.assert_called_once_with(mock_file(),
                                                    fieldnames=['Kind', 'Name', 'CountLineCode', 'CountDeclClass',
                                                                'CountDeclFunction', 'CountLineCodeDecl',
                                                                'SumEssential', 'SumCyclomaticStrict', 'MaxEssential',
                                                                'MaxCyclomaticStrict', 'MaxNesting'])
            mock_writer.writeheader.assert_called_once()


    class TestWriteMetrics:
        def test_case_1(self):
            writer = MetricsWriter(None)
            with pytest.raises(TypeError):
                writer.write_metrics("File", "path/file.java", {"CountLineCode": 10})

        @patch("builtins.print")
        def test_case_2(self, mock_print):
            writer = MetricsWriter("")
            writer.write_metrics("File", "path/file.java", {"CountLineCode": 10})
            mock_print.assert_any_call("Errore durante la scrittura nel file: [Errno 2] No such file or directory: ''")

        @patch("builtins.open", new_callable=mock_open)
        @patch("builtins.print")
        def test_case_3(self, mock_print, mock_file):
            writer = MetricsWriter("test.csv")
            mock_file.side_effect = PermissionError("Permission denied")

            writer.write_metrics("File", "path/file.java", {"CountLineCode": 10})
            mock_print.assert_any_call('Errore durante la scrittura nel file: Permission denied')

        @patch('builtins.open', new_callable=mock_open)
        @patch('csv.DictWriter')
        def test_case_4(self, mock_dictwriter, mock_file):
            metrics_writer = MetricsWriter("test.csv")
            mock_writer = MagicMock()
            mock_dictwriter.return_value = mock_writer

            metrics_writer.write_metrics(None, None, {"CountLineCode": 10})
            mock_file.assert_called_once_with('test.csv', mode='a', newline='', encoding='utf-8')
            mock_dictwriter.assert_called_once_with(mock_file(),
                                                    fieldnames=['Kind', 'Name', 'CountLineCode', 'CountDeclClass',
                                                                'CountDeclFunction', 'CountLineCodeDecl',
                                                                'SumEssential', 'SumCyclomaticStrict', 'MaxEssential',
                                                                'MaxCyclomaticStrict', 'MaxNesting'])
            mock_writer.writerow.assert_called_once()
            writerow_args = mock_writer.writerow.call_args
            expected_row = {
                "Kind": None,
                "Name": None,
                "CountLineCode": 10
            }
            assert writerow_args[0][0] == expected_row

        @patch('builtins.open', new_callable=mock_open)
        @patch('csv.DictWriter')
        def test_case_5(self, mock_dictwriter, mock_file):
            metrics_writer = MetricsWriter("test.csv")
            mock_writer = MagicMock()
            mock_dictwriter.return_value = mock_writer

            metrics_writer.write_metrics(None, [2,3,4], {"CountLineCode": 10})
            mock_file.assert_called_once_with('test.csv', mode='a', newline='', encoding='utf-8')
            mock_dictwriter.assert_called_once_with(mock_file(),
                                                    fieldnames=['Kind', 'Name', 'CountLineCode', 'CountDeclClass',
                                                                'CountDeclFunction', 'CountLineCodeDecl',
                                                                'SumEssential', 'SumCyclomaticStrict', 'MaxEssential',
                                                                'MaxCyclomaticStrict', 'MaxNesting'])
            mock_writer.writerow.assert_called_once()
            writerow_args = mock_writer.writerow.call_args
            expected_row = {
                "Kind": None,
                "Name": [2, 3, 4],
                "CountLineCode": 10
            }
            assert writerow_args[0][0] == expected_row

        @patch('builtins.open', new_callable=mock_open)
        @patch('csv.DictWriter')
        def test_case_6(self, mock_dictwriter, mock_file):
            metrics_writer = MetricsWriter("test.csv")
            mock_writer = MagicMock()
            mock_dictwriter.return_value = mock_writer

            metrics_writer.write_metrics(None, "", {"CountLineCode": 10})
            mock_file.assert_called_once_with('test.csv', mode='a', newline='', encoding='utf-8')
            mock_dictwriter.assert_called_once_with(mock_file(),
                                                    fieldnames=['Kind', 'Name', 'CountLineCode', 'CountDeclClass',
                                                                'CountDeclFunction', 'CountLineCodeDecl',
                                                                'SumEssential', 'SumCyclomaticStrict', 'MaxEssential',
                                                                'MaxCyclomaticStrict', 'MaxNesting'])
            mock_writer.writerow.assert_called_once()
            writerow_args = mock_writer.writerow.call_args
            expected_row = {
                "Kind": None,
                "Name": "",
                "CountLineCode": 10
            }
            assert writerow_args[0][0] == expected_row

        @patch('builtins.open', new_callable=mock_open)
        @patch('csv.DictWriter')
        def test_case_7(self, mock_dictwriter, mock_file):
            metrics_writer = MetricsWriter("test.csv")
            mock_writer = MagicMock()
            mock_dictwriter.return_value = mock_writer

            metrics_writer.write_metrics(None, "path/file.java", {"CountLineCode": 10})
            mock_file.assert_called_once_with('test.csv', mode='a', newline='', encoding='utf-8')
            mock_dictwriter.assert_called_once_with(mock_file(),
                                                    fieldnames=['Kind', 'Name', 'CountLineCode', 'CountDeclClass',
                                                                'CountDeclFunction', 'CountLineCodeDecl',
                                                                'SumEssential', 'SumCyclomaticStrict', 'MaxEssential',
                                                                'MaxCyclomaticStrict', 'MaxNesting'])
            mock_writer.writerow.assert_called_once()
            writerow_args = mock_writer.writerow.call_args
            expected_row = {
                "Kind": None,
                "Name": "path/file.java",
                "CountLineCode": 10
            }
            assert writerow_args[0][0] == expected_row

        @patch('builtins.open', new_callable=mock_open)
        @patch('csv.DictWriter')
        def test_case_8(self, mock_dictwriter, mock_file):
            metrics_writer = MetricsWriter("test.csv")
            mock_writer = MagicMock()
            mock_dictwriter.return_value = mock_writer

            metrics_writer.write_metrics(123, None, {"CountLineCode": 10})
            mock_file.assert_called_once_with('test.csv', mode='a', newline='', encoding='utf-8')
            mock_dictwriter.assert_called_once_with(mock_file(),
                                                    fieldnames=['Kind', 'Name', 'CountLineCode', 'CountDeclClass',
                                                                'CountDeclFunction', 'CountLineCodeDecl',
                                                                'SumEssential', 'SumCyclomaticStrict', 'MaxEssential',
                                                                'MaxCyclomaticStrict', 'MaxNesting'])
            mock_writer.writerow.assert_called_once()
            writerow_args = mock_writer.writerow.call_args
            expected_row = {
                "Kind": 123,
                "Name": None,
                "CountLineCode": 10
            }
            assert writerow_args[0][0] == expected_row

        @patch('builtins.open', new_callable=mock_open)
        @patch('csv.DictWriter')
        def test_case_9(self, mock_dictwriter, mock_file):
            metrics_writer = MetricsWriter("test.csv")
            mock_writer = MagicMock()
            mock_dictwriter.return_value = mock_writer

            metrics_writer.write_metrics(123, [2, 3, 4], {"CountLineCode": 10})
            mock_file.assert_called_once_with('test.csv', mode='a', newline='', encoding='utf-8')
            mock_dictwriter.assert_called_once_with(mock_file(),
                                                    fieldnames=['Kind', 'Name', 'CountLineCode', 'CountDeclClass',
                                                                'CountDeclFunction', 'CountLineCodeDecl',
                                                                'SumEssential', 'SumCyclomaticStrict', 'MaxEssential',
                                                                'MaxCyclomaticStrict', 'MaxNesting'])
            mock_writer.writerow.assert_called_once()
            writerow_args = mock_writer.writerow.call_args
            expected_row = {
                "Kind": 123,
                "Name": [2, 3, 4],
                "CountLineCode": 10
            }
            assert writerow_args[0][0] == expected_row

        @patch('builtins.open', new_callable=mock_open)
        @patch('csv.DictWriter')
        def test_case_10(self, mock_dictwriter, mock_file):
            metrics_writer = MetricsWriter("test.csv")
            mock_writer = MagicMock()
            mock_dictwriter.return_value = mock_writer

            metrics_writer.write_metrics(123, "", {"CountLineCode": 10})
            mock_file.assert_called_once_with('test.csv', mode='a', newline='', encoding='utf-8')
            mock_dictwriter.assert_called_once_with(mock_file(),
                                                    fieldnames=['Kind', 'Name', 'CountLineCode', 'CountDeclClass',
                                                                'CountDeclFunction', 'CountLineCodeDecl',
                                                                'SumEssential', 'SumCyclomaticStrict', 'MaxEssential',
                                                                'MaxCyclomaticStrict', 'MaxNesting'])
            mock_writer.writerow.assert_called_once()
            writerow_args = mock_writer.writerow.call_args
            expected_row = {
                "Kind": 123,
                "Name": "",
                "CountLineCode": 10
            }
            assert writerow_args[0][0] == expected_row

        @patch('builtins.open', new_callable=mock_open)
        @patch('csv.DictWriter')
        def test_case_11(self, mock_dictwriter, mock_file):
            metrics_writer = MetricsWriter("test.csv")
            mock_writer = MagicMock()
            mock_dictwriter.return_value = mock_writer

            metrics_writer.write_metrics(123, "path/file.java", {"CountLineCode": 10})
            mock_file.assert_called_once_with('test.csv', mode='a', newline='', encoding='utf-8')
            mock_dictwriter.assert_called_once_with(mock_file(),
                                                    fieldnames=['Kind', 'Name', 'CountLineCode', 'CountDeclClass',
                                                                'CountDeclFunction', 'CountLineCodeDecl',
                                                                'SumEssential', 'SumCyclomaticStrict', 'MaxEssential',
                                                                'MaxCyclomaticStrict', 'MaxNesting'])
            mock_writer.writerow.assert_called_once()
            writerow_args = mock_writer.writerow.call_args
            expected_row = {
                "Kind": 123,
                "Name": "path/file.java",
                "CountLineCode": 10
            }
            assert writerow_args[0][0] == expected_row

        @patch('builtins.open', new_callable=mock_open)
        @patch('csv.DictWriter')
        def test_case_12(self, mock_dictwriter, mock_file):
            metrics_writer = MetricsWriter("test.csv")
            mock_writer = MagicMock()
            mock_dictwriter.return_value = mock_writer

            # This case should succeed without raising an error
            metrics_writer.write_metrics("File", None, {"CountLineCode": 10})
            mock_file.assert_called_once_with('test.csv', mode='a', newline='', encoding='utf-8')
            mock_dictwriter.assert_called_once_with(mock_file(),
                                                    fieldnames=['Kind', 'Name', 'CountLineCode', 'CountDeclClass',
                                                                'CountDeclFunction', 'CountLineCodeDecl',
                                                                'SumEssential', 'SumCyclomaticStrict', 'MaxEssential',
                                                                'MaxCyclomaticStrict', 'MaxNesting'])
            mock_writer.writerow.assert_called_once()
            writerow_args = mock_writer.writerow.call_args
            expected_row = {
                "Kind": "File",
                "Name": None,
                "CountLineCode": 10
            }
            assert writerow_args[0][0] == expected_row

        @patch('builtins.open', new_callable=mock_open)
        @patch('csv.DictWriter')
        def test_case_13(self, mock_dictwriter, mock_file):
            metrics_writer = MetricsWriter("test.csv")
            mock_writer = MagicMock()
            mock_dictwriter.return_value = mock_writer

            # This case should succeed without raising an error
            metrics_writer.write_metrics("File", [1,2,3], {"CountLineCode": 10})
            mock_file.assert_called_once_with('test.csv', mode='a', newline='', encoding='utf-8')
            mock_dictwriter.assert_called_once_with(mock_file(),
                                                    fieldnames=['Kind', 'Name', 'CountLineCode', 'CountDeclClass',
                                                                'CountDeclFunction', 'CountLineCodeDecl',
                                                                'SumEssential', 'SumCyclomaticStrict', 'MaxEssential',
                                                                'MaxCyclomaticStrict', 'MaxNesting'])
            mock_writer.writerow.assert_called_once()
            writerow_args = mock_writer.writerow.call_args
            expected_row = {
                "Kind": "File",
                "Name": [1, 2, 3],
                "CountLineCode": 10
            }
            assert writerow_args[0][0] == expected_row

        @patch('builtins.open', new_callable=mock_open)
        @patch('csv.DictWriter')
        def test_case_14(self, mock_dictwriter, mock_file):
            metrics_writer = MetricsWriter("test.csv")
            mock_writer = MagicMock()
            mock_dictwriter.return_value = mock_writer

            metrics_writer.write_metrics("File", "", {"CountLineCode": 10})
            mock_file.assert_called_once_with('test.csv', mode='a', newline='', encoding='utf-8')
            mock_dictwriter.assert_called_once_with(mock_file(),
                                                    fieldnames=['Kind', 'Name', 'CountLineCode', 'CountDeclClass',
                                                                'CountDeclFunction', 'CountLineCodeDecl',
                                                                'SumEssential', 'SumCyclomaticStrict', 'MaxEssential',
                                                                'MaxCyclomaticStrict', 'MaxNesting'])
            mock_writer.writerow.assert_called_once()
            writerow_args = mock_writer.writerow.call_args
            expected_row = {
                "Kind": "File",
                "Name": "",
                "CountLineCode": 10
            }
            assert writerow_args[0][0] == expected_row

        @patch('builtins.open', new_callable=mock_open)
        @patch('csv.DictWriter')
        def test_case_15(self, mock_dictwriter, mock_file):
            metrics_writer = MetricsWriter("test.csv")
            mock_writer = MagicMock()
            mock_dictwriter.return_value = mock_writer

            metrics_writer.write_metrics("File", "path/file.java", {"CountLineCode": 10})
            mock_file.assert_called_once_with('test.csv', mode='a', newline='', encoding='utf-8')
            mock_dictwriter.assert_called_once_with(mock_file(),
                                                    fieldnames=['Kind', 'Name', 'CountLineCode', 'CountDeclClass',
                                                                'CountDeclFunction', 'CountLineCodeDecl',
                                                                'SumEssential', 'SumCyclomaticStrict', 'MaxEssential',
                                                                'MaxCyclomaticStrict', 'MaxNesting'])
            mock_writer.writerow.assert_called_once()
            writerow_args = mock_writer.writerow.call_args
            expected_row = {
                "Kind": "File",
                "Name": "path/file.java",
                "CountLineCode": 10
            }
            assert writerow_args[0][0] == expected_row

        @patch('builtins.open', new_callable=mock_open)
        @patch('csv.DictWriter')
        def test_case_16(self, mock_dictwriter, mock_file):
            metrics_writer = MetricsWriter("test_file.csv")
            mock_writer = MagicMock()
            mock_dictwriter.return_value = mock_writer

            with pytest.raises(TypeError):
                metrics_writer.write_metrics("File", "SomeName", None)

        @patch('builtins.open', new_callable=mock_open)
        @patch('csv.DictWriter')
        def test_case_17(self, mock_dictwriter, mock_file):
            metrics_writer = MetricsWriter("test_file.csv")
            mock_writer = MagicMock()
            mock_dictwriter.return_value = mock_writer

            with pytest.raises(TypeError):
                metrics_writer.write_metrics("File", "SomeName", "InvalidMetrics")
