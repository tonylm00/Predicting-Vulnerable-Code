import ast
import csv
import os
import pytest
from Dataset2.Main import Main

def read_dict_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        dictionary = ast.literal_eval(content)
    return dictionary


def check_csv(index, file_path, target_columns, expected_row_count):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        # Converti il CSV in una lista di dizionari
        rows = list(reader)

        # Controllo del numero di righe
        assert len(
            rows) == expected_row_count, f"Errore: il file deve avere esattamente {expected_row_count} righe, ma ne ha {len(rows)}."
        # non posso controllare il numero di righe del csv perchè la duplicazione del _text_minining.txt ad ogni esecuzione aggiunge righe al csv e non posso prevedere quante righe ci saranno

        selected_row = rows[index]
        # Controllo delle colonne della prima riga
        for column in selected_row:
            print(column.strip())
            print(target_columns)
            if column in target_columns:
                assert selected_row[column] == '1', f"Errore: la colonna '{column}' dovrebbe avere valore 1."
            elif column == 'Name':
                assert selected_row[
                               column] == f'commit{index + 1}\\file{index + 1}.java', f"Errore: la colonna '{column}' dovrebbe avere valore 'commit/file{index + 1}.java_'."  # viene lasciato il carattere _ dopo il nome del file
            else:
                assert selected_row[column] == '0', f"Errore: la colonna '{column}' dovrebbe avere valore 0."

