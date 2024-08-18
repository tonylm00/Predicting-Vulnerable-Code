from Dataset2.Union.Total_Combination.TotalCombination import initialize, getClass, another_option
import io
import pytest


class TestGetClass:

    def test_case_1(self):
        with pytest.raises(ValueError):
            getClass("")

    def test_case_2(self):
        assert getClass("a,b,c,pos") == "pos"
        assert getClass("x,neg") == "neg"
        assert getClass("1,2,3,4,5,pos") == "pos"
        assert getClass("1,2,3") == "3"

    def test_case_3(self):
        with pytest.raises(ValueError):
            getClass("a,b,c")


class TestAnotherOption:

    def test_case_1(self):
        with pytest.raises(ValueError):
            assert another_option(line_sm=None, line_tm=None, class_element=None) is None

    def test_case_2(self):
        with pytest.raises(ValueError):
            assert another_option(line_sm="", line_tm="", class_element="") is None

    def test_case_3(self):
        with pytest.raises(ValueError):
            assert another_option(line_sm=None, line_tm="", class_element=None) is None

    def test_case_4(self):
        with pytest.raises(ValueError):
            assert another_option(line_sm=None, line_tm="a,b,c,pos", class_element=None) is None

    def test_case_5(self):
        with pytest.raises(ValueError):
            assert another_option(line_sm=None, line_tm="a,b,c,pos", class_element="x") is None

    def test_case_6(self):
        with pytest.raises(ValueError):
            assert another_option(line_sm=None, line_tm="a,b,c,pos", class_element="neg") is None

    def test_case_7(self):
        assert another_option(line_sm=None, line_tm="a,b,c,pos", class_element="pos") == "a,b,c,"

    def test_case_8(self):
        with pytest.raises(ValueError):
            assert another_option(line_sm="", line_tm=None, class_element=None) is None

    def test_case_9(self):
        assert another_option(line_sm="a,b,c,d,e", line_tm=None, class_element=None) == "c,d,e,"


