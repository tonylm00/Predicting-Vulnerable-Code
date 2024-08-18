import io
from Dataset2.Union.Union_SM_ASA.Union_SMwithASA import initialize, getClass, another_option
import pytest


class TestGetClass:

    def test_case_1(self):
        with pytest.raises(ValueError):
            getClass("")

    def test_case_2(self):
        assert getClass("a,b,c,pos") == "pos"
        assert getClass("x,neg") == "neg"
        assert getClass("1,2,3,4,5,pos") == "pos"

    def test_case_3(self):
        with pytest.raises(ValueError):
            getClass("a,b,c")


class TestAnotherOption:

    def test_case_1(self):
        with pytest.raises(ValueError):
            assert another_option(line_asa=None, line_sm=None, class_element=None) is None

    def test_case_2(self):
        with pytest.raises(ValueError):
            assert another_option(line_asa="", line_sm="", class_element="") is None

    def test_case_3(self):
        with pytest.raises(ValueError):
            assert another_option(line_asa="", line_sm=None, class_element=None) is None

    def test_case_4(self):
        with pytest.raises(ValueError):
            assert another_option(line_asa="a,b,c", line_sm=None, class_element=None) is None

    def test_case_5(self):
        with pytest.raises(ValueError):
            assert another_option(line_asa="a,b,c", line_sm=None, class_element="") is None

    def test_case_6(self):
        with pytest.raises(ValueError):
            assert another_option(line_asa="a,b,c", line_sm=None, class_element="x") is None

    def test_case_7(self):
        with pytest.raises(ValueError):
            assert another_option(line_asa="a,b,c", line_sm=None, class_element="pos") is None

    def test_case_8(self):
        assert another_option(line_asa="a,b,c,pos", line_sm=None, class_element="pos") == "b,c,"

    def test_case_9(self):
        with pytest.raises(ValueError):
            assert another_option(line_asa=None, line_sm="", class_element=None) is None

    def test_case_10(self):
        with pytest.raises(ValueError):
            assert another_option(line_asa=None, line_sm="a,b,c", class_element=None) is None

    def test_case_11(self):
        with pytest.raises(ValueError):
            assert another_option(line_asa=None, line_sm="a,b,c", class_element="") is None

    def test_case_12(self):
        with pytest.raises(ValueError):
            assert another_option(line_asa=None, line_sm="a,b,c", class_element="x") is None

    def test_case_13(self):
        with pytest.raises(ValueError):
            assert another_option(line_asa=None, line_sm="a,b,c", class_element="pos") is None

    def test_case_14(self):
        assert another_option(line_asa=None, line_sm="a,b,c,pos", class_element="pos") == "a,b,c,"