class TestTextMiningIntegration:
    BASE_DIR = os.getcwd()
    @pytest.fixture(autouse=True)
    def setup(self, setup_environment):
        self.main = Main(self.BASE_DIR)

    # Testiamo nel caso la directory mining_results non esista
    @pytest.mark.parametrize('setup_environment', [
        {'levels': 0, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_1(self, setup_environment):
        with pytest.raises(FileNotFoundError, match=r".*mining_results"):
            self.main.run_text_mining()

    # Testiamo nel caso RepositoryMining1 non esista
    @pytest.mark.parametrize('setup_environment', [
        {'levels': 1, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_2(self, setup_environment):
        self.main.run_text_mining()
        file_path = os.path.join(self.BASE_DIR, "mining_results", "text_mining_dict.txt")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

        file_path_filt = os.path.join(self.BASE_DIR, "mining_results", "FilteredTextMining.txt")
        with open(file_path_filt, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

        file_path_csv = os.path.join(self.BASE_DIR, "mining_results", "csv_mining_final.csv")
        expected_content = [
            ['Name']
        ]
        with open(file_path_csv, newline='') as csvfile:
            reader = csv.reader(csvfile)
            actual_content = list(reader)
        assert actual_content == expected_content, "Il contenuto del file CSV non corrisponde a quello atteso"

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 2, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_3(self, setup_environment):
        self.main.run_text_mining()
        for i in range(1, 36, 1):
            repo_name = f"RepositoryMining{i}"
            repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name)
            assert os.listdir(repo_dir) == []

        file_path = os.path.join(self.BASE_DIR, "mining_results", "text_mining_dict.txt")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

        file_path_filt = os.path.join(self.BASE_DIR, "mining_results", "FilteredTextMining.txt")
        with open(file_path_filt, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

        file_path_csv = os.path.join(self.BASE_DIR, "mining_results", "csv_mining_final.csv")
        expected_content = [
            ['Name']
        ]
        with open(file_path_csv, newline='') as csvfile:
            reader = csv.reader(csvfile)
            actual_content = list(reader)
        assert actual_content == expected_content, "Il contenuto del file CSV non corrisponde a quello atteso"


    @pytest.mark.parametrize('setup_environment', [
        {'levels': 2, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_4(self, setup_environment, create_temp_file):
        create_temp_file(self.BASE_DIR + "/mining_results/" + "RepositoryMining1/" + f"file1.java",
                         f"ciao stiamo facendo una prova")

        self.main.run_text_mining()
        file_path = os.path.join(self.BASE_DIR, "mining_results", "text_mining_dict.txt")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

        file_path_filt = os.path.join(self.BASE_DIR, "mining_results", "FilteredTextMining.txt")
        with open(file_path_filt, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

        file_path_csv = os.path.join(self.BASE_DIR, "mining_results", "csv_mining_final.csv")
        expected_content = [
            ['Name']
        ]
        with open(file_path_csv, newline='') as csvfile:
            reader = csv.reader(csvfile)
            actual_content = list(reader)
        assert actual_content == expected_content, "Il contenuto del file CSV non corrisponde a quello atteso"

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 2, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_5(self, setup_environment, create_temp_file):
        for i in range(1, 36, 1):
            create_temp_file(self.BASE_DIR + "/mining_results/" + f"RepositoryMining{i}/" + f"CHECK.txt", "")

        self.main.run_text_mining()
        for i in range(1, 36, 1):
            repo_name = f"RepositoryMining{i}"
            repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name)
            assert os.listdir(repo_dir) == ["CHECK.txt"]

        file_path = os.path.join(self.BASE_DIR, "mining_results", "text_mining_dict.txt")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

        file_path_filt = os.path.join(self.BASE_DIR, "mining_results", "FilteredTextMining.txt")
        with open(file_path_filt, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

        file_path_csv = os.path.join(self.BASE_DIR, "mining_results", "csv_mining_final.csv")
        expected_content = [
            ['Name']
        ]
        with open(file_path_csv, newline='') as csvfile:
            reader = csv.reader(csvfile)
            actual_content = list(reader)
        assert actual_content == expected_content, "Il contenuto del file CSV non corrisponde a quello atteso"


    @pytest.mark.parametrize('setup_environment', [
        {'levels': 3, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_6(self, setup_environment):
        self.main.run_text_mining()
        for i in range(1, 36, 1):
            repo_name = f"RepositoryMining{i}"
            repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name)
            assert os.listdir(repo_dir + "/" + str(i)) == []

        file_path = os.path.join(self.BASE_DIR, "mining_results", "text_mining_dict.txt")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

        file_path_filt = os.path.join(self.BASE_DIR, "mining_results", "FilteredTextMining.txt")
        with open(file_path_filt, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

        file_path_csv = os.path.join(self.BASE_DIR, "mining_results", "csv_mining_final.csv")
        expected_content = [
            ['Name']
        ]
        with open(file_path_csv, newline='') as csvfile:
            reader = csv.reader(csvfile)
            actual_content = list(reader)
        assert actual_content == expected_content, "Il contenuto del file CSV non corrisponde a quello atteso"


    @pytest.mark.parametrize('setup_environment', [
        {'levels': 3, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_7(self, setup_environment, create_temp_file):
        create_temp_file(self.BASE_DIR + "/mining_results/" + "RepositoryMining1/1/" + f"file1.java",
                         f"ciao stiamo facendo una prova")

        self.main.run_text_mining()
        file_path = os.path.join(self.BASE_DIR, "mining_results", "text_mining_dict.txt")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

        file_path_filt = os.path.join(self.BASE_DIR, "mining_results", "FilteredTextMining.txt")
        with open(file_path_filt, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

        file_path_csv = os.path.join(self.BASE_DIR, "mining_results", "csv_mining_final.csv")
        expected_content = [
            ['Name']
        ]
        with open(file_path_csv, newline='') as csvfile:
            reader = csv.reader(csvfile)
            actual_content = list(reader)
        assert actual_content == expected_content, "Il contenuto del file CSV non corrisponde a quello atteso"

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 3, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_8(self, setup_environment, create_temp_file):
        for i in range(1, 36, 1):
            create_temp_file(self.BASE_DIR + "/mining_results/" + f"RepositoryMining{i}/" + str(i) + f"/.DS_Store", "")

        self.main.run_text_mining()
        for i in range(1, 36, 1):
            repo_name = f"RepositoryMining{i}"
            repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i))
            assert os.listdir(repo_dir) == [".DS_Store"]

        file_path = os.path.join(self.BASE_DIR, "mining_results", "text_mining_dict.txt")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

        file_path_filt = os.path.join(self.BASE_DIR, "mining_results", "FilteredTextMining.txt")
        with open(file_path_filt, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

        file_path_csv = os.path.join(self.BASE_DIR, "mining_results", "csv_mining_final.csv")
        expected_content = [
            ['Name']
        ]
        with open(file_path_csv, newline='') as csvfile:
            reader = csv.reader(csvfile)
            actual_content = list(reader)
        assert actual_content == expected_content, "Il contenuto del file CSV non corrisponde a quello atteso"


    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_9(self, setup_environment):
        self.main.run_text_mining()
        for i in range(1, 36, 1):
            repo_name = f"RepositoryMining{i}"
            repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name)
            assert os.listdir(repo_dir + "/" + str(i) + "/" + f"commit{i}") == []

        file_path = os.path.join(self.BASE_DIR, "mining_results", "text_mining_dict.txt")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

        file_path_filt = os.path.join(self.BASE_DIR, "mining_results", "FilteredTextMining.txt")
        with open(file_path_filt, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

        file_path_csv = os.path.join(self.BASE_DIR, "mining_results", "csv_mining_final.csv")
        expected_content = [
            ['Name']
        ]
        with open(file_path_csv, newline='') as csvfile:
            reader = csv.reader(csvfile)
            actual_content = list(reader)
        assert actual_content == expected_content, "Il contenuto del file CSV non corrisponde a quello atteso"


    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_10(self, setup_environment, create_temp_file):
        for i in range(1, 36, 1):
            create_temp_file(self.BASE_DIR + "/mining_results/" + f"RepositoryMining{i}/" + str(
                    i) + f"/commit{i}/" + f".DS_Store", "")

        self.main.run_text_mining()
        for i in range(1, 36, 1):
            repo_name = f"RepositoryMining{i}"
            repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i), f"commit{i}")
            assert os.listdir(repo_dir) == [".DS_Store"]

        file_path = os.path.join(self.BASE_DIR, "mining_results", "text_mining_dict.txt")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

        file_path_filt = os.path.join(self.BASE_DIR, "mining_results", "FilteredTextMining.txt")
        with open(file_path_filt, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

        file_path_csv = os.path.join(self.BASE_DIR, "mining_results", "csv_mining_final.csv")
        expected_content = [
            ['Name']
        ]
        with open(file_path_csv, newline='') as csvfile:
            reader = csv.reader(csvfile)
            actual_content = list(reader)
        assert actual_content == expected_content, "Il contenuto del file CSV non corrisponde a quello atteso"

    # RepositoryMining1 non viene considerata nel for del text_mining
    @pytest.mark.parametrize('setup_environment', [
        {'levels': 5, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_11(self, setup_environment):
        self.main.run_text_mining()
        file_path = os.path.join(self.BASE_DIR, "mining_results", "text_mining_dict.txt")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

        file_path_filt = os.path.join(self.BASE_DIR, "mining_results", "FilteredTextMining.txt")
        with open(file_path_filt, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

        file_path_csv = os.path.join(self.BASE_DIR, "mining_results", "csv_mining_final.csv")
        expected_content = [
            ['Name']
        ]
        with open(file_path_csv, newline='') as csvfile:
            reader = csv.reader(csvfile)
            actual_content = list(reader)
        assert actual_content == expected_content, "Il contenuto del file CSV non corrisponde a quello atteso"

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {'file.java': ''}}
    ], indirect=True)
    def test_case_12(self, setup_environment, create_temp_file):

        self.main.run_text_mining()

        file_path_dict = os.path.join(self.BASE_DIR, "mining_results", "text_mining_dict.txt")
        file_path_filt = os.path.join(self.BASE_DIR, "mining_results", "FilteredTextMining.txt")
        file_path_csv = os.path.join(self.BASE_DIR, "mining_results", "csv_mining_final.csv")

        repo_dir = os.path.join(self.BASE_DIR, "mining_results", "RepositoryMining1/1/", "commit1")
        assert os.listdir(repo_dir) == ["file.java", "file.java_text_mining.txt"]

        file_path = os.path.join(repo_dir, "file.java_text_mining.txt")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

        content = read_dict_from_file(file_path_dict)
        assert content == {}

        content = read_dict_from_file(file_path_filt)
        assert content == {}

        expected_content = [['Name'],
                 ['commit1\\file.java'],
                 ['commit2\\file.java'],
                 ['commit3\\file.java'],
                 ['commit4\\file.java'],
                 ['commit5\\file.java'],
                 ['commit6\\file.java'],
                 ['commit7\\file.java'],
                 ['commit8\\file.java'],
                 ['commit9\\file.java'],
                 ['commit10\\file.java'],
                 ['commit11\\file.java'],
                 ['commit12\\file.java'],
                 ['commit13\\file.java'],
                 ['commit14\\file.java'],
                 ['commit15\\file.java'],
                 ['commit16\\file.java'],
                 ['commit17\\file.java'],
                 ['commit18\\file.java'],
                 ['commit19\\file.java'],
                 ['commit20\\file.java'],
                 ['commit21\\file.java'],
                 ['commit22\\file.java'],
                 ['commit23\\file.java'],
                 ['commit24\\file.java'],
                 ['commit25\\file.java'],
                 ['commit26\\file.java'],
                 ['commit27\\file.java'],
                 ['commit28\\file.java'],
                 ['commit29\\file.java'],
                 ['commit30\\file.java'],
                 ['commit31\\file.java'],
                 ['commit32\\file.java'],
                 ['commit33\\file.java'],
                 ['commit34\\file.java'],
                 ['commit35\\file.java']]
        with open(file_path_csv, newline='') as csvfile:
            reader = csv.reader(csvfile)
            actual_content = list(reader)
        assert actual_content == expected_content, "Il contenuto del file CSV non corrisponde a quello atteso"

    # Se già presente text_mining, lo sovrascivere ma crea un nuovo file con il nome file.java_text_mining.txt_text_mining.txt vuoto
    # ottimizzare con controllo che text_mining non deve essere presente nel nome o che il file deve avere estensione .java
    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {'file.java': ''}}
    ], indirect=True)
    def test_case_13(self, setup_environment, create_temp_file):
        for i in range(1, 36, 1):
            repo_name = f"RepositoryMining{i}"
            repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i), f"commit{i}")
            create_temp_file(repo_dir + "/file.java_text_mining.txt", "")

        self.main.run_text_mining()

        repo_dir = os.path.join(self.BASE_DIR, "mining_results", "RepositoryMining1/1/", "commit1")
        assert os.listdir(repo_dir) == ["file.java", "file.java_text_mining.txt"]
        file_path = os.path.join(repo_dir, "file.java_text_mining.txt")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {'file.java': ''}}
    ], indirect=True)
    def test_case_14(self, setup_environment, create_temp_file):
        for i in range(1, 36, 1):
            repo_name = f"RepositoryMining{i}"
            repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i), f"commit{i}")
            create_temp_file(repo_dir + "/file.java_text_mining.txt", "{'import: 1, 'static':3, 'int': 2}")

        self.main.run_text_mining()

        repo_dir = os.path.join(self.BASE_DIR, "mining_results", "RepositoryMining1/1/", "commit1")
        assert os.listdir(repo_dir) == ["file.java", "file.java_text_mining.txt"]
        file_path = os.path.join(repo_dir, "file.java_text_mining.txt")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {}}
    ], indirect=True)
    def test_case_15(self, setup_environment, create_temp_file):
        for i in range(1, 36, 1):
            repo_name = f"RepositoryMining{i}"
            repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i), f"commit{i}")
            if i % 2 == 0:
                create_temp_file(repo_dir + "/" + f"file{i}.java", f"ciao stiamo facendo una prova")
            else:
                create_temp_file(repo_dir + "/" + f"file{i}.java", f"CIAO stiamo Facendo test sui file dispari")

        self.main.run_text_mining()

        file_path_csv = os.path.join(self.BASE_DIR, "mining_results", "csv_mining_final.csv")
        for i in range(1, 36, 1):
            if i % 2 == 0:
                check_csv(i - 1, file_path_csv, [' ciao', ' stiamo', ' facendo', ' una', ' prova'],
                          35)  # 34 perchè il 18 non ci sta
            else:
                check_csv(i - 1, file_path_csv,
                          [' ciao', ' stiamo', ' facendo', ' test', ' sui', ' file', ' dispari'],
                          35)  # le colonne sono tutte salvate con lo spazio alla fine

            repo_name = f"RepositoryMining{i}"
            repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i), f"commit{i}")
            assert os.listdir(repo_dir) == [f"file{i}.java", f"file{i}.java_text_mining.txt"]

            file_path = os.path.join(repo_dir, f"file{i}.java_text_mining.txt")
            content = read_dict_from_file(file_path)
            if i % 2 == 0:
                assert content == {'ciao': 1, 'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1}
            else:
                assert content == {'CIAO': 1, 'stiamo': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1,
                                   'dispari': 1}

        file_path_dict = os.path.join(self.BASE_DIR, "mining_results", "text_mining_dict.txt")
        content = read_dict_from_file(file_path_dict)
        assert content == {'CIAO': 18, 'Facendo': 18, 'test': 18, 'sui': 18, 'file': 18, 'dispari': 18, 'ciao': 17,
                           'stiamo': 35, 'facendo': 17, 'una': 17, 'prova': 17}

        file_path_filt = os.path.join(self.BASE_DIR, "mining_results", "FilteredTextMining.txt")
        content = read_dict_from_file(file_path_filt)
        assert content == {'ciao': 35, 'facendo': 35, 'test': 18, 'sui': 18, 'file': 18, 'dispari': 18, 'stiamo': 35, 'una': 17,
                           'prova': 17}

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {}}
    ], indirect=True)
    def test_case_16(self, setup_environment, create_temp_file):
        file_path_dict = os.path.join(self.BASE_DIR, "mining_results", "text_mining_dict.txt")
        file_path_filt = os.path.join(self.BASE_DIR, "mining_results", "FilteredTextMining.txt")
        file_path_csv = os.path.join(self.BASE_DIR, "mining_results", "csv_mining_final.csv")

        create_temp_file(file_path_dict, "prova completamente diversa per testare come vengono sovrascitti i file")
        create_temp_file(file_path_filt, "prova completamente diversa per testare come vengono sovrascitti i file")
        create_temp_file(file_path_csv, "Name, CIAO, diversa, file\n")

        for i in range(1, 36, 1):
            repo_name = f"RepositoryMining{i}"
            repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i), f"commit{i}")
            if i % 2 == 0:
                create_temp_file(repo_dir + "/" + f"file{i}.java", f"ciao stiamo facendo una prova")
            else:
                create_temp_file(repo_dir + "/" + f"file{i}.java", f"CIAO stiamo Facendo test sui file dispari")

        self.main.run_text_mining()

        file_path_csv = os.path.join(self.BASE_DIR, "mining_results", "csv_mining_final.csv")
        for i in range(1, 36, 1):
            if i % 2 == 0:
                check_csv(i - 1, file_path_csv, [' ciao', ' stiamo', ' facendo', ' una', ' prova'],
                          35)  # 34 perchè il 18 non ci sta
            else:
                check_csv(i - 1, file_path_csv,
                          [' ciao', ' stiamo', ' facendo', ' test', ' sui', ' file', ' dispari'],
                          35)  # le colonne sono tutte salvate con lo spazio alla fine

            repo_name = f"RepositoryMining{i}"
            repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i), f"commit{i}")
            assert os.listdir(repo_dir) == [f"file{i}.java", f"file{i}.java_text_mining.txt"]

            file_path = os.path.join(repo_dir, f"file{i}.java_text_mining.txt")
            content = read_dict_from_file(file_path)
            if i % 2 == 0:
                assert content == {'ciao': 1, 'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1}
            else:
                assert content == {'CIAO': 1, 'stiamo': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1,
                                   'dispari': 1}

        file_path_dict = os.path.join(self.BASE_DIR, "mining_results", "text_mining_dict.txt")
        content = read_dict_from_file(file_path_dict)
        assert content == {'CIAO': 18, 'Facendo': 18, 'test': 18, 'sui': 18, 'file': 18, 'dispari': 18, 'ciao': 17,
                           'stiamo': 35, 'facendo': 17, 'una': 17, 'prova': 17}

        file_path_filt = os.path.join(self.BASE_DIR, "mining_results", "FilteredTextMining.txt")
        content = read_dict_from_file(file_path_filt)
        assert content == {'ciao': 35, 'facendo': 35, 'test': 18, 'sui': 18, 'file': 18, 'dispari': 18, 'stiamo': 35,
                           'una': 17,
                           'prova': 17}

    #non ci sono più text_mining creati in loop
    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {}}
    ], indirect=True)
    def test_case_17(self, setup_environment, create_temp_file):
        for i in range(1, 36, 1):
            repo_name = f"RepositoryMining{i}"
            repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i), f"commit{i}")
            if i % 2 == 0:
                create_temp_file(repo_dir + "/" + f"file{i}.java", "ciao stiamo facendo una prova")
                create_temp_file(repo_dir + "/" + f"file{i}.java_text_mining.txt", "")
            else:
                create_temp_file(repo_dir + "/" + f"file{i}.java", f"CIAO stiamo Facendo test sui file dispari")
                create_temp_file(repo_dir + "/" + f"file{i}.java_text_mining.txt", "")

        self.main.run_text_mining()

        file_path_dict = os.path.join(self.BASE_DIR, "mining_results", "text_mining_dict.txt")
        content = read_dict_from_file(file_path_dict)
        assert content == {'CIAO': 18, 'Facendo': 18, 'test': 18, 'sui': 18, 'file': 18, 'dispari': 18, 'ciao': 17,
                           'stiamo': 35, 'facendo': 17, 'una': 17, 'prova': 17}

        file_path_filt = os.path.join(self.BASE_DIR, "mining_results", "FilteredTextMining.txt")
        content = read_dict_from_file(file_path_filt)
        assert content == {'ciao': 35, 'facendo': 35, 'test': 18, 'sui': 18, 'file': 18, 'dispari': 18, 'stiamo': 35,
                           'una': 17, 'prova': 17}

        file_path_csv = os.path.join(self.BASE_DIR, "mining_results", "csv_mining_final.csv")
        for i in range(1, 36, 1):
            repo_name = f"RepositoryMining{i}"
            repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i), f"commit{i}")
            assert os.listdir(repo_dir) == [f"file{i}.java", f"file{i}.java_text_mining.txt"]

            file_path = os.path.join(repo_dir, f"file{i}.java_text_mining.txt")
            content = read_dict_from_file(file_path)
            if i % 2 == 0:
                assert content == {'ciao': 1, 'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1}
            else:
                assert content == {'CIAO': 1, 'stiamo': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1,
                                   'dispari': 1}

            if i % 2 == 0:
                check_csv(i - 1, file_path_csv, [' ciao', ' stiamo', ' facendo', ' una', ' prova'],
                          35)  # 34 perchè il 18 non ci sta
            else:
                check_csv(i - 1, file_path_csv,
                          [' ciao', ' stiamo', ' facendo', ' test', ' sui', ' file', ' dispari'],
                          35)  # le colonne sono tutte salvate con lo spazio alla fine

    #non ci sono più text_mining creati in loop
    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {}}
    ], indirect=True)
    def test_case_18(self, setup_environment, create_temp_file):
        for i in range(1, 36, 1):
            repo_name = f"RepositoryMining{i}"
            repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i), f"commit{i}")
            if i % 2 == 0:
                create_temp_file(repo_dir + "/" + f"file{i}.java", "ciao stiamo facendo una prova")
                create_temp_file(repo_dir + "/" + f"file{i}.java_text_mining.txt",
                                 "{'ciao': 1, 'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1}")
            else:
                create_temp_file(repo_dir + "/" + f"file{i}.java", f"CIAO stiamo Facendo test sui file dispari")
                create_temp_file(repo_dir + "/" + f"file{i}.java_text_mining.txt",
                                 "{'CIAO': 1, 'stiamo': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1}")

        self.main.run_text_mining()

        file_path_dict = os.path.join(self.BASE_DIR, "mining_results", "text_mining_dict.txt")
        content = read_dict_from_file(file_path_dict)
        assert content == {'CIAO': 18, 'Facendo': 18, 'test': 18, 'sui': 18, 'file': 18, 'dispari': 18, 'ciao': 17,
                           'stiamo': 35, 'facendo': 17, 'una': 17, 'prova': 17}

        file_path_filt = os.path.join(self.BASE_DIR, "mining_results", "FilteredTextMining.txt")
        content = read_dict_from_file(file_path_filt)
        assert content == {'ciao': 35, 'facendo': 35, 'test': 18, 'sui': 18, 'file': 18, 'dispari': 18, 'stiamo': 35,
                           'una': 17, 'prova': 17}

        file_path_csv = os.path.join(self.BASE_DIR, "mining_results", "csv_mining_final.csv")
        for i in range(1, 36, 1):
            repo_name = f"RepositoryMining{i}"
            repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i), f"commit{i}")
            assert os.listdir(repo_dir) == [f"file{i}.java", f"file{i}.java_text_mining.txt"]

            file_path = os.path.join(repo_dir, f"file{i}.java_text_mining.txt")
            content = read_dict_from_file(file_path)
            if i % 2 == 0:
                assert content == {'ciao': 1, 'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1}
            else:
                assert content == {'CIAO': 1, 'stiamo': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1,
                                   'dispari': 1}

            if i % 2 == 0:
                check_csv(i - 1, file_path_csv, [' ciao', ' stiamo', ' facendo', ' una', ' prova'],
                          35)  # 34 perchè il 18 non ci sta
            else:
                check_csv(i - 1, file_path_csv,
                          [' ciao', ' stiamo', ' facendo', ' test', ' sui', ' file', ' dispari'],
                          35)  # le colonne sono tutte salvate con lo spazio alla fine

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {'file.txt': ''}}
    ], indirect=True)
    def test_case_19(self, setup_environment):
        self.main.run_text_mining()

        repo_dir = os.path.join(self.BASE_DIR, "mining_results", "RepositoryMining1/1/", "commit1")
        assert os.listdir(repo_dir) == ["file.txt"]
        #non viene più considerato perchè non termina con .java