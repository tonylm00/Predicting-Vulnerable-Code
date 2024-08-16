from unittest import mock
from Dataset2.Union.Union_TM_SM.Union import initialize, getClass, another_option
import unittest
import io


class TestGetClass(unittest.TestCase):

    def test_TC_1(self):
        with self.assertRaises(ValueError):
            getClass("")

    def test_TC_2(self):
        self.assertEqual(getClass("a,b,c,pos"), "pos")
        self.assertEqual(getClass("x,neg"), "neg")
        self.assertEqual(getClass("1,2,3,4,5,pos"), "pos")
        self.assertEqual(getClass("1,2,3"), "3")

    def test_TC_3(self):
        with self.assertRaises(ValueError):
            getClass("a,b,c")


class TestAnotherOption(unittest.TestCase):

    def test_TC_1(self):
        with self.assertRaises(ValueError):
            self.assertEqual(another_option(line_sm=None, line_tm=None, class_element=None), None)

    def test_TC_2(self):
        with self.assertRaises(ValueError):
            self.assertEqual(another_option(line_sm="", line_tm="", class_element=""), None)

    def test_TC_3(self):
        with self.assertRaises(ValueError):
            self.assertEqual(another_option(line_sm=None, line_tm="", class_element=None), None)

    def test_TC_4(self):
        with self.assertRaises(ValueError):
            self.assertEqual(another_option(line_sm=None, line_tm="a,b,c,pos", class_element=None), None)

    def test_TC_5(self):
        with self.assertRaises(ValueError):
            self.assertEqual(another_option(line_sm=None, line_tm="a,b,c,pos", class_element="x"), None)

    def test_TC_6(self):
        with self.assertRaises(ValueError):
            self.assertEqual(another_option(line_sm=None, line_tm="a,b,c,pos", class_element="neg"), None)

    def test_TC_7(self):
        self.assertEqual(another_option(line_sm=None, line_tm="a,b,c,pos", class_element="pos"), "a,b,c,")

    def test_TC_8(self):
        with self.assertRaises(ValueError):
            self.assertEqual(another_option(line_sm="", line_tm=None, class_element=None), None)

    def test_TC_9(self):
        self.assertEqual(another_option(line_sm="a,b,c,d,e", line_tm=None, class_element=None), "c,d,e,")


