from Dataset2.Union.Union_SM_ASA.Union_SMwithASA import initialize, getClass, another_option
import pytest


class TestGetClass:

    def test_case_1(self):
        assert getClass("") == ""

    def test_case_2(self):
        assert getClass("1,2,3,4,pos") == "pos"

    def test_case_3(self):
        assert getClass("a,b,c") == "c"


class TestAnotherOption:

    def test_case_1(self):
        with pytest.raises(AttributeError):
            assert another_option(line_asa=None, line_sm=None, class_element=None)

    def test_case_2(self):
        assert another_option(line_asa="", line_sm="", class_element="") is None

    def test_case_3(self):
        with pytest.raises(AttributeError):
            assert another_option(line_asa="", line_sm=None, class_element=None)

    def test_case_4(self):
        with pytest.raises(AttributeError):
            assert another_option(line_asa="a,b,c", line_sm=None, class_element=None)

    def test_case_5(self):
        with pytest.raises(ValueError):
            assert another_option(line_asa="a,b,c", line_sm=None, class_element="")

    def test_case_6(self):
        with pytest.raises(ValueError):
            assert another_option(line_asa="a,b,c", line_sm=None, class_element="pos")

    def test_case_7(self):
        assert another_option(line_asa="a,b,c,pos", line_sm=None, class_element="pos") == "b,c,"

    def test_case_8(self):
        with pytest.raises(ValueError):
            assert another_option(line_asa=None, line_sm="", class_element=None)

    def test_case_9(self):
        with pytest.raises(ValueError):
            assert another_option(line_asa=None, line_sm="a,b,c", class_element=None)

    def test_case_10(self):
        with pytest.raises(ValueError):
            assert another_option(line_asa=None, line_sm="a,b,c", class_element="")

    def test_case_11(self):
        with pytest.raises(ValueError):
            assert another_option(line_asa=None, line_sm="a,b,c", class_element="pos")

    def test_case_12(self):
        assert another_option(line_asa=None, line_sm="a,b,c,pos", class_element="pos") == "a,b,c,"


class TestInitialize:

    def test_case_1(self, fixture_both_csv, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        with pytest.raises(FileNotFoundError):
            with output_file_path.open("w", encoding="utf-8") as output:
                initialize("", "csv_ASA_final.csv", output)

        written_data = output_file_path.read_text()
        assert written_data == ""

    def test_case_2(self, fixture_both_csv, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        with pytest.raises(FileNotFoundError):
            with output_file_path.open("w", encoding="utf-8") as output:
                initialize("not_mining_results_sm_final.csv", "csv_ASA_final.csv", output)

        written_data = output_file_path.read_text()
        assert written_data == ""

    def test_case_3(self, fixture_both_csv, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        with pytest.raises(FileNotFoundError):
            with output_file_path.open("w", encoding="utf-8") as output:
                initialize("mining_results_sm_final.csv", "", output)

        written_data = output_file_path.read_text()
        assert written_data == ""

    def test_case_4(self, fixture_both_csv, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        with pytest.raises(FileNotFoundError):
            with output_file_path.open("w", encoding="utf-8") as output:
                initialize("mining_results_sm_final.csv", "not_csv_ASA_final.csv", output)

        written_data = output_file_path.read_text()
        assert written_data == ""

    def test_case_5(self, fixture_both_csv, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        # Creiamo il file e lo impostiamo in modalità di sola lettura per simulare un `PermissionError`
        output_file_path.touch()
        output_file_path.chmod(0o444)  # Imposta il file in modalità sola lettura

        # Esegui la funzione initialize e verifica che sollevi un `PermissionError`
        with pytest.raises(PermissionError):
            initialize("mining_results_sm_final.csv", "csv_ASA_final.csv",
                       output_file_path.open("w", encoding="utf-8"))

        # Ripristina i permessi del file dopo il test per evitare problemi
        output_file_path.chmod(0o666)

    def test_case_6(self, fixture_only_asa, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        # Esegui la funzione initialize e verifica che sollevi un FileNotFoundError
        with pytest.raises(FileNotFoundError):
            with output_file_path.open("w", encoding="utf-8") as output:
                initialize("mining_results_sm_final.csv", "csv_ASA_final.csv", output)

    def test_case_7(self, fixture_only_sm, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        # Esegui la funzione initialize e verifica che sollevi un FileNotFoundError
        with pytest.raises(FileNotFoundError):
            with output_file_path.open("w", encoding="utf-8") as output:
                initialize("mining_results_sm_final.csv", "csv_ASA_final.csv", output)

    def test_case_8(self, fixture_empty_sm, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        with output_file_path.open("w", encoding="utf-8") as output:
            initialize("mining_results_sm_final.csv", "csv_ASA_final.csv", output)

        # Leggi il contenuto dell'output per verificare
        written_data = output_file_path.read_text()

        expected_output = ""

        assert written_data.strip() == expected_output.strip()

    def test_case_9(self, fixture_header_sm, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        with output_file_path.open("w", encoding="utf-8") as output:
            initialize("mining_results_sm_final.csv", "csv_ASA_final.csv", output)

        written_data = output_file_path.read_text()

        expected_output = 'Kind,NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,' \
                          'java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,java:asa9,' \
                          'java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,java:asa16,java:asa17,' \
                          'java:asa18,java:asa19,class '

        assert written_data.strip() == expected_output.strip()

    def test_case_10(self, fixture_empty_asa, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        with output_file_path.open("w", encoding="utf-8") as output:
            initialize("mining_results_sm_final.csv", "csv_ASA_final.csv", output)

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

        with output_file_path.open("w", encoding="utf-8") as output:
            initialize("mining_results_sm_final.csv", "csv_ASA_final.csv", output)

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
        with output_file_path.open("w", encoding="utf-8") as output:
            initialize("mining_results_sm_final.csv", "csv_ASA_final.csv", output)

        # Leggi il contenuto dell'output per verificare
        written_data = output_file_path.read_text()

        expected_output = "Kind,NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee," \
                          "java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,java:asa9," \
                          "java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,java:asa16,java:asa17," \
                          "java:asa18,java:asa19,class\n" \
                          "File,tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,m1,m2,m3,m4,m5," \
                          "m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n" \
                          "File,dani.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4," \
                          "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,pos\n"

        assert written_data.strip() == expected_output.strip()