class TestInitialize:

    def test_case_1(self, mocker):
        mock_open = mocker.patch("builtins.open", new_callable=mocker.mock_open)
        with pytest.raises(FileNotFoundError):
            initialize("", "mining_results_sm_final.csv", mock_open())

    def test_case_2(self, mocker):
        mock_open = mocker.patch("builtins.open", new_callable=mocker.mock_open)
        with pytest.raises(FileNotFoundError):
            initialize("not_Union_TM_ASA.csv", "mining_results_sm_final.csv", mock_open())

    def test_case_3(self, mocker):
        mock_open = mocker.patch("builtins.open", new_callable=mocker.mock_open)
        with pytest.raises(FileNotFoundError):
            initialize("Union_TM_ASA.csv", "", mock_open())

    def test_case_4(self, mocker):
        mock_open = mocker.patch("builtins.open", new_callable=mocker.mock_open)
        with pytest.raises(FileNotFoundError):
            initialize("Union_TM_ASA.csv", "not_mining_results_sm_final.csv", mock_open())

    def test_case_5(self, mocker):
        mock_open = mocker.patch("builtins.open", new_callable=mocker.mock_open, side_effect=FileNotFoundError)
        with pytest.raises(FileNotFoundError):
            initialize("Union_TM_ASA.csv", "mining_results_sm_final.csv", mock_open())

    def test_case_6(self, mocker):
        mocker.patch("os.getcwd", return_value="/home")
        mocker.patch("os.chdir")

        name_csv_mining = "Union_TM_ASA.csv"
        name_csv_soft_m = "mining_results_sm_final.csv"

        def open_side_effect(file_name, mode):
            if file_name == name_csv_mining:
                raise FileNotFoundError
            return mocker.mock_open().return_value

        mock_open = mocker.patch("builtins.open", side_effect=open_side_effect)

        with pytest.raises(FileNotFoundError):
            initialize(name_csv_mining, name_csv_soft_m, mock_open)

        mock_open.assert_called_with(name_csv_mining, "r+")

    def test_case_7(self, mocker):
        mocker.patch("os.getcwd", return_value="/home")
        mocker.patch("os.chdir")

        name_csv_mining = "Union_TM_ASA.csv"
        name_csv_soft_m = "mining_results_sm_final.csv"

        def open_side_effect(file_name, mode):
            if file_name == name_csv_soft_m:
                raise FileNotFoundError
            return mocker.mock_open().return_value

        mock_open = mocker.patch("builtins.open", side_effect=open_side_effect)

        with pytest.raises(FileNotFoundError):
            initialize(name_csv_mining, name_csv_soft_m, mock_open)

        mock_open.assert_called_with(name_csv_soft_m, "r+")

    def test_case_8(self, mocker):
        mocker.patch("os.getcwd", return_value="/home/")
        mocker.patch("os.chdir")

        name_csv_mining = "Union_TM_ASA.csv"
        name_csv_soft_m = "mining_results_sm_final.csv"

        mock_csv_mining = mocker.mock_open(read_data="")
        mock_csv_software_metric = mocker.mock_open(read_data="kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n")
        mock_new_union = mocker.mock_open()

        mocker.patch("builtins.open", side_effect=[
            mock_csv_mining.return_value,
            mock_csv_software_metric.return_value,
            mock_new_union.return_value
        ])

        with pytest.raises(ValueError):
            initialize(name_csv_mining, name_csv_soft_m, mock_new_union)

        mock_csv_mining.assert_called_with(name_csv_mining, "r+", encoding="utf-8")

    def test_case_9(self, mocker):
        mocker.patch("os.getcwd", return_value="/home/")
        mocker.patch("os.chdir")

        name_csv_mining = "Union_TM_ASA.csv"
        name_csv_soft_m = "mining_results_sm_final.csv"

        mock_csv_mining = mocker.mock_open(read_data=
                                           "NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,java:asa1,java:asa2,"
                                           "java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,java:asa9,java:asa10,java:asa11,java:asa12,"
                                           "java:asa13,java:asa14,java:asa15,java:asa16,java:asa17,java:asa18,java:asa19,class\n"
                                           )

        mock_csv_software_metric = mocker.mock_open(read_data=
                                                    'kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n'
                                                    'txt,nicola,1,2,3,4,5,6,7,8,9,10,11,pos\n'
                                                    'txt,tony.java,1,2,3,4,5,6,7,8,9,10,11,pos\n'
                                                    )
        mock_new_union = mocker.mock_open()

        mocker.patch("builtins.open", side_effect=[
            mock_csv_mining.return_value,
            mock_csv_software_metric.return_value,
            mock_new_union.return_value
        ])

        with pytest.raises(ValueError, match="Errore, il file csv_mining contiene solo l'intestazione"):
            initialize(name_csv_mining, name_csv_soft_m, mock_new_union())

        mock_csv_mining.assert_called_with(name_csv_mining, "r+", encoding="utf-8")
        assert len(mock_csv_mining().readlines()) == 1

    def test_case_10(self, mocker):
        mocker.patch("os.getcwd", return_value="/home/")
        mocker.patch("os.chdir")

        name_csv_mining = "Union_TM_ASA.csv"
        name_csv_soft_m = "mining_results_sm_final.csv"

        mock_csv_mining = mocker.mock_open(
            read_data="NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,"
                      "java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,"
                      "java:asa9,java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,"
                      "java:asa16,java:asa17,java:asa18,java:asa19,class\n"
                      "tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,"
                      "m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n"
        )

        mock_csv_software_metric = mocker.mock_open(read_data="")
        mock_new_union = mocker.mock_open()

        mocker.patch("builtins.open", side_effect=[
            mock_csv_mining.return_value,
            mock_csv_software_metric.return_value,
            mock_new_union.return_value
        ])

        with pytest.raises(ValueError):
            initialize(name_csv_mining, name_csv_soft_m, mock_new_union())

        mock_csv_software_metric.assert_called_with(name_csv_soft_m, "r+", encoding="utf-8")

    def test_case_11(self, mocker):
        mocker.patch("os.getcwd", return_value="/home/")
        mocker.patch("os.chdir")

        name_csv_mining = "Union_TM_ASA.csv"
        name_csv_soft_m = "mining_results_sm_final.csv"

        mock_csv_mining = mocker.mock_open(
            read_data="NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,"
                      "java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,"
                      "java:asa9,java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,"
                      "java:asa16,java:asa17,java:asa18,java:asa19,class\n"
                      "tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,"
                      "m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n"
        )

        mock_csv_software_metric = mocker.mock_open(read_data='kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n')
        mock_new_union = mocker.mock_open()

        mocker.patch("builtins.open", side_effect=[
            mock_csv_mining.return_value,
            mock_csv_software_metric.return_value,
            mock_new_union.return_value
        ])

        with pytest.raises(ValueError, match="Errore, il file csv_software_metric contiene solo l’intestazione"):
            initialize(name_csv_mining, name_csv_soft_m, mock_new_union())

        mock_csv_software_metric.assert_called_with(name_csv_soft_m, "r+", encoding="utf-8")

    def test_case_12(self, mocker):
        mocker.patch("os.getcwd", return_value="/home/")
        mocker.patch("os.chdir")

        name_csv_mining = "Union_TM_ASA.csv"
        name_csv_soft_m = "mining_results_sm_final.csv"

        mock_csv_mining = mocker.mock_open(
            read_data="NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,"
                      "java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,"
                      "java:asa9,java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,"
                      "java:asa16,java:asa17,java:asa18,java:asa19,class\n"
                      "tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,"
                      "m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n"
        )

        mock_csv_software_metric = mocker.mock_open(read_data=
                                                    'kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n'
                                                    'txt,nicola,1,2,3,4,5,6,7,8,9,10,11,pos\n'
                                                    'txt,tony.java,1,2,3,4,5,6,7,8,9,10,11,pos\n'
                                                    )

        mock_new_union = mocker.mock_open()
        mock_new_union().write.side_effect = Exception("Errore durante l'unione dei due csv")

        mocker.patch("builtins.open", side_effect=[
            mock_csv_mining.return_value,
            mock_csv_software_metric.return_value,
            mock_new_union.return_value
        ])

        with pytest.raises(Exception, match="Errore durante l’unione dei due csv"):
            initialize(name_csv_mining, name_csv_soft_m, mock_new_union())

        mock_csv_mining.assert_called_with(name_csv_mining, "r+", encoding="utf-8")
        mock_csv_software_metric.assert_called_with(name_csv_soft_m, "r+", encoding="utf-8")

    def test_case_13(self, mocker):
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

        mocker.patch('builtins.open', side_effect=[
            mocker.mock_open(read_data=csv_mining_content).return_value,
            mocker.mock_open(read_data=csv_soft_m_content).return_value
        ])

        initialize("Union_TM_ASA.csv", "mining_results_sm_final.csv", output)

        output.seek(0)
        written_data = output.getvalue()

        expected_output = "NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee," \
                          "java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8," \
                          "java:asa9,java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15," \
                          "java:asa16,java:asa17,java:asa18,java:asa19,class\n" \
                          "tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4," \
                          "m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21," \
                          "1,2,3,4,5,6,7,8,9,10,11,pos,pos\n"

        assert written_data.strip() == expected_output.strip()
