import ast
import os
import csv
import pytest
from Dataset2.Text_Mining.text_mining import main as text_mining_main
from Dataset2.Text_Mining.dict_generator import main as dict_gen_main
from Dataset2.Text_Mining.less_element_text_mining import main as less_element_main
from Dataset2.Text_Mining.creator_csv_for_TextMining import main as creator_csv_main


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
        assert len(rows) == expected_row_count, f"Errore: il file deve avere esattamente {expected_row_count} righe, ma ne ha {len(rows)}."
        # non posso controllare il numero di righe del csv perchè la duplicazione del _text_minining.txt ad ogni esecuzione aggiunge righe al csv e non posso prevedere quante righe ci saranno


        selected_row = rows[index]
        print(index)
        # Controllo delle colonne della prima riga
        for column in selected_row:
            print(selected_row[column])
            if column in target_columns:
                assert selected_row[column] == '1', f"Errore: la colonna '{column}' dovrebbe avere valore 1."
            elif column == 'NameClass ':
                if index <= 16:
                    assert selected_row[column] == f'commit{index+1}/file{index+1}.java_', f"Errore: la colonna '{column}' dovrebbe avere valore 'commit/file{index+1}.java_'."  # viene lasciato il carattere _ dopo il nome del file
                else:
                    assert selected_row[column] == f'commit{index+2}/file{index+2}.java_', f"Errore: la colonna '{column}' dovrebbe avere valore 'commit/file{index+2}.java_'."  # viene lasciato il carattere _ dopo il nome del file
            elif column == 'class':
                if index <= 16:
                    assert selected_row[column] == ' pos', f"Errore: la colonna '{column}' dovrebbe avere valore 'pos"
                else:
                    assert selected_row[column] == ' neg', f"Errore: la colonna '{column}' dovrebbe avere valore 'neg"
            else:
                assert selected_row[column] == '0', f"Errore: la colonna '{column}' dovrebbe avere valore 0."


