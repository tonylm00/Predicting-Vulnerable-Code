from Dataset2.Union.Union_TM_SM.Union import initialize, getClass, another_option
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
            assert another_option(line_sm=None, line_tm=None, class_element=None) is None

    def test_case_2(self):
        assert another_option(line_sm="", line_tm="", class_element="") is None

    def test_case_3(self):
        with pytest.raises(ValueError):
            assert another_option(line_sm=None, line_tm="", class_element=None) is None

    def test_case_4(self):
        with pytest.raises(ValueError):
            assert another_option(line_sm=None, line_tm="a,b,c,pos", class_element=None) is None

    def test_case_5(self):
        with pytest.raises(ValueError):
            assert another_option(line_sm=None, line_tm="a,b,c,pos", class_element="")

    def test_case_6(self):
        with pytest.raises(ValueError):
            assert another_option(line_sm=None, line_tm="a,b,c,pos", class_element="x") is None

    def test_case_7(self):
        assert another_option(line_sm=None, line_tm="a,b,c,pos", class_element="pos") == "a,b,c,"

    def test_case_8(self):
        assert another_option(line_sm="", line_tm=None, class_element=None) == ""

    def test_case_9(self):
        assert another_option(line_sm="a,b,c,d,e", line_tm=None, class_element=None) == "c,d,e,"


class TestInitialize:

    def test_case_1(self, fixture_both_csv, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        with pytest.raises(FileNotFoundError):
            with output_file_path.open("w") as output:
                initialize("", "mining_results_sm_final.csv", output)

        written_data = output_file_path.read_text()
        assert written_data == ""

    def test_case_2(self, fixture_both_csv, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        with pytest.raises(FileNotFoundError):
            with output_file_path.open("w") as output:
                initialize("not_csv_mining_final", "mining_results_sm_final.csv", output)

        written_data = output_file_path.read_text()
        assert written_data == ""

    def test_case_3(self, fixture_both_csv, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        with pytest.raises(FileNotFoundError):
            with output_file_path.open("w") as output:
                initialize("csv_mining_final", "", output)

        written_data = output_file_path.read_text()
        assert written_data == ""

    def test_case_4(self, fixture_both_csv, base_fixture):

        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        with pytest.raises(FileNotFoundError):
            with output_file_path.open("w") as output:
                initialize("csv_mining_final", "not_mining_results_sm_final", output)

        written_data = output_file_path.read_text()
        assert written_data == ""

    def test_case_5(self, fixture_both_csv, base_fixture):
        # Percorso del file di output nella directory temporanea
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        # Creiamo il file e lo impostiamo in modalità di sola lettura per simulare un `PermissionError`
        output_file_path.touch()
        output_file_path.chmod(0o444)  # Imposta il file in modalità sola lettura

        # Esegui la funzione initialize e verifica che sollevi un `PermissionError`
        with pytest.raises(PermissionError):
            initialize("csv_mining_final.csv", "mining_results_sm_final.csv",
                       output_file_path.open("w"))

        # Ripristina i permessi del file dopo il test per evitare problemi
        output_file_path.chmod(0o666)

    def test_case_6(self, fixture_only_sm, base_fixture):
        # Percorso del file di output nella directory temporanea
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        # Esegui la funzione initialize e verifica che sollevi un FileNotFoundError
        with pytest.raises(FileNotFoundError):
            with output_file_path.open("w") as output:
                initialize("csv_mining_final.csv", "mining_results_sm_final.csv", output)

    def test_case_7(self, fixture_only_tm, base_fixture):
        # Percorso del file di output nella directory temporanea
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        # Esegui la funzione initialize e verifica che sollevi un FileNotFoundError
        with pytest.raises(FileNotFoundError):
            with output_file_path.open("w") as output:
                initialize("csv_mining_final.csv", "mining_results_sm_final.csv", output)

    def test_case_8(self, fixture_empty_tm, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        # Esegui la funzione initialize usando i file temporanei
        with output_file_path.open("w") as output:
            initialize("csv_mining_final.csv", "mining_results_sm_final.csv", output)

        # Leggi il contenuto dell'output per verificare
        written_data = output_file_path.read_text()

        expected_output = ""

        assert written_data.strip() == expected_output.strip()

    def test_case_9(self, fixture_header_tm, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        # Esegui la funzione initialize usando i file temporanei
        with output_file_path.open("w") as output:
            initialize("csv_mining_final.csv", "mining_results_sm_final.csv", output)

        # Leggi il contenuto dell'output per verificare
        written_data = output_file_path.read_text()

        expected_output = "NameClass,a1,a2,a3,a4,a5,a6,a7,a8,a9,m1,m2,m3,m4,m5,m6,m7,m8,class\n"

        assert written_data.strip() == expected_output.strip()

    def test_case_10(self, fixture_empty_sm, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        # Esegui la funzione initialize usando i file temporanei
        with output_file_path.open("w") as output:
            initialize("csv_mining_final.csv", "mining_results_sm_final.csv", output)

        # Leggi il contenuto dell'output per verificare
        written_data = output_file_path.read_text()

        expected_output = "NameClass,a1,a2,a3,a4,a5,a6,a7,a8,a9,class\n"

        assert written_data.strip() == expected_output.strip()

    def test_case_11(self, fixture_header_sm, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        with output_file_path.open("w") as output:
            initialize("csv_mining_final.csv", "mining_results_sm_final.csv", output)

        # Leggi il contenuto dell'output per verificare
        written_data = output_file_path.read_text()

        expected_output = "NameClass,a1,a2,a3,a4,a5,a6,a7,a8,a9,m1,m2,m3,m4,m5,m6,m7,m8,class\n"

        assert written_data.strip() == expected_output.strip()

    def test_case_12(self, fixture_both_csv, base_fixture):
        _, _, output_dir_path = base_fixture
        output_file_path = output_dir_path / "output.csv"

        # Esegui la funzione initialize usando i file temporanei
        with output_file_path.open("w") as output:
            initialize("csv_mining_final.csv", "mining_results_sm_final.csv", output)

        # Leggi il contenuto dell'output per verificare
        written_data = output_file_path.read_text()

        expected_output = (
            "NameClass,a1,a2,a3,a4,a5,a6,a7,a8,a9,m1,m2,m3,m4,m5,m6,m7,m8,class\n"
            "tony.java,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,10,11,pos,pos\n"
        )

        assert written_data.strip() == expected_output.strip()
