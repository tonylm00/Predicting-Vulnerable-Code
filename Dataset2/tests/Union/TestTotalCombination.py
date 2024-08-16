from Dataset2.Union.Total_Combination.TotalCombination import initialize, getClass, another_option
import unittest
from unittest import mock
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
            initialize("not_Union_TM_ASA.csv", "mining_results_sm_final.csv", mock_file())

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_TC_3(self, mock_file):

        with self.assertRaises(FileNotFoundError):
            initialize("Union_TM_ASA.csv", "", mock_file())

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_TC_4(self, mock_file):

        with self.assertRaises(FileNotFoundError):
            initialize("Union_TM_ASA.csv", "not_mining_results_sm_final.csv", mock_file())

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_TC_5(self, mock_file):

        mock_file.side_effect = FileNotFoundError

        with self.assertRaises(FileNotFoundError):
            initialize("Union_TM_ASA.csv", "mining_results_sm_final.csv", mock_file())

    @mock.patch("os.getcwd", return_value="/home")
    @mock.patch("os.chdir")
    def test_TC_6(self, mock_chdir, mock_getcwd):

        name_csv_mining = "Union_TM_ASA.csv"
        name_csv_soft_m = "mining_results_sm_final.csv"

        def open_side_effect(file_name, mode, encoding=None):
            if file_name == name_csv_mining:
                raise FileNotFoundError
            else:
                # Usa un mock standard per altri file
                return mock.mock_open().return_value

        with mock.patch("builtins.open", side_effect=open_side_effect) as mock_open:
            with self.assertRaises(FileNotFoundError):
                # Chiamata alla funzione da testare
                initialize(name_csv_mining, name_csv_soft_m, mock_open)

        mock_open.assert_called_with(name_csv_mining, "r+", encoding="utf-8")

    @mock.patch("os.getcwd", return_value="/home")
    @mock.patch("os.chdir")
    def test_TC_7(self, mock_chdir, mock_getcwd):

        name_csv_mining = "Union_TM_ASA.csv"
        name_csv_soft_m = "mining_results_sm_final.csv"

        def open_side_effect(file_name, mode, encoding=None):
            if file_name == name_csv_soft_m:
                raise FileNotFoundError
            else:
                # Usa un mock standard per altri file
                return mock.mock_open().return_value

        with mock.patch("builtins.open", side_effect=open_side_effect) as mock_open:
            with self.assertRaises(FileNotFoundError):
                # Chiamata alla funzione da testare
                initialize(name_csv_mining, name_csv_soft_m, mock_open)

        mock_open.assert_called_with(name_csv_soft_m, "r+", encoding="utf-8")

    @mock.patch("os.getcwd", return_value="/home/")
    @mock.patch("os.chdir")
    def test_TC_8(self, mock_chdir, mock_getcwd):
        name_csv_mining = "Union_TM_ASA.csv"
        name_csv_soft_m = "mining_results_sm_final.csv"

        mock_csv_mining = mock.mock_open(read_data="")

        # inserire correttamente i dati
        mock_csv_software_metric = mock.mock_open(read_data="kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n")

        mock_new_union = mock.mock_open()

        with mock.patch("builtins.open",
                        side_effect=[
                            mock_csv_mining.return_value,
                            mock_csv_software_metric.return_value,
                            mock_new_union.return_value
                        ]):
            with self.assertRaises(ValueError):
                initialize(name_csv_mining, name_csv_soft_m, mock_new_union)

        mock_csv_mining.assert_called_with(name_csv_mining, "r+", encoding="utf-8")

    @mock.patch("os.getcwd", return_value="/home/")
    @mock.patch("os.chdir")
    def test_TC_9(self, mock_chdir, mock_getcwd):
        name_csv_mining = "Union_TM_ASA.csv"
        name_csv_soft_m = "mining_results_sm_final.csv"

        mock_csv_mining = mock.mock_open(read_data=
                                         "NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,"
                                         "eeee,java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,"
                                         "java:asa8,java:asa9,java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,"
                                         "java:asa15,java:asa16,java:asa17,java:asa18,java:asa19,class\n")

        mock_csv_software_metric = mock.mock_open(read_data=
                                                  'kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n'
                                                  'txt,nicola,1,2,3,4,5,6,7,8,9,10,11,pos\n'
                                                  'txt,tony.java,1,2,3,4,5,6,7,8,9,10,11,pos\n')

        mock_new_union = mock.mock_open()

        with mock.patch("builtins.open", side_effect=[
            mock_csv_mining.return_value,
            mock_csv_software_metric.return_value,
            mock_new_union.return_value
        ]):
            with self.assertRaises(ValueError, msg="Errore, il file csv_mining contiene solo l'intestazione"):
                initialize(name_csv_mining, name_csv_soft_m, mock_new_union())

        mock_csv_mining.assert_called_with(name_csv_mining, "r+", encoding="utf-8")
        self.assertEqual(len(mock_csv_mining().readlines()), 1)

    @mock.patch("os.getcwd", return_value="/home/")
    @mock.patch("os.chdir")
    def test_TC_10(self, mock_chdir, mock_getcwd):
        name_csv_mining = "Union_TM_ASA.csv"
        name_csv_soft_m = "mining_results_sm_final.csv"

        mock_csv_mining = mock.mock_open(
            read_data="NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,"
                      "java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,"
                      "java:asa9,java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,"
                      "java:asa16,java:asa17,java:asa18,java:asa19,class\n"
                      "tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,"
                      "m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n")

        mock_csv_software_metric = mock.mock_open(read_data="")
        mock_new_union = mock.mock_open()

        with mock.patch("builtins.open", side_effect=[
            mock_csv_mining.return_value,
            mock_csv_software_metric.return_value,
            mock_new_union.return_value
        ]):
            with self.assertRaises(ValueError):
                initialize(name_csv_mining, name_csv_soft_m, mock_new_union())

        mock_csv_software_metric.assert_called_with(name_csv_soft_m, "r+", encoding="utf-8")

    @mock.patch("os.getcwd", return_value="/home/")
    @mock.patch("os.chdir")
    def test_TC_11(self, mock_chdir, mock_getcwd):
        name_csv_mining = "Union_TM_ASA.csv"
        name_csv_soft_m = "mining_results_sm_final.csv"

        mock_csv_mining = mock.mock_open(
            read_data="NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,"
                      "java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,"
                      "java:asa9,java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,"
                      "java:asa16,java:asa17,java:asa18,java:asa19,class\n"
                      "tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,"
                      "m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n")

        mock_csv_software_metric = mock.mock_open(read_data='kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n')
        mock_new_union = mock.mock_open()

        with mock.patch("builtins.open", side_effect=[
            mock_csv_mining.return_value,
            mock_csv_software_metric.return_value,
            mock_new_union.return_value
        ]):
            with self.assertRaises(ValueError, msg="Errore, il file csv_software_metric contiene solo l’intestazione"):
                initialize(name_csv_mining, name_csv_soft_m, mock_new_union())

        mock_csv_software_metric.assert_called_with(name_csv_soft_m, "r+", encoding="utf-8")

    @mock.patch("os.getcwd", return_value="/home/")
    @mock.patch("os.chdir")
    def test_TC_12(self, mock_chdir, mock_getcwd):
        name_csv_mining = "Union_TM_ASA.csv"
        name_csv_soft_m = "mining_results_sm_final.csv"

        mock_csv_mining = mock.mock_open(
            read_data="NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,"
                      "java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,"
                      "java:asa9,java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,"
                      "java:asa16,java:asa17,java:asa18,java:asa19,class\n"
                      "tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,"
                      "m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n")

        mock_csv_software_metric = mock.mock_open(read_data=
                                                  'kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n'
                                                  'txt,nicola,1,2,3,4,5,6,7,8,9,10,11,pos\n'
                                                  'txt,tony.java,1,2,3,4,5,6,7,8,9,10,11,pos\n')

        mock_new_union = mock.mock_open()
        mock_new_union().write.side_effect = Exception("Errore durante l'unione dei due csv")

        with mock.patch("builtins.open", side_effect=[
            mock_csv_mining.return_value,
            mock_csv_software_metric.return_value,
            mock_new_union.return_value
        ]):
            with self.assertRaises(Exception, msg="Errore durante l’unione dei due csv"):
                initialize(name_csv_mining, name_csv_soft_m, mock_new_union())

        mock_csv_mining.assert_called_with(name_csv_mining, "r+", encoding="utf-8")
        mock_csv_software_metric.assert_called_with(name_csv_soft_m, "r+", encoding="utf-8")

    def test_TC_13(self):
        output = io.StringIO()

        csv_mining_content = "NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee," \
                             "java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8," \
                             "java:asa9,java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15," \
                             "java:asa16,java:asa17,java:asa18,java:asa19,class\n" \
                             "tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4," \
                             "m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n"

        csv_soft_m_content = 'kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n' \
                             'txt,nicola,1,2,3,4,5,6,7,8,9,10,11,pos\n' \
                             'txt,tony.java,1,2,3,4,5,6,7,8,9,10,11,pos\n'

        with mock.patch('builtins.open', mock.mock_open()) as mocked_open:
            mocked_open.side_effect = [
                mock.mock_open(read_data=csv_mining_content).return_value,
                mock.mock_open(read_data=csv_soft_m_content).return_value
            ]

            initialize("Union_TM_ASA.csv", "mining_results_sm_final.csv", output)

        output.seek(0)
        written_data = output.getvalue()
        print("Actual:\n", written_data)

        expected_output = "NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee," \
                          "java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8," \
                          "java:asa9,java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15," \
                          "java:asa16,java:asa17,java:asa18,java:asa19,class\n" \
                          "tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4," \
                          "m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21" \
                          ",1,2,3,4,5,6,7,8,9,10,11,pos,pos\n"

        print("Expected:\n", expected_output)

        self.assertEqual(written_data.strip(), expected_output.strip())