class TestTextMiningIntegration:
    BASE_DIR = os.getcwd()

    #Testiamo nel caso la directory mining_results non esista
    def test_case_1(self):
        with pytest.raises(FileNotFoundError, match=r".*mining_results"):
            text_mining_main()
            dict_gen_main()
            less_element_main()
            creator_csv_main()

    #Testiamo nel caso RepositoryMining1 non esista
    @pytest.mark.parametrize('setup_environment', [
        {'levels': 1, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_2(self, setup_environment):
        with pytest.raises(FileNotFoundError, match=r".*RepositoryMining1"):
            text_mining_main()
            dict_gen_main()
            less_element_main()
            creator_csv_main()

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 2, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_3(self, setup_environment):
        text_mining_main()
        dict_gen_main()
        less_element_main()
        creator_csv_main()
        for i in range(1, 36, 1):
            if i == 18:
                continue  # Salta RepositoryMining18

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
            ['NameClass ', 'class'],
            []
        ]
        with open(file_path_csv, newline='') as csvfile:
            reader = csv.reader(csvfile)
            actual_content = list(reader)
        assert actual_content == expected_content, "Il contenuto del file CSV non corrisponde a quello atteso"

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 2, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_4(self, setup_environment, create_temp_file):
        create_temp_file(self.BASE_DIR + "/mining_results/" +"RepositoryMining1/" + f"file1.java", f"ciao stiamo facendo una prova")

        with pytest.raises(NotADirectoryError, match=r'.*file1.java'):
            text_mining_main()
            dict_gen_main()
            less_element_main()
            creator_csv_main()

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 2, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_5(self, setup_environment, create_temp_file):
        for i in range(1, 36, 1):
            if i != 18:
                create_temp_file(self.BASE_DIR + "/mining_results/" + f"RepositoryMining{i}/" + f".DS_Store", "")

        text_mining_main()
        dict_gen_main()
        less_element_main()
        creator_csv_main()
        for i in range(1, 36, 1):
            if i == 18:
                continue  # Salta RepositoryMining18

            repo_name = f"RepositoryMining{i}"
            repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name)
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
            ['NameClass ', 'class'],
            []
        ]
        with open(file_path_csv, newline='') as csvfile:
            reader = csv.reader(csvfile)
            actual_content = list(reader)
        assert actual_content == expected_content, "Il contenuto del file CSV non corrisponde a quello atteso"

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 3, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_6(self, setup_environment):
        text_mining_main()
        dict_gen_main()
        less_element_main()
        creator_csv_main()
        for i in range(1, 36, 1):
            if i == 18:
                continue  # Salta RepositoryMining18

            repo_name = f"RepositoryMining{i}"
            repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name)
            assert os.listdir(repo_dir+"/"+str(i)) == []

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
            ['NameClass ', 'class'],
            []
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

        with pytest.raises(NotADirectoryError, match=r".*file1.java"):
            text_mining_main()
            dict_gen_main()
            less_element_main()
            creator_csv_main()

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 3, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_8(self, setup_environment, create_temp_file):
        for i in range(1, 36, 1):
            if i != 18:
                create_temp_file(self.BASE_DIR + "/mining_results/" + f"RepositoryMining{i}/" + str(i) + f"CHECK.txt", "")

        text_mining_main()
        dict_gen_main()
        less_element_main()
        creator_csv_main()
        for i in range(1, 36, 1):
            if i == 18:
                continue  # Salta RepositoryMining18

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
            ['NameClass ', 'class'],
            []
        ]
        with open(file_path_csv, newline='') as csvfile:
            reader = csv.reader(csvfile)
            actual_content = list(reader)
        assert actual_content == expected_content, "Il contenuto del file CSV non corrisponde a quello atteso"

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_9(self, setup_environment):
        text_mining_main()
        dict_gen_main()
        less_element_main()
        creator_csv_main()
        for i in range(1, 36, 1):
            if i == 18:
                continue  # Salta RepositoryMining18

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
            ['NameClass ', 'class'],
            []
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
            if i != 18:
                create_temp_file(self.BASE_DIR + "/mining_results/" + f"RepositoryMining{i}/" + str(i) + f"commit{i}/" + f".DS_Store", "")

        text_mining_main()
        dict_gen_main()
        less_element_main()
        creator_csv_main()
        for i in range(1, 36, 1):
            if i == 18:
                continue  # Salta RepositoryMining18

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
            ['NameClass ', 'class'],
            []
        ]
        with open(file_path_csv, newline='') as csvfile:
            reader = csv.reader(csvfile)
            actual_content = list(reader)
        assert actual_content == expected_content, "Il contenuto del file CSV non corrisponde a quello atteso"

    #RepositoryMining1 non viene considerata nel for del text_mining
    @pytest.mark.parametrize('setup_environment', [
        {'levels': 5, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_11(self, setup_environment):
        with pytest.raises(PermissionError, match=r".*Permission denied: 'directory'"):
            text_mining_main()
            dict_gen_main()
            less_element_main()
            creator_csv_main()

    #modificare la codifica nella lettura e scrittura dei file in utf-8 per tutti gli script (creava sempre un errore di UnicodeDecodeError non previsto)
    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {'file.java': ''}}
    ], indirect=True)
    def test_case_12(self, setup_environment):
        text_mining_main()
        dict_gen_main()
        less_element_main()
        creator_csv_main()

        repo_dir = os.path.join(self.BASE_DIR, "mining_results", "RepositoryMining1/1/", "commit1")
        assert os.listdir(repo_dir) == ["file.java", "file.java_text_mining.txt"]

        file_path = os.path.join(repo_dir, "file.java_text_mining.txt")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {'file.java': ''}}
    ], indirect=True)
    def test_case_13(self, setup_environment, create_temp_file):
        file_path_dict = os.path.join(self.BASE_DIR, "mining_results", "text_mining_dict.txt")
        file_path_filt = os.path.join(self.BASE_DIR, "mining_results", "FilteredTextMining.txt")
        file_path_csv = os.path.join(self.BASE_DIR, "mining_results", "csv_mining_final.csv")

        create_temp_file(file_path_dict, "{'CIAO': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1, 'ciao': 1, 'stiamo': 1, 'facendo': 1, 'una': 1}")
        create_temp_file(file_path_filt, "{'CIAO': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1, 'ciao': 1, 'stiamo': 1, 'facendo': 1, 'una': 1}")
        create_temp_file(file_path_csv, "NameClass ,CIAO ,Facendo ,test , class\n")

        text_mining_main()
        dict_gen_main()
        less_element_main()
        creator_csv_main()

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



    #Se già presente text_mining, lo sovrascivere ma crea un nuovo file con il nome file.java_text_mining.txt_text_mining.txt vuoto
    #ottimizzare con controllo che text_mining non deve essere presente nel nome o che il file deve avere estensione .java
    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {'file.java': ''}}
    ], indirect=True)
    def test_case_14(self, setup_environment, create_temp_file):
        for i in range(1, 36, 1):
            if i != 18:
                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i), f"commit{i}")
                create_temp_file(repo_dir + "/file.java_text_mining.txt", "")

        text_mining_main()
        dict_gen_main()
        less_element_main()
        creator_csv_main()

        repo_dir = os.path.join(self.BASE_DIR, "mining_results", "RepositoryMining1/1/", "commit1")
        assert os.listdir(repo_dir) == ["file.java", "file.java_text_mining.txt",
                                         "file.java_text_mining.txt_text_mining.txt"]
        file_path = os.path.join(repo_dir, "file.java_text_mining.txt")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {'file.java': ''}}
    ], indirect=True)
    def test_case_15(self, setup_environment, create_temp_file):
        for i in range(1, 36, 1):
            if i != 18:
                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i), f"commit{i}")
                create_temp_file(repo_dir + "/file.java_text_mining.txt", "{'import: 1, 'static':3, 'int': 2}")

        text_mining_main()
        dict_gen_main()
        less_element_main()
        creator_csv_main()

        repo_dir = os.path.join(self.BASE_DIR, "mining_results", "RepositoryMining1/1/", "commit1")
        assert os.listdir(repo_dir) == ["file.java", "file.java_text_mining.txt",
                                        "file.java_text_mining.txt_text_mining.txt"]
        file_path = os.path.join(repo_dir, "file.java_text_mining.txt")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"


    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {}}
    ], indirect=True)
    def test_case_16(self, setup_environment, create_temp_file):
        for i in range(1, 36, 1):
            if i != 18: # Salta RepositoryMining18
                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i), f"commit{i}")
                if i % 2 == 0:
                    create_temp_file(repo_dir + "/" + f"file{i}.java", f"ciao stiamo facendo una prova")
                else:
                    create_temp_file(repo_dir + "/" + f"file{i}.java", f"CIAO stiamo Facendo test sui file dispari")

        text_mining_main()
        dict_gen_main()
        less_element_main()
        creator_csv_main()

        file_path_csv = os.path.join(self.BASE_DIR, "mining_results", "csv_mining_final.csv")
        for i in range(1, 36, 1):
            print(i)
            if i < 17:
                if i % 2 == 0:
                    check_csv(i-1, file_path_csv, ['ciao ', 'stiamo ', 'facendo ', 'una ', 'prova '], 34) #34 perchè il 18 non ci sta
                else:
                    check_csv(i-1, file_path_csv, ['ciao ', 'stiamo ', 'facendo ', 'test ', 'sui ', 'file ', 'dispari '], 34)  # le colonne sono tutte salvate con lo spazio alla fine
            elif 17 < i < 34:
                if i % 2 == 0:
                    check_csv(i, file_path_csv, ['ciao ', 'stiamo ', 'facendo ', 'una ', 'prova '],
                              34)  # 34 perchè il 18 non ci sta
                else:
                    check_csv(i, file_path_csv,
                              ['ciao ', 'stiamo ', 'facendo ', 'test ', 'sui ', 'file ', 'dispari '],
                              34)  # le colonne sono tutte salvate con lo spazio alla fine

            if i != 18:
                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i), f"commit{i}")
                assert os.listdir(repo_dir) == [f"file{i}.java", f"file{i}.java_text_mining.txt"]

                file_path = os.path.join(repo_dir, f"file{i}.java_text_mining.txt")
                content = read_dict_from_file(file_path)
                if i % 2 == 0:
                    assert content == {'ciao': 1, 'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1}
                else:
                    assert content == {'CIAO': 1, 'stiamo': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1}


        file_path_dict = os.path.join(self.BASE_DIR, "mining_results", "text_mining_dict.txt")
        content = read_dict_from_file(file_path_dict)
        assert content == {'CIAO': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1, 'ciao': 1, 'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1}

        file_path_filt = os.path.join(self.BASE_DIR, "mining_results", "FilteredTextMining.txt")
        content = read_dict_from_file(file_path_filt)
        assert content == {'ciao': 2, 'facendo': 2, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1, 'stiamo': 1, 'una': 1, 'prova': 1}

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {}}
    ], indirect=True)
    def test_case_17(self, setup_environment, create_temp_file):
        file_path_dict = os.path.join(self.BASE_DIR, "mining_results", "text_mining_dict.txt")
        file_path_filt = os.path.join(self.BASE_DIR, "mining_results", "FilteredTextMining.txt")
        file_path_csv = os.path.join(self.BASE_DIR, "mining_results", "csv_mining_final.csv")

        create_temp_file(file_path_dict, "prova completamente diversa per testare come vengono sovrascitti i file")
        create_temp_file(file_path_filt, "prova completamente diversa per testare come vengono sovrascitti i file")
        create_temp_file(file_path_csv, "NameClass ,CIAO ,diversa ,file , class\n")

        for i in range(1, 36, 1):
            if i != 18:  # Salta RepositoryMining18
                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i), f"commit{i}")
                if i % 2 == 0:
                    create_temp_file(repo_dir + "/" + f"file{i}.java", f"ciao stiamo facendo una prova")
                else:
                    create_temp_file(repo_dir + "/" + f"file{i}.java", f"CIAO stiamo Facendo test sui file dispari")

        text_mining_main()
        dict_gen_main()
        less_element_main()
        creator_csv_main()

        for i in range(1, 36, 1):
            print(i)
            if i < 17:
                if i % 2 == 0:
                    check_csv(i - 1, file_path_csv, ['ciao ', 'stiamo ', 'facendo ', 'una ', 'prova '],
                              34)  # 34 perchè il 18 non ci sta
                else:
                    check_csv(i - 1, file_path_csv,
                              ['ciao ', 'stiamo ', 'facendo ', 'test ', 'sui ', 'file ', 'dispari '],
                              34)  # le colonne sono tutte salvate con lo spazio alla fine
            elif 17 < i < 34:
                if i % 2 == 0:
                    check_csv(i, file_path_csv, ['ciao ', 'stiamo ', 'facendo ', 'una ', 'prova '],
                              34)  # 34 perchè il 18 non ci sta
                else:
                    check_csv(i, file_path_csv,
                              ['ciao ', 'stiamo ', 'facendo ', 'test ', 'sui ', 'file ', 'dispari '],
                              34)  # le colonne sono tutte salvate con lo spazio alla fine

            if i != 18:
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

        content = read_dict_from_file(file_path_dict)
        assert content == {'CIAO': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1, 'ciao': 1,
                           'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1}

        content = read_dict_from_file(file_path_filt)
        assert content == {'ciao': 2, 'facendo': 2, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1, 'stiamo': 1, 'una': 1,
                           'prova': 1}

    # fallisce perchè aggiunge al csv anche i file di text_mining.txt_text_mining.txt vuoti, quindi il numero di righe saranno 68
    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {}}
    ], indirect=True)
    def test_case_18(self, setup_environment, create_temp_file):
        for i in range(1, 36, 1):
            if i != 18:
                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i), f"commit{i}")
                if i % 2 == 0:
                    create_temp_file(repo_dir + "/" + f"file{i}.java", "ciao stiamo facendo una prova")
                    create_temp_file(repo_dir + "/" + f"file{i}.java_text_mining.txt", "")
                else:
                    create_temp_file(repo_dir + "/" + f"file{i}.java", f"CIAO stiamo Facendo test sui file dispari")
                    create_temp_file(repo_dir + "/" + f"file{i}.java_text_mining.txt", "")

        text_mining_main()
        dict_gen_main()
        less_element_main()
        creator_csv_main()

        file_path_dict = os.path.join(self.BASE_DIR, "mining_results", "text_mining_dict.txt")
        content = read_dict_from_file(file_path_dict)
        assert content == {'CIAO': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1, 'ciao': 1,
                           'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1}

        file_path_filt = os.path.join(self.BASE_DIR, "mining_results", "FilteredTextMining.txt")
        content = read_dict_from_file(file_path_filt)
        assert content == {'ciao': 2, 'facendo': 2, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1, 'stiamo': 1,
                           'una': 1, 'prova': 1}

        file_path_csv = os.path.join(self.BASE_DIR, "mining_results", "csv_mining_final.csv")
        for i in range(1, 36, 1):

            if i != 18:
                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i), f"commit{i}")
                assert os.listdir(repo_dir) == [f"file{i}.java", f"file{i}.java_text_mining.txt",
                                                f"file{i}.java_text_mining.txt_text_mining.txt"]

                file_path = os.path.join(repo_dir, f"file{i}.java_text_mining.txt")
                content = read_dict_from_file(file_path)
                if i % 2 == 0:
                    assert content == {'ciao': 1, 'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1}
                else:
                    assert content == {'CIAO': 1, 'stiamo': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1,
                                       'dispari': 1}

            if i < 17:
                if i % 2 == 0:
                    check_csv(i - 1, file_path_csv, ['ciao ', 'stiamo ', 'facendo ', 'una ', 'prova '],
                              34)  # 34 perchè il 18 non ci sta
                else:
                    check_csv(i - 1, file_path_csv,
                              ['ciao ', 'stiamo ', 'facendo ', 'test ', 'sui ', 'file ', 'dispari '],
                              34)  # le colonne sono tutte salvate con lo spazio alla fine
            elif 17 < i < 34:
                if i % 2 == 0:
                    check_csv(i, file_path_csv, ['ciao ', 'stiamo ', 'facendo ', 'una ', 'prova '],
                              34)  # 34 perchè il 18 non ci sta
                else:
                    check_csv(i, file_path_csv,
                              ['ciao ', 'stiamo ', 'facendo ', 'test ', 'sui ', 'file ', 'dispari '],
                              34)  # le colonne sono tutte salvate con lo spazio alla fine

    #fallisce perchè aggiunge al csv anche i file di text_mining.txt_text_mining.txt vuoti, quindi il numero di righe saranno 68
    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {}}
    ], indirect=True)
    def test_case_19(self, setup_environment, create_temp_file):
        for i in range(1, 36, 1):
            if i != 18:
                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i), f"commit{i}")
                if i % 2 == 0:
                    create_temp_file(repo_dir + "/" + f"file{i}.java", "ciao stiamo facendo una prova")
                    create_temp_file(repo_dir + "/" + f"file{i}.java_text_mining.txt", "{'ciao': 1, 'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1}")
                else:
                    create_temp_file(repo_dir + "/" + f"file{i}.java", f"CIAO stiamo Facendo test sui file dispari")
                    create_temp_file(repo_dir + "/" + f"file{i}.java_text_mining.txt", "{'CIAO': 1, 'stiamo': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1}")

        text_mining_main()
        dict_gen_main()
        less_element_main()
        creator_csv_main()

        file_path_dict = os.path.join(self.BASE_DIR, "mining_results", "text_mining_dict.txt")
        content = read_dict_from_file(file_path_dict)
        assert content == {'CIAO': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1, 'ciao': 1,
                           'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1}

        file_path_filt = os.path.join(self.BASE_DIR, "mining_results", "FilteredTextMining.txt")
        content = read_dict_from_file(file_path_filt)
        assert content == {'ciao': 2, 'facendo': 2, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1, 'stiamo': 1, 'una': 1,
                           'prova': 1}

        file_path_csv = os.path.join(self.BASE_DIR, "mining_results", "csv_mining_final.csv")
        for i in range(1, 36, 1):

            if i != 18:
                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i), f"commit{i}")
                assert os.listdir(repo_dir) == [f"file{i}.java", f"file{i}.java_text_mining.txt", f"file{i}.java_text_mining.txt_text_mining.txt"]

                file_path = os.path.join(repo_dir, f"file{i}.java_text_mining.txt")
                content = read_dict_from_file(file_path)
                if i % 2 == 0:
                    assert content == {'ciao': 1, 'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1}
                else:
                    assert content == {'CIAO': 1, 'stiamo': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1}

            if i < 17:
                if i % 2 == 0:
                    check_csv(i-1, file_path_csv, ['ciao ', 'stiamo ', 'facendo ', 'una ', 'prova '], 34) #34 perchè il 18 non ci sta
                else:
                    check_csv(i-1, file_path_csv, ['ciao ', 'stiamo ', 'facendo ', 'test ', 'sui ', 'file ', 'dispari '], 34)  # le colonne sono tutte salvate con lo spazio alla fine
            elif 17 < i < 34:
                if i % 2 == 0:
                    check_csv(i, file_path_csv, ['ciao ', 'stiamo ', 'facendo ', 'una ', 'prova '],
                              34)  # 34 perchè il 18 non ci sta
                else:
                    check_csv(i, file_path_csv,
                              ['ciao ', 'stiamo ', 'facendo ', 'test ', 'sui ', 'file ', 'dispari '],
                              34)  # le colonne sono tutte salvate con lo spazio alla fine

    # funziona anche con file non java, forse controllo???
    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {'file.txt': ''}}
    ], indirect=True)
    def test_case_20(self, setup_environment):
        text_mining_main()
        dict_gen_main()
        less_element_main()
        creator_csv_main()

        repo_dir = os.path.join(self.BASE_DIR, "mining_results", "RepositoryMining1/1/", "commit1")
        assert os.listdir(repo_dir) == ["file.txt", "file.txt_text_mining.txt"]

        file_path = os.path.join(repo_dir, "file.txt_text_mining.txt")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == "{}", "Il file non è un dizionario vuoto"