class TestInitialize(unittest.TestCase):

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_TC_1(self, mock_file):

        with self.assertRaises(FileNotFoundError):
            initialize("", "mining_results_sm_final.csv", mock_file())

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_TC_2(self, mock_file):

        with self.assertRaises(FileNotFoundError):
            initialize("not_csv_mining_final.csv", "mining_results_sm_final.csv", mock_file())

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_TC_3(self, mock_file):

        with self.assertRaises(FileNotFoundError):
            initialize("csv_mining_final.csv", "", mock_file())

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_TC_4(self, mock_file):

        with self.assertRaises(FileNotFoundError):
            initialize("csv_mining_final.csv", "not_mining_results_sm_final.csv", mock_file())

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_TC_5(self, mock_file):

        mock_file.side_effect = FileNotFoundError

        with self.assertRaises(FileNotFoundError):
            initialize("csv_mining_final.csv", "mining_results_sm_final.csv", mock_file())

    @mock.patch("os.getcwd", return_value="/home")
    @mock.patch("os.chdir")
    def test_TC_6(self, mock_chdir, mock_getcwd):

        # Parametri del test case
        name_csv_mining = "csv_mining_final.csv"
        name_csv_soft_m = "mining_results_sm_final.csv"

        # Definiamo una funzione side_effect che lancia FileNotFoundError solo per csv_mining_final.csv
        def open_side_effect(file_name, mode, encoding=None):
            if file_name == name_csv_mining:
                raise FileNotFoundError
            else:
                # Usa un mock standard per altri file
                return mock.mock_open().return_value

        # Patchiamo solo la chiamata open che gestisce csv_mining
        with mock.patch("builtins.open", side_effect=open_side_effect) as mock_open:
            with self.assertRaises(FileNotFoundError):
                # Chiamata alla funzione da testare
                initialize(name_csv_mining, name_csv_soft_m, mock_open)

        # Verifica che la funzione abbia provato ad aprire il file csv_mining
        mock_open.assert_called_with(name_csv_mining, "r+", encoding="utf-8")

    @mock.patch("os.getcwd", return_value="/home")
    @mock.patch("os.chdir")
    def test_TC_7(self, mock_chdir, mock_getcwd):

        # Parametri del test case
        name_csv_mining = "csv_mining_final.csv"
        name_csv_soft_m = "mining_results_sm_final.csv"

        # Definiamo una funzione side_effect che lancia FileNotFoundError solo per csv_mining_final.csv
        def open_side_effect(file_name, mode, encoding=None):
            if file_name == name_csv_soft_m:
                raise FileNotFoundError
            else:
                # Usa un mock standard per altri file
                return mock.mock_open().return_value

        # Patchiamo solo la chiamata open che gestisce csv_mining
        with mock.patch("builtins.open", side_effect=open_side_effect) as mock_open:
            with self.assertRaises(FileNotFoundError):
                # Chiamata alla funzione da testare
                initialize(name_csv_mining, name_csv_soft_m, mock_open)

        # Verifica che la funzione abbia provato ad aprire il file csv_mining
        mock_open.assert_called_with(name_csv_soft_m, "r+", encoding="utf-8")

    @mock.patch("os.getcwd", return_value="/home/")
    @mock.patch("os.chdir")
    def test_TC_8(self, mock_chdir, mock_getcwd):
        name_csv_mining = "csv_mining_final.csv"
        name_csv_soft_m = "mining_results_sm_final.csv"

        # csv_mining_final vuoto
        mock_csv_mining = mock.mock_open(read_data="")

        # Simuliamo che il file csv_software_metric contenga dati
        mock_csv_software_metric = mock.mock_open(read_data="kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n")

        # Creiamo un mock per new_Union
        mock_new_union = mock.mock_open()

        # Patchiamo la funzione open per restituire i file mockati
        with mock.patch("builtins.open",
                        side_effect=[
                            mock_csv_mining.return_value,
                            mock_csv_software_metric.return_value,
                            mock_new_union.return_value
                        ]):
            with self.assertRaises(ValueError):
                initialize(name_csv_mining, name_csv_soft_m, mock_new_union)

        # Verifica che csv_mining sia stato aperto e letto come vuoto
        mock_csv_mining.assert_called_with(name_csv_mining, "r+", encoding="utf-8")

    @mock.patch("os.getcwd", return_value="/home/")
    @mock.patch("os.chdir")
    def test_TC_9(self, mock_chdir, mock_getcwd):
        name_csv_mining = "csv_mining_final.csv"
        name_csv_soft_m = "mining_results_sm_final.csv"

        # Simuliamo che il file csv_mining_final.csv contenga solo l'intestazione
        mock_csv_mining = mock.mock_open(read_data="NameClass,a1,a2,a3,a4,a5,a6,a7,a8,a9,class\n")

        # Simuliamo che il file csv_software_metric contenga dati validi
        mock_csv_software_metric = mock.mock_open(read_data="kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n"
                                                            "txt,nicola,1,2,3,4,5,6,7,8,9,10,11,pos\n")

        # Creiamo un mock per new_Union
        mock_new_union = mock.mock_open()

        # Patchiamo la funzione open per restituire i file mockati
        with mock.patch("builtins.open", side_effect=[
            mock_csv_mining.return_value,
            mock_csv_software_metric.return_value,
            mock_new_union.return_value
        ]):
            with self.assertRaises(ValueError, msg="Errore, il file csv_mining contiene solo le intestazioni"):
                initialize(name_csv_mining, name_csv_soft_m, mock_new_union())

        # Verifica che csv_mining sia stato aperto e letto con solo l'intestazione
        mock_csv_mining.assert_called_with(name_csv_mining, "r+", encoding="utf-8")

    @mock.patch("os.getcwd", return_value="/home/")
    @mock.patch("os.chdir")
    def test_TC_10(self, mock_chdir, mock_getcwd):
        name_csv_mining = "csv_mining_final.csv"
        name_csv_soft_m = "mining_results_sm_final.csv"

        # Simuliamo che il file csv_mining contenga dati validi
        mock_csv_mining = mock.mock_open(read_data="NameClass,a1,a2,a3,a4,a5,a6,a7,a8,a9,class\n"
                                                   "tony.java,1,2,3,4,5,6,7,8,9,pos\n")

        # Simuliamo che il file csv_software_metric sia vuoto
        mock_csv_software_metric = mock.mock_open(read_data="")

        # Creiamo un mock per new_Union
        mock_new_union = mock.mock_open()

        # Patchiamo la funzione open per restituire i file mockati
        with mock.patch("builtins.open", side_effect=[
            mock_csv_mining.return_value,
            mock_csv_software_metric.return_value,
            mock_new_union.return_value
        ]):
            with self.assertRaises(ValueError, msg="Errore, il file csv_software_metric è vuoto"):
                initialize(name_csv_mining, name_csv_soft_m, mock_new_union())

        # Verifica che csv_software_metric sia stato aperto e letto come vuoto
        mock_csv_software_metric.assert_called_with(name_csv_soft_m, "r+", encoding="utf-8")

    @mock.patch("os.getcwd", return_value="/home/")
    @mock.patch("os.chdir")
    def test_TC_11(self, mock_chdir, mock_getcwd):
        name_csv_mining = "csv_mining_final.csv"
        name_csv_soft_m = "mining_results_sm_final.csv"

        # Simuliamo che il file csv_mining contenga dati completi
        mock_csv_mining = mock.mock_open(read_data="NameClass,a1,a2,a3,a4,a5,a6,a7,a8,a9,class\n"
                                                   "tony.java,1,2,3,4,5,6,7,8,9,pos\n")

        # Simuliamo che il file csv_software_metric contenga solo l'intestazione
        mock_csv_software_metric = mock.mock_open(read_data="kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n")

        # Creiamo un mock per new_Union e abilitiamo il metodo write
        mock_new_union = mock.mock_open()

        # Patchiamo la funzione open per restituire i file mockati
        with mock.patch("builtins.open", side_effect=[
            mock_csv_mining.return_value,
            mock_csv_software_metric.return_value,
            mock_new_union.return_value
        ]):
            with self.assertRaises(ValueError, msg="Errore, il file csv_software_metric contiene solo l’intestazione"):
                initialize(name_csv_mining, name_csv_soft_m, mock_new_union())

        # Verifica che csv_software_metric sia stato aperto e letto con solo l'intestazione
        mock_csv_software_metric.assert_called_with(name_csv_soft_m, "r+", encoding="utf-8")

    @mock.patch("os.getcwd", return_value="/home/")
    @mock.patch("os.chdir")  # Mockiamo anche il cambio di directory
    def test_TC_12(self, mock_chdir, mock_getcwd):
        name_csv_mining = "csv_mining_final.csv"
        name_csv_soft_m = "mining_results_sm_final.csv"

        # Simuliamo che csv_mining contenga dati
        mock_csv_mining = mock.mock_open(read_data="NameClass,a1,a2,a3,a4,a5,a6,a7,a8,a9,class\n"
                                                   "tony.java,1,2,3,4,5,6,7,8,9,pos\n")

        # Simuliamo che csv_software_metric contenga dati
        mock_csv_software_metric = mock.mock_open(read_data="kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n"
                                                            "txt,tony.java,1,2,3,4,5,6,7,8,9,10,11,pos\n")

        # Creiamo un mock per new_Union e simuliamo un errore durante la scrittura
        mock_new_union = mock.mock_open()

        mock_new_union().write.side_effect = Exception("Errore durante l'unione dei due csv")

        # Patchiamo la funzione open per restituire i file mockati
        with mock.patch("builtins.open", side_effect=[
            mock_csv_mining.return_value,
            mock_csv_software_metric.return_value,
            mock_new_union.return_value
        ]):
            with self.assertRaises(Exception, msg="Errore durante l’unione dei due csv"):
                initialize(name_csv_mining, name_csv_soft_m, mock_new_union())

        # Verifica che csv_mining e csv_software_metric siano stati aperti correttamente
        mock_csv_mining.assert_called_with(name_csv_mining, "r+", encoding="utf-8")
        mock_csv_software_metric.assert_called_with(name_csv_soft_m, "r+", encoding="utf-8")

    def test_TC_13(self):
        output = io.StringIO()

        csv_mining_content = 'NameClass,a1,a2,a3,a4,a5,a6,a7,a8,a9,class\n' \
                             'tony.java,1,2,3,4,5,6,7,8,9,pos\n' \
                             'paky,1,2,3,4,5,6,7,8,9,pos\n' \
                             'dani,1,2,3,4,5,6,7,8,9,pos\n'

        csv_soft_m_content = 'kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n' \
                             'txt,nicola,1,2,3,4,5,6,7,8,9,10,11,pos\n' \
                             'txt,tony.java,1,2,3,4,5,6,7,8,9,10,11,pos\n'

        with mock.patch('builtins.open', mock.mock_open()) as mocked_open:
            mocked_open.side_effect = [
                mock.mock_open(read_data=csv_mining_content).return_value,
                mock.mock_open(read_data=csv_soft_m_content).return_value
            ]

            initialize("name_csv_mining.csv", "name_csv_soft_m.csv", output)

        output.seek(0)
        written_data = output.getvalue()
        print("Actual:\n", written_data)

        expected_output = "NameClass,a1,a2,a3,a4,a5,a6,a7,a8,a9,m1,m2,m3,m4,m5,m6,m7,m8,class\n" \
                          "tony.java,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,10,11,pos,pos\n"

        print("Expected:\n", expected_output)

        self.assertEqual(written_data.strip(), expected_output.strip())