class TestInitialize:

    def test_case_1(self, mocker):
        mock_open = mocker.patch("builtins.open", new_callable=mocker.mock_open)
        with pytest.raises(FileNotFoundError):
            initialize("", "csv_ASA_final.csv", mock_open())

    def test_case_2(self, mocker):
        mock_open = mocker.patch("builtins.open", new_callable=mocker.mock_open)
        with pytest.raises(FileNotFoundError):
            initialize("not_mining_results_sm_final.csv", "csv_ASA_final.csv", mock_open())

    def test_case_3(self, mocker):
        mock_open = mocker.patch("builtins.open", new_callable=mocker.mock_open)
        with pytest.raises(FileNotFoundError):
            initialize("mining_results_sm_final.csv", "", mock_open())

    def test_case_4(self, mocker):
        mock_open = mocker.patch("builtins.open", new_callable=mocker.mock_open)
        with pytest.raises(FileNotFoundError):
            initialize("mining_results_sm_final.csv", "not_csv_ASA_final.csv", mock_open())

    def test_case_5(self, mocker):
        mock_open = mocker.patch("builtins.open", new_callable=mocker.mock_open, side_effect=FileNotFoundError)
        with pytest.raises(FileNotFoundError):
            initialize("mining_results_sm_final.csv", "csv_ASA_final.csv", mock_open())

    def test_case_6(self, mocker):
        mocker.patch("os.getcwd", return_value="/home")
        mocker.patch("os.chdir")

        name_csv_sm = "mining_results_sm_final.csv"
        name_csv_asa = "csv_ASA_final.csv"

        def open_side_effect(file_name, mode, encoding=None):
            if file_name == name_csv_sm:
                raise FileNotFoundError
            return mocker.mock_open().return_value

        mock_open = mocker.patch("builtins.open", side_effect=open_side_effect)

        with pytest.raises(FileNotFoundError):
            initialize(name_csv_sm, name_csv_asa, mock_open)

        mock_open.assert_called_with(name_csv_sm, "r+", encoding="utf-8")

    def test_case_7(self, mocker):
        mocker.patch("os.getcwd", return_value="/home")
        mocker.patch("os.chdir")

        name_csv_sm = "mining_results_sm_final.csv"
        name_csv_asa = "csv_ASA_final.csv"

        def open_side_effect(file_name, mode, encoding=None):
            if file_name == name_csv_asa:
                raise FileNotFoundError
            return mocker.mock_open().return_value

        mock_open = mocker.patch("builtins.open", side_effect=open_side_effect)

        with pytest.raises(FileNotFoundError):
            initialize(name_csv_sm, name_csv_asa, mock_open)

        mock_open.assert_called_with(name_csv_asa, "r+", encoding="utf-8")

    def test_case_8(self, mocker):
        mocker.patch("os.getcwd", return_value="/home/")
        mocker.patch("os.chdir")

        name_csv_sm = "mining_results_sm_final.csv"
        name_csv_asa = "csv_ASA_final.csv"

        mock_csv_sm = mocker.mock_open(read_data="")
        mock_csv_asa = mocker.mock_open(read_data='Name,java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,'
                                                  'java:asa7,java:asa8,java:asa9,java:asa10,java:asa11,java:asa12,'
                                                  'java:asa13,java:asa14,java:asa15,java:asa16,java:asa17,java:asa18,'
                                                  'java:asa19,java:asa20,java:asa21,class\n'
                                                  'paky.java,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,'
                                                  'm12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n'
                                                  'tony.java,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,'
                                                  'm12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n')
        mock_new_union = mocker.mock_open()

        mocker.patch("builtins.open", side_effect=[
            mock_csv_sm.return_value,
            mock_csv_asa.return_value,
            mock_new_union.return_value
        ])

        with pytest.raises(ValueError):
            initialize(name_csv_sm, name_csv_asa, mock_new_union)

        mock_csv_sm.assert_called_with(name_csv_sm, "r+", encoding="utf-8")

    def test_case_9(self, mocker):
        mocker.patch("os.getcwd", return_value="/home/")
        mocker.patch("os.chdir")

        name_csv_sm = "mining_results_sm_final.csv"
        name_csv_asa = "csv_ASA_final.csv"

        mock_csv_sm = mocker.mock_open(read_data='Kind,NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,'
                                                 'd,dd,ddd,dddd,e,ee,eee,eeee,class\n')

        mock_csv_asa = mocker.mock_open(read_data='Name,java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,'
                                                  'java:asa7,java:asa8,java:asa9,java:asa10,java:asa11,java:asa12,'
                                                  'java:asa13,java:asa14,java:asa15,java:asa16,java:asa17,java:asa18,'
                                                  'java:asa19,java:asa20,java:asa21,class\n'
                                                  'paky.java,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,'
                                                  'm12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n'
                                                  'tony.java,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,'
                                                  'm12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n')
        mock_new_union = mocker.mock_open()

        mocker.patch("builtins.open", side_effect=[
            mock_csv_sm.return_value,
            mock_csv_asa.return_value,
            mock_new_union.return_value
        ])

        with pytest.raises(ValueError):
            initialize(name_csv_sm, name_csv_asa, mock_new_union())

        mock_csv_sm.assert_called_with(name_csv_sm, "r+", encoding="utf-8")

    def test_case_10(self, mocker):
        mocker.patch("os.getcwd", return_value="/home/")
        mocker.patch("os.chdir")

        name_csv_sm = "mining_results_sm_final.csv"
        name_csv_asa = "csv_ASA_final.csv"

        mock_csv_sm = mocker.mock_open(read_data='Kind,NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,'
                                                 'dddd,e,ee,eee,eeee,class\n'
                                                 'File,tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,'
                                                 'd1,d2,d3,d4,e1,e2,e3,e4,pos\n'
                                                 'File,dani.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,'
                                                 'd1,d2,d3,d4,e1,e2,e3,e4,pos\n')
        mock_csv_asa = mocker.mock_open(read_data="")
        mock_new_union = mocker.mock_open()

        mocker.patch("builtins.open", side_effect=[
            mock_csv_sm.return_value,
            mock_csv_asa.return_value,
            mock_new_union.return_value
        ])

        with pytest.raises(ValueError, match="Errore, il file csv_software_metric è vuoto"):
            initialize(name_csv_sm, name_csv_asa, mock_new_union())

        mock_csv_asa.assert_called_with(name_csv_asa, "r+", encoding="utf-8")

    def test_case_11(self, mocker):
        mocker.patch("os.getcwd", return_value="/home/")
        mocker.patch("os.chdir")

        name_csv_sm = "mining_results_sm_final.csv"
        name_csv_asa = "csv_ASA_final.csv"

        mock_csv_sm = mocker.mock_open(read_data='Kind,NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,'
                                                 'dddd,e,ee,eee,eeee,class\n'
                                                 'File,tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,'
                                                 'd1,d2,d3,d4,e1,e2,e3,e4,pos\n'
                                                 'File,dani.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,'
                                                 'd1,d2,d3,d4,e1,e2,e3,e4,pos\n')

        mock_csv_asa = mocker.mock_open(read_data='Name,java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,'
                                                  'java:asa7,java:asa8,java:asa9,java:asa10,java:asa11,java:asa12,'
                                                  'java:asa13,java:asa14,java:asa15,java:asa16,java:asa17,java:asa18,'
                                                  'java:asa19,java:asa20,java:asa21,class\n')
        mock_new_union = mocker.mock_open()

        mocker.patch("builtins.open", side_effect=[
            mock_csv_sm.return_value,
            mock_csv_asa.return_value,
            mock_new_union.return_value
        ])

        with pytest.raises(ValueError, match="Errore, il file csv_asa contiene solo l’intestazione"):
            initialize(name_csv_sm, name_csv_asa, mock_new_union())

        mock_csv_asa.assert_called_with(name_csv_asa, "r+", encoding="utf-8")

    def test_case_12(self, mocker):
        mocker.patch("os.getcwd", return_value="/home/")
        mocker.patch("os.chdir")

        name_csv_sm = "mining_results_sm_final.csv"
        name_csv_asa = "csv_ASA_final.csv"

        mock_csv_sm = mocker.mock_open(read_data='Kind,NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,'
                                                 'dddd,e,ee,eee,eeee,class\n'
                                                 'File,tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,'
                                                 'd1,d2,d3,d4,e1,e2,e3,e4,pos\n'
                                                 'File,dani.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,'
                                                 'd1,d2,d3,d4,e1,e2,e3,e4,pos\n')

        mock_csv_asa = mocker.mock_open(read_data='Name,java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,'
                                                  'java:asa7,java:asa8,java:asa9,java:asa10,java:asa11,java:asa12,'
                                                  'java:asa13,java:asa14,java:asa15,java:asa16,java:asa17,java:asa18,'
                                                  'java:asa19,java:asa20,java:asa21,class\n'
                                                  'paky.java,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,'
                                                  'm12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n'
                                                  'tony.java,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,'
                                                  'm12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n')
        mock_new_union = mocker.mock_open()

        mock_new_union().write.side_effect = Exception("Errore durante l'unione dei due csv")

        mocker.patch("builtins.open", side_effect=[
            mock_csv_sm.return_value,
            mock_csv_asa.return_value,
            mock_new_union.return_value
        ])

        with pytest.raises(Exception, match="Errore durante l’unione dei due csv"):
            initialize(name_csv_sm, name_csv_asa, mock_new_union())

        mock_csv_sm.assert_called_with(name_csv_sm, "r+", encoding="utf-8")
        mock_csv_asa.assert_called_with(name_csv_asa, "r+", encoding="utf-8")

    def test_case_13(self, mocker):
        output = io.StringIO()

        csv_sm_content = 'Kind,NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,' \
                         'dddd,e,ee,eee,eeee,class\n' \
                         'File,tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,' \
                         'd1,d2,d3,d4,e1,e2,e3,e4,pos\n' \
                         'File,dani.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,' \
                         'd1,d2,d3,d4,e1,e2,e3,e4,pos\n'

        csv_asa_content = 'Name,java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,' \
                          'java:asa7,java:asa8,java:asa9,java:asa10,java:asa11,java:asa12,' \
                          'java:asa13,java:asa14,java:asa15,java:asa16,java:asa17,java:asa18,' \
                          'java:asa19,java:asa20,java:asa21,class\n' \
                          'paky.java,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,' \
                          'm12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n' \
                          'tony.java,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,' \
                          'm12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n'

        mocker.patch('builtins.open', side_effect=[
            mocker.mock_open(read_data=csv_sm_content).return_value,
            mocker.mock_open(read_data=csv_asa_content).return_value
        ])

        initialize("mining_results_sm_final.csv", "csv_ASA_final.csv", output)

        output.seek(0)
        written_data = output.getvalue()

        expected_output = "Kind,NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee," \
                          "java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,java:asa9," \
                          "java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,java:asa16,java:asa17," \
                          "java:asa18,java:asa19,class\n" \
                          "File,tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,m1,m2,m3,m4,m5," \
                          "m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n" \
                          "File,dani.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4," \
                          "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,pos\n"

        assert written_data.strip() == expected_output.strip()