"""
    #fallisce perchè si aspetta altri file nel csv, come commit1/file1.java__, i '_' non vengono eliminati
    #non fallisce se nei text_mining.txt c'è un dizionario sbaglio, va quindi a sovrascriverlo correttamente
    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {}}
    ], indirect=True)
    def test_case_12(self, setup_environment, create_temp_file):
        for i in range(1, 36, 1):
            if i != 18:
                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i), f"commit{i}")
                if i % 2 == 0:
                    create_temp_file(repo_dir + "/" + f"file{i}.java",
                                     "ciao stiamo facendo una prova")
                    create_temp_file(
                        repo_dir + "/" + f"file{i}.java_text_mining.txt",
                        "{'ciao': 3, 'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1, 'test': 3}")
                else:
                    create_temp_file(repo_dir + "/" + f"file{i}.java",
                                     f"CIAO stiamo Facendo test sui file dispari")
                    create_temp_file(
                        repo_dir + "/" + f"file{i}.java_text_mining.txt",
                        "{'CIAO': 1, 'stiamo': 10, 'Facendo': 1, 'sui': 1, 'file': 1, 'dispari': 1}")

        text_mining_main()
        dict_gen_main()
        less_element_main()
        creator_csv_main()

        file_path_csv = os.path.join(self.BASE_DIR, "mining_results", "csv_mining_final.csv")
        for i in range(1, 36, 1):
            if i != 18:
                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(self.BASE_DIR, "mining_results", repo_name, str(i), f"commit{i}")
                assert os.listdir(repo_dir) == [f"file{i}.java", f"file{i}.java_text_mining.txt",
                                                f"file{i}.java_text_mining.txt_text_mining.txt"]

                file_path = os.path.join(repo_dir, f"file{i}.java_text_mining.txt")
                content = read_dict_from_file(file_path)
                if i % 2 == 0:
                    assert content == {'ciao': 1, 'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1}
                else:
                    assert content == {'CIAO': 1, 'stiamo': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1,
                                       'dispari': 1}

            if i < 17:
                if i % 2 == 0:
                    check_csv(i - 1, file_path_csv, ['ciao ', 'stiamo ', 'facendo ', 'una ', 'prova '],
                              68)  # 34 perchè il 18 non ci sta
                else:
                    check_csv(i - 1, file_path_csv,
                              ['ciao ', 'stiamo ', 'facendo ', 'test ', 'sui ', 'file ', 'dispari '],
                              68)  # le colonne sono tutte salvate con lo spazio alla fine
            elif 17 < i < 34:
                if i % 2 == 0:
                    check_csv(i, file_path_csv, ['ciao ', 'stiamo ', 'facendo ', 'una ', 'prova '],
                              68)  # 34 perchè il 18 non ci sta
                else:
                    check_csv(i, file_path_csv,
                              ['ciao ', 'stiamo ', 'facendo ', 'test ', 'sui ', 'file ', 'dispari '],
                              68)  # le colonne sono tutte salvate con lo spazio alla fine

        file_path_dict = os.path.join(self.BASE_DIR, "mining_results", "text_mining_dict.txt")
        content = read_dict_from_file(file_path_dict)
        assert content == {'CIAO': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1, 'ciao': 1,
                           'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1}

        file_path_filt = os.path.join(self.BASE_DIR, "mining_results", "FilteredTextMining.txt")
        content = read_dict_from_file(file_path_filt)
        assert content == {'ciao': 2, 'facendo': 2, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1, 'stiamo': 1,
                           'una': 1, 'prova': 1}
"""