'''
    def test_initialize_headers(self):
        output = io.StringIO()

        csv_mining_content = 'NameClass,a1,a2,a3,a4,a5,a6,a7,a8,a9,class\n'
        csv_soft_m_content = 'kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n'

        with patch('builtins.open') as mocked_open:
            mocked_open.side_effect = [
                mock_open(read_data=csv_mining_content).return_value,
                mock_open(read_data=csv_soft_m_content).return_value
            ]

            initialize("name_csv_mining.csv", "name_csv_soft_m.csv", output)

        output.seek(0)
        written_data = output.getvalue()

        expected_output = "NameClass,a1,a2,a3,a4,a5,a6,a7,a8,a9,m1,m2,m3,m4,m5,m6,m7,m8,class\n"
        self.assertEqual(written_data.strip(), expected_output.strip())


    @patch('os.getcwd', return_value='/home/')
    @patch('os.chdir')
    def test_cwd(self, mock_chdir, mock_getcwd):
        output = io.StringIO()

        # Usiamo il mock per aprire file in modo controllato
        with patch('builtins.open', mock_open(read_data='file1, data1, class1\n')):
            initialize("name_csv_mining.csv", "name_csv_soft_m.csv", output)

        expected_calls = [
            call(".."),
            call(".."),
            call("Text_Mining"),
            call(".."),
            call("Software_Metrics"),
            call(".."),
            call("Union/Union_TM_SM")
        ]

        mock_chdir.assert_has_calls(expected_calls, any_order=False)

        # Ritorno alla directory iniziale
        self.assertEqual(mock_getcwd.call_count, 1)
'''
