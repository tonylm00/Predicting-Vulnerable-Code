import unittest
from unittest.mock import patch, mock_open
import pytest
from Dataset2.Text_Mining.CSVWriter import CSVWriter

class TestCSVWriter:
    @patch("builtins.open", new_callable=mock_open)
    def test_case_1(self, mock_file):
        # Dati di esempio
        filtered_dict = [1, 2, 3]
        mining_dict = {
            "commit1": {"classname": 3, "methodname": 2, "variablename": 1},
            "commit2": {"classname": 0, "methodname": 1, "variablename": 0}
        }
        output_csv_name = "output.csv"

        # Crea un'istanza di CSVWriter

        with pytest.raises(AttributeError):
            CSVWriter(filtered_dict, mining_dict, output_csv_name)

    class TestWriteHeader:
        @patch("builtins.open", new_callable=mock_open)
        def test_case_1(self, mock_file):
            filtered_dict = {
                "className": 3,
                "methodName": 3,
                "variableName": 1
            }
            mining_dict = {
                "commit1": {"classname": 3, "methodname": 2, "variablename": 1},
                "commit2": {"classname": 0, "methodname": 1, "variablename": 0}
            }
            output_csv_name = "output.csv"

            # Crea un'istanza di CSVWriter
            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            # Esegui la funzione write_rows
            csv_writer.write_header()

            # Recupera il file gestito dal mock
            handle = mock_file()

            # Verifica che write sia stato chiamato con i valori corretti
            expected_calls = [
                # Prima riga per commit1
                unittest.mock.call.write("Name"),
                unittest.mock.call.write(", className"),
                unittest.mock.call.write(", methodName"),
                unittest.mock.call.write(", variableName"),
                unittest.mock.call.write("\n")
            ]

            # Verifica che write sia stato chiamato con la sequenza corretta
            handle.write.assert_has_calls(expected_calls, any_order=False)

        @patch("builtins.open", new_callable=mock_open)
        def test_case_2(self, mock_file):
            filtered_dict = {
                "className": 3,
                "methodName": 3,
                "variableName": 1
            }
            mining_dict = {}
            output_csv_name = "output.csv"

            # Crea un'istanza di CSVWriter
            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            # Esegui la funzione write_rows
            csv_writer.write_header()

            # Recupera il file gestito dal mock
            handle = mock_file()

            # Verifica che write sia stato chiamato con i valori corretti
            expected_calls = [
                # Prima riga per commit1
                unittest.mock.call.write("Name"),
                unittest.mock.call.write(", className"),
                unittest.mock.call.write(", methodName"),
                unittest.mock.call.write(", variableName"),
                unittest.mock.call.write("\n")
            ]

            # Verifica che write sia stato chiamato con la sequenza corretta
            handle.write.assert_has_calls(expected_calls, any_order=False)

        @patch("builtins.open", new_callable=mock_open)
        def test_case_3(self, mock_file):
            filtered_dict = {
                "className": 3,
                "methodName": 3,
                "variableName": 1
            }
            mining_dict = "prova con una variabile non dizionario"
            output_csv_name = "output.csv"

            # Crea un'istanza di CSVWriter
            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            # Esegui la funzione write_rows
            csv_writer.write_header()

            # Recupera il file gestito dal mock
            handle = mock_file()

            # Verifica che write sia stato chiamato con i valori corretti
            expected_calls = [
                # Prima riga per commit1
                unittest.mock.call.write("Name"),
                unittest.mock.call.write(", className"),
                unittest.mock.call.write(", methodName"),
                unittest.mock.call.write(", variableName"),
                unittest.mock.call.write("\n")
            ]

            # Verifica che write sia stato chiamato con la sequenza corretta
            handle.write.assert_has_calls(expected_calls, any_order=False)

        @patch("builtins.open", new_callable=mock_open)
        def test_case_4(self, mock_file):
            filtered_dict = {}
            mining_dict = {
                "commit1": {"classname": 3, "methodname": 2, "variablename": 1},
                "commit2": {"classname": 0, "methodname": 1, "variablename": 0}
            }
            output_csv_name = "output.csv"

            # Crea un'istanza di CSVWriter
            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            # Esegui la funzione write_rows
            csv_writer.write_header()

            # Recupera il file gestito dal mock
            handle = mock_file()

            # Verifica che write sia stato chiamato con i valori corretti
            expected_calls = [
                # Prima riga per commit1
                unittest.mock.call.write("Name"),
                unittest.mock.call.write("\n")
            ]

            # Verifica che write sia stato chiamato con la sequenza corretta
            handle.write.assert_has_calls(expected_calls, any_order=False)

        @patch("builtins.open", new_callable=mock_open)
        def test_case_5(self, mock_file):
            filtered_dict = {}
            mining_dict = {}
            output_csv_name = "output.csv"

            # Crea un'istanza di CSVWriter
            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            # Esegui la funzione write_rows
            csv_writer.write_header()

            # Recupera il file gestito dal mock
            handle = mock_file()

            # Verifica che write sia stato chiamato con i valori corretti
            expected_calls = [
                # Prima riga per commit1
                unittest.mock.call.write("Name"),
                unittest.mock.call.write("\n")
            ]

            # Verifica che write sia stato chiamato con la sequenza corretta
            handle.write.assert_has_calls(expected_calls, any_order=False)

        @patch("builtins.open", new_callable=mock_open)
        def test_case_6(self, mock_file):
            filtered_dict = {}
            mining_dict = "prova con una variabile non dizionario"
            output_csv_name = "output.csv"

            # Crea un'istanza di CSVWriter
            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            # Esegui la funzione write_rows
            csv_writer.write_header()

            # Recupera il file gestito dal mock
            handle = mock_file()

            # Verifica che write sia stato chiamato con i valori corretti
            expected_calls = [
                # Prima riga per commit1
                unittest.mock.call.write("Name"),
                unittest.mock.call.write("\n")
            ]

            # Verifica che write sia stato chiamato con la sequenza corretta
            handle.write.assert_has_calls(expected_calls, any_order=False)

        @patch("builtins.open", new_callable=mock_open)
        def test_case_7(self, mock_file):
            mock_file.side_effect = PermissionError("Accesso negato")

            filtered_dict = {"className": 3, "methodName": 3, "variableName": 1}
            mining_dict = {"commit1": {"classname": 3, "methodname": 2, "variablename": 1}}
            output_csv_name = "output.csv"

            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            # Verifichiamo che venga lanciato PermissionError durante l'apertura del file
            with pytest.raises(PermissionError):
                csv_writer.write_header()

        @patch("builtins.open", new_callable=mock_open)
        def test_case_8(self, mock_file):
            handle = mock_file()
            handle.write.side_effect = IOError("Errore di scrittura")

            filtered_dict = {"className": 3, "methodName": 3, "variableName": 1}
            mining_dict = {"commit1": {"classname": 3, "methodname": 2, "variablename": 1}}
            output_csv_name = "output.csv"

            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            # Verifichiamo che venga lanciato IOError durante la scrittura
            with pytest.raises(IOError):
                csv_writer.write_header()

    class TestWriteRows:
        #perchè le chiavi di mining_dict vengono portate a lowercase, non ci sarà quindi corrispondenza con le chiavi di filtered_dict
        @patch("builtins.open", new_callable=mock_open)
        def test_case_1(self, mock_file):
            # Dati di esempio
            filtered_dict = {
                "className": 3,
                "methodName": 3,
                "variableName": 1
            }
            mining_dict = {
                "commit1": {"className": 3, "methodName": 2, "variableName": 1},
                "commit2": {"className": 0, "methodName": 1, "variableName": 0}
            }
            output_csv_name = "output.csv"

            # Crea un'istanza di CSVWriter
            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            # Esegui la funzione write_rows
            csv_writer.write_rows()

            # Recupera il file gestito dal mock
            handle = mock_file()

            # Verifica che write sia stato chiamato con i valori corretti
            expected_calls = [
                # Prima riga per commit1
                unittest.mock.call.write("commit1"),
                unittest.mock.call.write(",0"),
                unittest.mock.call.write(",0"),
                unittest.mock.call.write(",0"),
                unittest.mock.call.write("\n"),
                # Seconda riga per commit2
                unittest.mock.call.write("commit2"),
                unittest.mock.call.write(",0"),
                unittest.mock.call.write(",0"),
                unittest.mock.call.write(",0"),
                unittest.mock.call.write("\n"),
            ]

            # Verifica che write sia stato chiamato con la sequenza corretta
            handle.write.assert_has_calls(expected_calls, any_order=False)

        @patch("builtins.open", new_callable=mock_open)
        def test_case_2(self, mock_file):
            # Dati di esempio
            filtered_dict = {'package': 723, 'java': 16, 'apache': 32, 'sdk': 24, 'web': 1650, 'util': 986, 'import': 584, 'com': 180, 'static': 70}
            mining_dict = {
                "commit1": {'package': 1, 'com': 18, 'apache': 5, 'sdk': 2, 'import': 23, 'java': 6, 'util': 13},
                "commit2": {'package': 1, 'com': 18, 'apache': 5, 'sdk': 2, 'import': 23, 'java': 6, 'util': 13}
            }
            output_csv_name = "output.csv"

            # Crea un'istanza di CSVWriter
            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            # Esegui la funzione write_rows
            csv_writer.write_rows()

            # Recupera il file gestito dal mock
            handle = mock_file()

            # Verifica che write sia stato chiamato con i valori corretti
            expected_calls = [
                # Prima riga per commit1
                unittest.mock.call.write("commit1"),
                unittest.mock.call.write(",5"),
                unittest.mock.call.write(",18"),
                unittest.mock.call.write(",23"),
                unittest.mock.call.write(",6"),
                unittest.mock.call.write(",1"),
                unittest.mock.call.write(",2"),
                unittest.mock.call.write(",0"),
                unittest.mock.call.write(",13"),
                unittest.mock.call.write(",0"),
                unittest.mock.call.write("\n"),
                # Seconda riga per commit2
                unittest.mock.call.write("commit2"),
                unittest.mock.call.write(",5"),
                unittest.mock.call.write(",18"),
                unittest.mock.call.write(",23"),
                unittest.mock.call.write(",6"),
                unittest.mock.call.write(",1"),
                unittest.mock.call.write(",2"),
                unittest.mock.call.write(",0"),
                unittest.mock.call.write(",13"),
                unittest.mock.call.write(",0"),
                unittest.mock.call.write("\n"),
            ]

            # Verifica che write sia stato chiamato con la sequenza corretta
            handle.write.assert_has_calls(expected_calls, any_order=False)

        @patch("builtins.open", new_callable=mock_open)
        def test_case_3(self, mock_file):
            # Dati di esempio
            filtered_dict = {'package': 723, 'java': 16, 'apache': 32, 'sdk': 24, 'web': 1650, 'util': 986,
                             'import': 584,
                             'com': 180, 'static': 70}

            mining_dict = {
                "commit1": "non è corretto",
                "commit2": {'package': 1, 'com': 18, 'apache': 5, 'sdk': 2, 'import': 23, 'java': 6, 'util': 13}
            }
            output_csv_name = "output.csv"

            # Crea un'istanza di CSVWriter
            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            with pytest.raises(TypeError):
                # Esegui la funzione write_rows
                csv_writer.write_rows()

        @patch("builtins.open", new_callable=mock_open)
        def test_case_4(self, mock_file):
            # Dati di esempio
            filtered_dict = {'package': 723, 'java': 16, 'apache': 32, 'sdk': 24, 'web': 1650, 'util': 986,
                             'import': 584,
                             'com': 180, 'static': 70}

            mining_dict = {
                "commit1": {},
                "commit2": {'package': 1, 'com': 18, 'apache': 5, 'sdk': 2, 'import': 23, 'java': 6, 'util': 13}
            }
            output_csv_name = "output.csv"

            # Crea un'istanza di CSVWriter
            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            # Esegui la funzione write_rows
            csv_writer.write_rows()

            # Recupera il file gestito dal mock
            handle = mock_file()

            # Verifica che write sia stato chiamato con i valori corretti
            expected_calls = [
                # Prima riga per commit1
                unittest.mock.call.write("commit1"),
                unittest.mock.call.write(",0"),
                unittest.mock.call.write(",0"),
                unittest.mock.call.write(",0"),
                unittest.mock.call.write(",0"),
                unittest.mock.call.write(",0"),
                unittest.mock.call.write(",0"),
                unittest.mock.call.write(",0"),
                unittest.mock.call.write(",0"),
                unittest.mock.call.write(",0"),
                unittest.mock.call.write("\n"),
                # Seconda riga per commit2
                unittest.mock.call.write("commit2"),
                unittest.mock.call.write(",5"),
                unittest.mock.call.write(",18"),
                unittest.mock.call.write(",23"),
                unittest.mock.call.write(",6"),
                unittest.mock.call.write(",1"),
                unittest.mock.call.write(",2"),
                unittest.mock.call.write(",0"),
                unittest.mock.call.write(",13"),
                unittest.mock.call.write(",0"),
                unittest.mock.call.write("\n"),
            ]

            # Verifica che write sia stato chiamato con la sequenza corretta
            handle.write.assert_has_calls(expected_calls, any_order=False)

        @patch("builtins.open", new_callable=mock_open)
        def test_case_5(self, mock_file):
            # Dati di esempio
            filtered_dict = {'package': 723, 'java': 16, 'apache': 32, 'sdk': 24, 'web': 1650, 'util': 986,
                             'import': 584, 'com': 180, 'static': 70}
            mining_dict = {"classname": 3, "methodname": 2, "variablename": 1}
            output_csv_name = "output.csv"

            # Crea un'istanza di CSVWriter
            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            with pytest.raises(TypeError):
                # Esegui la funzione write_rows
                csv_writer.write_rows()

        @patch("builtins.open", new_callable=mock_open)
        def test_case_6(self, mock_file):
            # Dati di esempio
            filtered_dict = {
                "classname": 3,
                "methodname": 3,
                "variablename": 1
            }
            mining_dict = {}
            output_csv_name = "output.csv"

            # Crea un'istanza di CSVWriter
            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            # Esegui la funzione write_rows
            csv_writer.write_rows()

            # Recupera il file gestito dal mock
            handle = mock_file()

            # Verifica che write sia stato chiamato con i valori corretti
            expected_calls = []

            # Verifica che write sia stato chiamato con la sequenza corretta
            handle.write.assert_has_calls(expected_calls, any_order=False)

        @patch("builtins.open", new_callable=mock_open)
        def test_case_7(self, mock_file):
            # Dati di esempio
            filtered_dict = {
                "classname": 3,
                "methodname": 3,
                "variablename": 1
            }
            mining_dict = [1, 2, 3]
            output_csv_name = "output.csv"

            # Crea un'istanza di CSVWriter
            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            with pytest.raises(AttributeError):
                # Esegui la funzione write_rows
                csv_writer.write_rows()

        @patch("builtins.open", new_callable=mock_open)
        def test_case_8(self, mock_file):
            # Dati di esempio
            filtered_dict = {}
            mining_dict = {
                "commit1": {"classname": 3, "methodname": 2, "variablename": 1},
                "commit2": {"classname": 0, "methodname": 1, "variablename": 0}
            }
            output_csv_name = "output.csv"

            # Crea un'istanza di CSVWriter
            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            # Esegui la funzione write_rows
            csv_writer.write_rows()

            # Recupera il file gestito dal mock
            handle = mock_file()

            # Verifica che write sia stato chiamato con i valori corretti
            expected_calls = []

            # Verifica che write sia stato chiamato con la sequenza corretta
            handle.write.assert_has_calls(expected_calls, any_order=False)

        @patch("builtins.open", new_callable=mock_open)
        def test_case_9(self, mock_file):
            # Dati di esempio
            filtered_dict = {}

            mining_dict = {
                "commit1": "non è corretto",
                "commit2": {'package': 1, 'com': 18, 'apache': 5, 'sdk': 2, 'import': 23, 'java': 6, 'util': 13}
            }
            output_csv_name = "output.csv"

            # Crea un'istanza di CSVWriter
            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            with pytest.raises(TypeError):
                # Esegui la funzione write_rows
                csv_writer.write_rows()

        @patch("builtins.open", new_callable=mock_open)
        def test_case_10(self, mock_file):
            # Dati di esempio
            filtered_dict = {}

            mining_dict = {
                "commit1": {},
                "commit2": {'package': 1, 'com': 18, 'apache': 5, 'sdk': 2, 'import': 23, 'java': 6, 'util': 13}
            }
            output_csv_name = "output.csv"

            # Crea un'istanza di CSVWriter
            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            # Esegui la funzione write_rows
            csv_writer.write_rows()

            # Recupera il file gestito dal mock
            handle = mock_file()

            # Verifica che write sia stato chiamato con i valori corretti
            expected_calls = [
                # Prima riga per commit1
                unittest.mock.call.write("commit1"),
                unittest.mock.call.write("\n"),
                # Seconda riga per commit2
                unittest.mock.call.write("commit2"),
                unittest.mock.call.write("\n"),
            ]

            # Verifica che write sia stato chiamato con la sequenza corretta
            handle.write.assert_has_calls(expected_calls, any_order=False)

        @patch("builtins.open", new_callable=mock_open)
        def test_case_11(self, mock_file):
            # Dati di esempio
            filtered_dict = {}
            mining_dict = {"classname": 0, "methodname": 1, "variablename": 0}

            output_csv_name = "output.csv"

            # Crea un'istanza di CSVWriter
            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            with pytest.raises(TypeError):
                # Esegui la funzione write_rows
                csv_writer.write_rows()

        @patch("builtins.open", new_callable=mock_open)
        def test_case_12(self, mock_file):
            # Dati di esempio
            filtered_dict = {}
            mining_dict = {}
            output_csv_name = "output.csv"

            # Crea un'istanza di CSVWriter
            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            # Esegui la funzione write_rows
            csv_writer.write_rows()

            # Recupera il file gestito dal mock
            handle = mock_file()

            # Verifica che write sia stato chiamato con i valori corretti
            expected_calls = []

            # Verifica che write sia stato chiamato con la sequenza corretta
            handle.write.assert_has_calls(expected_calls, any_order=False)

        @patch("builtins.open", new_callable=mock_open)
        def test_case_13(self, mock_file):
            # Dati di esempio
            filtered_dict = {}
            mining_dict = "test non dizionario"
            output_csv_name = "output.csv"

            # Crea un'istanza di CSVWriter
            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            with pytest.raises(AttributeError):
                # Esegui la funzione write_rows
                csv_writer.write_rows()

        @patch("builtins.open", new_callable=mock_open)
        def test_case_14(self, mock_file):
            mock_file.side_effect = PermissionError("Accesso negato")

            filtered_dict = {"className": 3, "methodName": 3, "variableName": 1}
            mining_dict = {"commit1": {"classname": 3, "methodname": 2, "variablename": 1}}
            output_csv_name = "output.csv"

            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            # Verifichiamo che venga lanciato PermissionError durante l'apertura del file
            with pytest.raises(PermissionError):
                csv_writer.write_rows()

        @patch("builtins.open", new_callable=mock_open)
        def test_case_15(self, mock_file):
            handle = mock_file()
            handle.write.side_effect = IOError("Errore di scrittura")

            filtered_dict = {"className": 3, "methodName": 3, "variableName": 1}
            mining_dict = {"commit1": {"classname": 3, "methodname": 2, "variablename": 1}}
            output_csv_name = "output.csv"

            csv_writer = CSVWriter(filtered_dict, mining_dict, output_csv_name)

            # Verifichiamo che venga lanciato IOError durante la scrittura
            with pytest.raises(IOError):
                csv_writer.write_rows()
