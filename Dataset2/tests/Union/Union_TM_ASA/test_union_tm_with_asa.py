from Union.Union_TM_ASA.Union_TMwithASA import initialize, getClass, another_option
import pytest


class TestGetClass:

    @pytest.mark.parametrize("line, expected, property_l, property_c",
                             [("", "", "emptyString", None)])
    def test_case_1(self, line, expected, property_l, property_c):
        assert getClass(line) == expected

    @pytest.mark.parametrize("line, expected, property_l, property_c",
                             [("1,2,3,4,pos", "pos", "notEmptyString", "classElement")])
    def test_case_2(self, line, expected, property_l, property_c):
        assert getClass(line) == expected

    @pytest.mark.parametrize("line, expected, property_l, property_c",
                             [("a,b,c", "c", "notEmptyString", "noClassElement")])
    def test_case_3(self, line, expected, property_l, property_c):
        assert getClass(line) == expected


class TestAnotherOption:

    def test_case_1(self):
        with pytest.raises(AttributeError):
            assert another_option(line_asa=None, line_tm=None, class_element=None)

    def test_case_2(self):
        assert another_option(line_asa="", line_tm="", class_element="") is None

    def test_case_3(self):
        with pytest.raises(AttributeError):
            assert another_option(line_asa=None, line_tm=None, class_element="x")

    def test_case_4(self):
        with pytest.raises(ValueError):
            assert another_option(line_asa=None, line_tm="a,b,c", class_element="pos")

    def test_case_5(self):
        assert another_option(line_asa=None, line_tm="a,b,c,pos", class_element="pos") == "a,b,c,"

    def test_case_6(self):
        with pytest.raises(ValueError):
            assert another_option(line_tm=None, line_asa="a,b,c,pos", class_element="neg")

    def test_case_7(self):
        assert another_option(line_tm=None, line_asa="a,b,c,pos", class_element="pos") == "b,c,"

    def test_case_8(self):
        assert another_option(line_tm="a,b,c,d,pos", line_asa="a,b,c,pos", class_element="pos") is None


class TestInitialize:

    def test_case_1(self, fixture_both_csv, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        with pytest.raises(FileNotFoundError):
            with output_file_path.open("w") as output:
                initialize("", "csv_ASA_final.csv", output)

        written_data = output_file_path.read_text()
        assert written_data == ""

    def test_case_2(self, fixture_both_csv, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        with pytest.raises(FileNotFoundError):
            with output_file_path.open("w") as output:
                initialize("not_csv_mining_final.csv", "csv_ASA_final.csv", output)

        written_data = output_file_path.read_text()
        assert written_data == ""

    def test_case_3(self, fixture_both_csv, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        with pytest.raises(FileNotFoundError):
            with output_file_path.open("w") as output:
                initialize("csv_mining_final.csv", "", output)

        written_data = output_file_path.read_text()
        assert written_data == ""

    def test_case_4(self, fixture_both_csv, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        with pytest.raises(FileNotFoundError):
            with output_file_path.open("w") as output:
                initialize("csv_mining_final.csv", "not_csv_ASA_final.csv", output)

        written_data = output_file_path.read_text()
        assert written_data == ""

    def test_case_5(self, fixture_both_csv, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        output_file_path.touch()
        output_file_path.chmod(0o444)

        with pytest.raises(PermissionError):
            initialize("csv_mining_final.csv", "csv_ASA_final.csv",
                       output_file_path.open("w"))

        output_file_path.chmod(0o666)

    def test_case_6(self, fixture_only_asa, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        # Esegui la funzione initialize e verifica che sollevi un FileNotFoundError
        with pytest.raises(FileNotFoundError):
            with output_file_path.open("w") as output:
                initialize("csv_mining_final.csv", "csv_ASA_final.csv", output)

    def test_case_7(self, fixture_both_csv_empty, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        # Esegui la funzione initialize usando i file temporanei
        with output_file_path.open("w") as output:
            initialize("csv_mining_final.csv", "csv_ASA_final.csv", output)

        assert output_file_path.read_text() == ""

    def test_case_8(self, fixture_header_csv, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        with output_file_path.open("w") as output:
            initialize("csv_mining_final.csv", "csv_ASA_final.csv", output)

        written_data = output_file_path.read_text()

        expected_output = 'NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,' \
                          'java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,java:asa9,' \
                          'java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,java:asa16,java:asa17,' \
                          'java:asa18,java:asa19,class'

        assert written_data.strip() == expected_output.strip()

    def test_case_9(self, fixture_only_tm, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        # Esegui la funzione initialize e verifica che sollevi un FileNotFoundError
        with pytest.raises(FileNotFoundError):
            with output_file_path.open("w") as output:
                initialize("csv_mining_final.csv", "csv_ASA_final.csv", output)

    def test_case_10(self, fixture_empty_asa, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        with output_file_path.open("w") as output:
            initialize("csv_mining_final.csv", "csv_ASA_final.csv", output)

        written_data = output_file_path.read_text()

        expected_output = 'Kind,NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,' \
                          'd,dd,ddd,dddd,e,ee,eee,eeee,class\n' \
                          'File,tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,0,0,0,0,0,0,0,' \
                          '0,0,0,0,0,0,0,0,0,0,0,0,pos\n' \
                          'File,dani.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,0,0,0,0,0,0,0,' \
                          '0,0,0,0,0,0,0,0,0,0,0,0,pos '

        assert written_data.strip() == expected_output.strip()

    def test_case_11(self, fixture_header_asa, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        with output_file_path.open("w") as output:
            initialize("csv_mining_final.csv", "csv_ASA_final.csv", output)

        written_data = output_file_path.read_text()

        expected_output = 'Kind,NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,' \
                          'java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,java:asa9,' \
                          'java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,java:asa16,java:asa17,' \
                          'java:asa18,java:asa19,class\nFile,tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,' \
                          'd4,e1,e2,e3,e4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,pos\n' \
                          'File,dani.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,0,0,0,0,0,0,0,' \
                          '0,0,0,0,0,0,0,0,0,0,0,0,pos '

        assert written_data.strip() == expected_output.strip()

    def test_case_12(self, fixture_both_csv, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        # Esegui la funzione initialize usando i file temporanei
        with output_file_path.open("w") as output:
            initialize("csv_mining_final.csv", "csv_ASA_final.csv", output)

        # Leggi il contenuto dell'output per verificare
        written_data = output_file_path.read_text()

        expected_output = "NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee," \
                          "java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,java:asa9," \
                          "java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,java:asa16,java:asa17," \
                          "java:asa18,java:asa19,class\n" \
                          "tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,m1,m2,m3,m4,m5,m6,m7," \
                          "m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n"

        assert written_data.strip() == expected_output.strip()
