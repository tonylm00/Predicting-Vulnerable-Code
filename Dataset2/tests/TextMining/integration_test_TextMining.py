import ast
import os
import csv
import shutil
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

def check_words_in_dict(string, dictionary, values_for_keys=None, default_value=1):
    if values_for_keys is None:
        values_for_keys = {}  # Dizionario vuoto se non vengono passati valori specifici

    words = string.split()
    for word in words:
        expected_value = values_for_keys.get(word, default_value)  # Valore specifico o predefinito
        if dictionary.get(word) != expected_value:
            return False
    return True

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
    def test_case_2(self):
        """
        Testa che venga sollevata un'eccezione quando la directory 'mining_results' non esiste.
        """
        # Percorso della directory da eliminare
        mining_results_dir = os.path.dirname(self.BASE_DIR)
        os.mkdir(mining_results_dir+'/'+"mining_results", mode=0o777)

        try:
            with pytest.raises(FileNotFoundError, match=r".*RepositoryMining1"):
                text_mining_main()
                dict_gen_main()
                less_element_main()
                creator_csv_main()
        finally:
            os.chdir(self.BASE_DIR)
            shutil.rmtree(mining_results_dir+'/'+"mining_results")

    #text_mining.py prova ad accedere a RepositoryMining18, che non esiste
    #controllare nel main così da evitare di accedere a RepositoryMining18
    def test_case_3(self):
        mining_results_dir = os.path.dirname(self.BASE_DIR)
        os.mkdir(mining_results_dir + '/' + "mining_results", mode=0o777)

        for i in range(1, 36, 1):
            if i == 18:
                continue  # Salta RepositoryMining18

            repo_name = f"RepositoryMining{i}"
            repo_dir = os.path.join(mining_results_dir, "mining_results", repo_name)

            os.mkdir(repo_dir, mode=0o777)

        try:
            text_mining_main()
            dict_gen_main()
            less_element_main()
            creator_csv_main()
            for i in range(1, 36, 1):
                if i == 18:
                    continue  # Salta RepositoryMining18

                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(mining_results_dir, "mining_results", repo_name)
                assert os.listdir(repo_dir) == []

            file_path = os.path.join(mining_results_dir, "mining_results", "text_mining_dict.txt")
            with open(file_path, 'r') as file:
                content = file.read()
            assert content == "{}", "Il file non è un dizionario vuoto"

            file_path_filt = os.path.join(mining_results_dir, "mining_results", "FilteredTextMining.txt")
            with open(file_path_filt, 'r') as file:
                content = file.read()
            assert content == "{}", "Il file non è un dizionario vuoto"

            file_path_csv = os.path.join(mining_results_dir, "mining_results", "csv_mining_final.csv")
            expected_content = [
                ['NameClass ', 'class'],
                []
            ]
            with open(file_path_csv, newline='') as csvfile:
                reader = csv.reader(csvfile)
                actual_content = list(reader)
            assert actual_content == expected_content, "Il contenuto del file CSV non corrisponde a quello atteso"

        finally:
            os.chdir(self.BASE_DIR)
            shutil.rmtree(mining_results_dir+'/'+"mining_results")


    def test_case_4(self):
        mining_results_dir = os.path.dirname(self.BASE_DIR)
        os.mkdir(mining_results_dir + '/' + "mining_results", mode=0o777)

        for i in range(1, 36, 1):
            if i == 18:
                continue  # Salta RepositoryMining18

            repo_name = f"RepositoryMining{i}"
            repo_dir = os.path.join(mining_results_dir, "mining_results", repo_name)

            os.mkdir(repo_dir, mode=0o777)
            os.mkdir(repo_dir+"/"+str(i), mode=0o777)

        try:
            text_mining_main()
            dict_gen_main()
            less_element_main()
            creator_csv_main()
            for i in range(1, 36, 1):
                if i == 18:
                    continue  # Salta RepositoryMining18

                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(mining_results_dir, "mining_results", repo_name)
                assert os.listdir(repo_dir+"/"+str(i)) == []

            file_path = os.path.join(mining_results_dir, "mining_results", "text_mining_dict.txt")
            with open(file_path, 'r') as file:
                content = file.read()
            assert content == "{}", "Il file non è un dizionario vuoto"

            file_path_filt = os.path.join(mining_results_dir, "mining_results", "FilteredTextMining.txt")
            with open(file_path_filt, 'r') as file:
                content = file.read()
            assert content == "{}", "Il file non è un dizionario vuoto"

            file_path_csv = os.path.join(mining_results_dir, "mining_results", "csv_mining_final.csv")
            expected_content = [
                ['NameClass ', 'class'],
                []
            ]
            with open(file_path_csv, newline='') as csvfile:
                reader = csv.reader(csvfile)
                actual_content = list(reader)
            assert actual_content == expected_content, "Il contenuto del file CSV non corrisponde a quello atteso"

        finally:
            os.chdir(self.BASE_DIR)
            shutil.rmtree(mining_results_dir + '/' + "mining_results")


    def test_case_5(self):
        mining_results_dir = os.path.dirname(self.BASE_DIR)
        os.mkdir(mining_results_dir + '/' + "mining_results", mode=0o777)

        for i in range(1, 36, 1):
            if i == 18:
                continue  # Salta RepositoryMining18

            repo_name = f"RepositoryMining{i}"
            repo_dir = os.path.join(mining_results_dir, "mining_results", repo_name)

            os.mkdir(repo_dir, mode=0o777)
            os.mkdir(repo_dir+"/"+str(i), mode=0o777)
            os.mkdir(repo_dir + "/" + str(i) + "/" + "commit", mode=0o777)

        try:
            text_mining_main()
            dict_gen_main()
            less_element_main()
            creator_csv_main()
            for i in range(1, 36, 1):
                if i == 18:
                    continue  # Salta RepositoryMining18

                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(mining_results_dir, "mining_results", repo_name)
                assert os.listdir(repo_dir + "/" + str(i) + "/" + "commit") == []

            file_path = os.path.join(mining_results_dir, "mining_results", "text_mining_dict.txt")
            with open(file_path, 'r') as file:
                content = file.read()
            assert content == "{}", "Il file non è un dizionario vuoto"

            file_path_filt = os.path.join(mining_results_dir, "mining_results", "FilteredTextMining.txt")
            with open(file_path_filt, 'r') as file:
                content = file.read()
            assert content == "{}", "Il file non è un dizionario vuoto"

            file_path_csv = os.path.join(mining_results_dir, "mining_results", "csv_mining_final.csv")
            expected_content = [
                ['NameClass ', 'class'],
                []
            ]
            with open(file_path_csv, newline='') as csvfile:
                reader = csv.reader(csvfile)
                actual_content = list(reader)
            assert actual_content == expected_content, "Il contenuto del file CSV non corrisponde a quello atteso"

        finally:
            os.chdir(self.BASE_DIR)
            shutil.rmtree(mining_results_dir + '/' + "mining_results")

    #RepositoryMining1 non viene considerata nel for del text_mining
    def test_case_6(self):
        mining_results_dir = os.path.dirname(self.BASE_DIR)
        os.mkdir(mining_results_dir + '/' + "mining_results", mode=0o777)

        for i in range(1, 36, 1):
            if i == 18:
                continue  # Salta RepositoryMining18

            repo_name = f"RepositoryMining{i}"
            repo_dir = os.path.join(mining_results_dir, "mining_results", repo_name)

            os.mkdir(repo_dir, mode=0o777)
            os.mkdir(repo_dir + "/" + str(i), mode=0o777)
            os.mkdir(repo_dir + "/" + str(i) + "/" + "commit", mode=0o777)
            os.mkdir(repo_dir + "/" + str(i) + "/" + "commit" + "/" + "directory", mode=0o777)

        try:
            with pytest.raises(PermissionError, match=r".*Permission denied: 'directory'"):
                text_mining_main()
                dict_gen_main()
                less_element_main()
                creator_csv_main()
        finally:
            os.chdir(self.BASE_DIR)
            shutil.rmtree(mining_results_dir + '/' + "mining_results")

    #modificare la codifica nella lettura e scrittura dei file in utf-8 per tutti gli script (creava sempre un errore di UnicodeDecodeError non previsto)
    def test_case_7(self, create_temp_file):
        mining_results_dir = os.path.dirname(self.BASE_DIR)
        try:
            os.mkdir(mining_results_dir + '/' + "mining_results", mode=0o777)

            for i in range(1, 36, 1):
                if i == 18:
                    continue  # Salta RepositoryMining18

                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(mining_results_dir, "mining_results", repo_name)
                os.mkdir(repo_dir, mode=0o777)
                os.mkdir(repo_dir + "/" + str(i), mode=0o777)
                os.mkdir(repo_dir + "/" + str(i) + "/" + "commit", mode=0o777)
                create_temp_file(repo_dir + "/" + str(i) + "/" + "commit/"+"file.java", "")

            text_mining_main()
            dict_gen_main()
            less_element_main()
            creator_csv_main()

            repo_dir = os.path.join(mining_results_dir, "mining_results", "RepositoryMining1/1/","commit")
            assert os.listdir(repo_dir) == ["file.java", "file.java_text_mining.txt"]

            file_path = os.path.join(repo_dir, "file.java_text_mining.txt")
            with open(file_path, 'r') as file:
                content = file.read()
            assert content == "{}", "Il file non è un dizionario vuoto"

        finally:
            os.chdir(self.BASE_DIR)
            shutil.rmtree(mining_results_dir + '/' + "mining_results")

    #Se già presente text_mining, lo sovrascivere ma crea un nuovo file con il nome file.java_text_mining.txt_text_mining.txt
    #ottimizzare con controllo che text_mining non deve essere presente nel nome o che il file deve avere estensione .java
    def test_case_8(self, create_temp_file):
        mining_results_dir = os.path.dirname(self.BASE_DIR)
        try:
            os.mkdir(mining_results_dir + '/' + "mining_results", mode=0o777)

            for i in range(1, 36, 1):
                if i == 18:
                    continue  # Salta RepositoryMining18

                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(mining_results_dir, "mining_results", repo_name)
                os.mkdir(repo_dir, mode=0o777)
                os.mkdir(repo_dir + "/" + str(i), mode=0o777)
                os.mkdir(repo_dir + "/" + str(i) + "/" + "commit", mode=0o777)
                create_temp_file(repo_dir + "/" + str(i) + "/" + "commit/" + "file.java", "")
                create_temp_file(repo_dir + "/" + str(i) + "/" + "commit/" + "file.java_text_mining.txt", "")

            text_mining_main()
            dict_gen_main()
            less_element_main()
            creator_csv_main()

            repo_dir = os.path.join(mining_results_dir, "mining_results", "RepositoryMining1/1/", "commit")
            assert os.listdir(repo_dir) == ["file.java", "file.java_text_mining.txt",
                                             "file.java_text_mining.txt_text_mining.txt"]
            file_path = os.path.join(repo_dir, "file.java_text_mining.txt")
            with open(file_path, 'r') as file:
                content = file.read()
            assert content == "{}", "Il file non è un dizionario vuoto"

        finally:
            os.chdir(self.BASE_DIR)
            shutil.rmtree(mining_results_dir + '/' + "mining_results")

    #funziona anche con file non java, forse controllo???
    def test_case_9(self, create_temp_file):
        mining_results_dir = os.path.dirname(self.BASE_DIR)
        try:
            os.mkdir(mining_results_dir + '/' + "mining_results", mode=0o777)

            for i in range(1, 36, 1):
                if i == 18:
                    continue  # Salta RepositoryMining18

                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(mining_results_dir, "mining_results", repo_name)
                os.mkdir(repo_dir, mode=0o777)
                os.mkdir(repo_dir + "/" + str(i), mode=0o777)
                os.mkdir(repo_dir + "/" + str(i) + "/" + "commit", mode=0o777)
                create_temp_file(repo_dir + "/" + str(i) + "/" + "commit/" + "file.txt", "")

            text_mining_main()
            dict_gen_main()
            less_element_main()
            creator_csv_main()

            repo_dir = os.path.join(mining_results_dir, "mining_results", "RepositoryMining1/1/", "commit")
            assert os.listdir(repo_dir) == ["file.txt", "file.txt_text_mining.txt"]

            file_path = os.path.join(repo_dir, "file.txt_text_mining.txt")
            with open(file_path, 'r') as file:
                content = file.read()
            assert content == "{}", "Il file non è un dizionario vuoto"

        finally:
            os.chdir(self.BASE_DIR)
            shutil.rmtree(mining_results_dir + '/' + "mining_results")

    def test_case_10(self, create_temp_file):
        mining_results_dir = os.path.dirname(self.BASE_DIR)
        try:
            os.mkdir(mining_results_dir + '/' + "mining_results", mode=0o777)

            for i in range(1, 36, 1):
                if i == 18:
                    continue  # Salta RepositoryMining18

                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(mining_results_dir, "mining_results", repo_name)
                os.mkdir(repo_dir, mode=0o777)
                os.mkdir(repo_dir + "/" + str(i), mode=0o777)
                os.mkdir(repo_dir + "/" + str(i) + "/" + f"commit{i}", mode=0o777)
                if i % 2 == 0:
                    create_temp_file(repo_dir + "/" + str(i) + "/" + f"commit{i}/" + f"file{i}.java", f"ciao stiamo facendo una prova")
                else:
                    create_temp_file(repo_dir + "/" + str(i) + "/" + f"commit{i}/" + f"file{i}.java", f"CIAO stiamo Facendo test sui file dispari")
            text_mining_main()
            dict_gen_main()
            less_element_main()
            creator_csv_main()

            file_path_csv = os.path.join(mining_results_dir, "mining_results", "csv_mining_final.csv")
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

                if i == 18:
                    continue

                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(mining_results_dir, "mining_results", repo_name, str(i), f"commit{i}")
                assert os.listdir(repo_dir) == [f"file{i}.java", f"file{i}.java_text_mining.txt"]

                file_path = os.path.join(repo_dir, f"file{i}.java_text_mining.txt")
                content = read_dict_from_file(file_path)
                if i % 2 == 0:
                    assert content == {'ciao': 1, 'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1}
                else:
                    assert content == {'CIAO': 1, 'stiamo': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1}


            file_path_dict = os.path.join(mining_results_dir, "mining_results", "text_mining_dict.txt")
            content = read_dict_from_file(file_path_dict)
            assert content == {'CIAO': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1, 'ciao': 1, 'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1}

            file_path_filt = os.path.join(mining_results_dir, "mining_results", "FilteredTextMining.txt")
            content = read_dict_from_file(file_path_filt)
            assert content == {'ciao': 2, 'facendo': 2, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1, 'stiamo': 1, 'una': 1, 'prova': 1}

        finally:
            os.chdir(self.BASE_DIR)
            shutil.rmtree(mining_results_dir + '/' + "mining_results")

    #fallisce perchè aggiunge al csv anche i file di text_mining.txt_text_mining.txt vuoti, quindi il numero di righe saranno 68
    def test_case_11(self, create_temp_file):
        mining_results_dir = os.path.dirname(self.BASE_DIR)
        try:
            os.mkdir(mining_results_dir + '/' + "mining_results", mode=0o777)

            for i in range(1, 36, 1):
                if i == 18:
                    continue  # Salta RepositoryMining18

                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(mining_results_dir, "mining_results", repo_name)
                os.mkdir(repo_dir, mode=0o777)
                os.mkdir(repo_dir + "/" + str(i), mode=0o777)
                os.mkdir(repo_dir + "/" + str(i) + "/" + f"commit{i}", mode=0o777)
                if i % 2 == 0:
                    create_temp_file(repo_dir + "/" + str(i) + "/" + f"commit{i}/" + f"file{i}.java", "ciao stiamo facendo una prova")
                    create_temp_file(repo_dir + "/" + str(i) + "/" + f"commit{i}/" + f"file{i}.java_text_mining.txt", "{'ciao': 1, 'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1}")
                else:
                    create_temp_file(repo_dir + "/" + str(i) + "/" + f"commit{i}/" + f"file{i}.java", f"CIAO stiamo Facendo test sui file dispari")
                    create_temp_file(repo_dir + "/" + str(i) + "/" + f"commit{i}/" + f"file{i}.java_text_mining.txt", "{'CIAO': 1, 'stiamo': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1}")

            text_mining_main()
            dict_gen_main()
            less_element_main()
            creator_csv_main()

            file_path_csv = os.path.join(mining_results_dir, "mining_results", "csv_mining_final.csv")
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

                if i == 18:
                    continue

                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(mining_results_dir, "mining_results", repo_name, str(i), f"commit{i}")
                assert os.listdir(repo_dir) == [f"file{i}.java", f"file{i}.java_text_mining.txt", f"file{i}.java_text_mining.txt_text_mining.txt"]

                file_path = os.path.join(repo_dir, f"file{i}.java_text_mining.txt")
                content = read_dict_from_file(file_path)
                if i % 2 == 0:
                    assert content == {'ciao': 1, 'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1}
                else:
                    assert content == {'CIAO': 1, 'stiamo': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1}


            file_path_dict = os.path.join(mining_results_dir, "mining_results", "text_mining_dict.txt")
            content = read_dict_from_file(file_path_dict)
            assert content == {'CIAO': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1, 'ciao': 1, 'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1}

            file_path_filt = os.path.join(mining_results_dir, "mining_results", "FilteredTextMining.txt")
            content = read_dict_from_file(file_path_filt)
            assert content == {'ciao': 2, 'facendo': 2, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1, 'stiamo': 1, 'una': 1, 'prova': 1}

        finally:
            os.chdir(self.BASE_DIR)
            shutil.rmtree(mining_results_dir + '/' + "mining_results")

    #fallisce perchè si aspetta altri file nel csv, come commit1/file1.java__, i '_' non vengono eliminati
    #non fallisce se nei text_mining.txt c'è un dizionario sbaglio, va quindi a sovrascriverlo correttamente
    def test_case_12(self, move_directory, create_temp_file):
        mining_results_dir = os.path.dirname(self.BASE_DIR)
        try:
            os.mkdir(mining_results_dir + '/' + "mining_results", mode=0o777)

            for i in range(1, 36, 1):
                if i == 18:
                    continue  # Salta RepositoryMining18

                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(mining_results_dir, "mining_results", repo_name)
                os.mkdir(repo_dir, mode=0o777)
                os.mkdir(repo_dir + "/" + str(i), mode=0o777)
                os.mkdir(repo_dir + "/" + str(i) + "/" + f"commit{i}", mode=0o777)
                if i % 2 == 0:
                    create_temp_file(repo_dir + "/" + str(i) + "/" + f"commit{i}/" + f"file{i}.java",
                                     "ciao stiamo facendo una prova")
                    create_temp_file(
                        repo_dir + "/" + str(i) + "/" + f"commit{i}/" + f"file{i}.java_text_mining.txt",
                        "{'ciao': 3, 'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1, 'test': 3}")
                else:
                    create_temp_file(repo_dir + "/" + str(i) + "/" + f"commit{i}/" + f"file{i}.java",
                                     f"CIAO stiamo Facendo test sui file dispari")
                    create_temp_file(
                        repo_dir + "/" + str(i) + "/" + f"commit{i}/" + f"file{i}.java_text_mining.txt",
                        "{'CIAO': 1, 'stiamo': 10, 'Facendo': 1, 'sui': 1, 'file': 1, 'dispari': 1}")

            text_mining_main()
            dict_gen_main()
            less_element_main()
            creator_csv_main()

            file_path_csv = os.path.join(mining_results_dir, "mining_results", "csv_mining_final.csv")
            for i in range(1, 36, 1):
                if i != 18:
                    repo_name = f"RepositoryMining{i}"
                    repo_dir = os.path.join(mining_results_dir, "mining_results", repo_name, str(i), f"commit{i}")
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


            file_path_dict = os.path.join(mining_results_dir, "mining_results", "text_mining_dict.txt")
            content = read_dict_from_file(file_path_dict)
            assert content == {'CIAO': 1, 'Facendo': 1, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1, 'ciao': 1,
                               'stiamo': 1, 'facendo': 1, 'una': 1, 'prova': 1}

            file_path_filt = os.path.join(mining_results_dir, "mining_results", "FilteredTextMining.txt")
            content = read_dict_from_file(file_path_filt)
            assert content == {'ciao': 2, 'facendo': 2, 'test': 1, 'sui': 1, 'file': 1, 'dispari': 1, 'stiamo': 1,
                               'una': 1, 'prova': 1}

        finally:
            os.chdir(self.BASE_DIR)
            shutil.rmtree(mining_results_dir + '/' + "mining_results")