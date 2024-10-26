import ast
import csv
import os
from unittest.mock import patch
import pytest
from Dataset2.Main import Main

class TestSoftwareMetricsIntegration:
    BASE_DIR = os.getcwd()
    @pytest.fixture(autouse=True)
    def setup(self, setup_environment):
        self.main = Main(self.BASE_DIR)

    @patch('builtins.print')
    @pytest.mark.parametrize('setup_environment', [
        {'levels': 0, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_1(self, mock_print, setup_environment):
        self.main.run_software_metrics()
        mock_print.called_once_with("Errore durante l'apertura del file: [Errno 2] No such file or directory: 'Software_Metrics/mining_results_sm_final.csv'")

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 1, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_2(self, setup_environment):
        self.main.run_software_metrics()
        file_path = os.path.join(self.BASE_DIR, "Software_Metrics", "mining_results_sm_final.csv")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == ("Kind,Name,CountLineCode,CountDeclClass,CountDeclFunction,CountLineCodeDecl,SumEssential,SumCyclomaticStrict,MaxEssential,MaxCyclomaticStrict,MaxNesting\n"), "Il file non contiene solo l'header del CSV"

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 2, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_3(self, setup_environment):
        self.main.run_text_mining()
        self.main.run_software_metrics()
        file_path = os.path.join(self.BASE_DIR, "Software_Metrics", "mining_results_sm_final.csv")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == (
            "Kind,Name,CountLineCode,CountDeclClass,CountDeclFunction,CountLineCodeDecl,SumEssential,SumCyclomaticStrict,MaxEssential,MaxCyclomaticStrict,MaxNesting\n"), "Il file non contiene solo l'header del CSV"


    @pytest.mark.parametrize('setup_environment', [
        {'levels': 2, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_4(self, setup_environment, create_temp_file):
        create_temp_file(self.BASE_DIR + "/mining_results/" + "RepositoryMining1/" + f"file1.java",
                         f"ciao stiamo facendo una prova")

        self.main.run_software_metrics()
        file_path = os.path.join(self.BASE_DIR, "Software_Metrics", "mining_results_sm_final.csv")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == (
            "Kind,Name,CountLineCode,CountDeclClass,CountDeclFunction,CountLineCodeDecl,SumEssential,SumCyclomaticStrict,MaxEssential,MaxCyclomaticStrict,MaxNesting\n"), "Il file non contiene solo l'header del CSV"


    @pytest.mark.parametrize('setup_environment', [
        {'levels': 2, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_5(self, setup_environment, create_temp_file):
        for i in range(1, 36, 1):
            create_temp_file(self.BASE_DIR + "/mining_results/" + f"RepositoryMining{i}/" + f"CHECK.txt", "")

        self.main.run_software_metrics()
        file_path = os.path.join(self.BASE_DIR, "Software_Metrics", "mining_results_sm_final.csv")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == (
            "Kind,Name,CountLineCode,CountDeclClass,CountDeclFunction,CountLineCodeDecl,SumEssential,SumCyclomaticStrict,MaxEssential,MaxCyclomaticStrict,MaxNesting\n"), "Il file non contiene solo l'header del CSV"


    @pytest.mark.parametrize('setup_environment', [
        {'levels': 3, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_6(self, setup_environment):
        self.main.run_text_mining()
        self.main.run_software_metrics()
        file_path = os.path.join(self.BASE_DIR, "Software_Metrics", "mining_results_sm_final.csv")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == (
            "Kind,Name,CountLineCode,CountDeclClass,CountDeclFunction,CountLineCodeDecl,SumEssential,SumCyclomaticStrict,MaxEssential,MaxCyclomaticStrict,MaxNesting\n"), "Il file non contiene solo l'header del CSV"


    @pytest.mark.parametrize('setup_environment', [
        {'levels': 3, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_7(self, setup_environment, create_temp_file):
        create_temp_file(self.BASE_DIR + "/mining_results/" + "RepositoryMining1/1/" + f"file1.java",
                         f"ciao stiamo facendo una prova")

        self.main.run_software_metrics()
        file_path = os.path.join(self.BASE_DIR, "Software_Metrics", "mining_results_sm_final.csv")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == (
            "Kind,Name,CountLineCode,CountDeclClass,CountDeclFunction,CountLineCodeDecl,SumEssential,SumCyclomaticStrict,MaxEssential,MaxCyclomaticStrict,MaxNesting\n"), "Il file non contiene solo l'header del CSV"


    @pytest.mark.parametrize('setup_environment', [
        {'levels': 3, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_8(self, setup_environment, create_temp_file):
        for i in range(1, 36, 1):
            create_temp_file(self.BASE_DIR + "/mining_results/" + f"RepositoryMining{i}/" + str(i) + f"/.DS_Store", "")

        self.main.run_software_metrics()
        file_path = os.path.join(self.BASE_DIR, "Software_Metrics", "mining_results_sm_final.csv")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == (
            "Kind,Name,CountLineCode,CountDeclClass,CountDeclFunction,CountLineCodeDecl,SumEssential,SumCyclomaticStrict,MaxEssential,MaxCyclomaticStrict,MaxNesting\n"), "Il file non contiene solo l'header del CSV"


    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_9(self, setup_environment):
        self.main.run_software_metrics()
        file_path = os.path.join(self.BASE_DIR, "Software_Metrics", "mining_results_sm_final.csv")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == (
            "Kind,Name,CountLineCode,CountDeclClass,CountDeclFunction,CountLineCodeDecl,SumEssential,SumCyclomaticStrict,MaxEssential,MaxCyclomaticStrict,MaxNesting\n"), "Il file non contiene solo l'header del CSV"


    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_10(self, setup_environment, create_temp_file):
        for i in range(1, 36, 1):
            create_temp_file(self.BASE_DIR + "/mining_results/" + f"RepositoryMining{i}/" + str(
                    i) + f"/commit{i}/" + f".DS_Store", "")

        self.main.run_software_metrics()
        file_path = os.path.join(self.BASE_DIR, "Software_Metrics", "mining_results_sm_final.csv")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == (
            "Kind,Name,CountLineCode,CountDeclClass,CountDeclFunction,CountLineCodeDecl,SumEssential,SumCyclomaticStrict,MaxEssential,MaxCyclomaticStrict,MaxNesting\n"), "Il file non contiene solo l'header del CSV"

    # RepositoryMining1 non viene considerata nel for del text_mining
    @pytest.mark.parametrize('setup_environment', [
        {'levels': 5, 'base_dir': BASE_DIR}
    ], indirect=True)
    def test_case_11(self, setup_environment):
        self.main.run_software_metrics()
        file_path = os.path.join(self.BASE_DIR, "Software_Metrics", "mining_results_sm_final.csv")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == (
            "Kind,Name,CountLineCode,CountDeclClass,CountDeclFunction,CountLineCodeDecl,SumEssential,SumCyclomaticStrict,MaxEssential,MaxCyclomaticStrict,MaxNesting\n"), "Il file non contiene solo l'header del CSV"

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {'file.java': ''}}
    ], indirect=True)
    def test_case_12(self, setup_environment, create_temp_file):
        self.main.run_software_metrics()

        log_path = os.path.join(self.BASE_DIR, "Software_Metrics", "software_metrics.log")
        with open(log_path, 'r') as file_log:
            content_log = file_log.read()
        assert content_log == "", "Il file non contiene i valori attesi"

        file_path = os.path.join(self.BASE_DIR, "Software_Metrics", "mining_results_sm_final.csv")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == ('Kind,Name,CountLineCode,CountDeclClass,CountDeclFunction,CountLineCodeDecl,SumEssential,SumCyclomaticStrict,MaxEssential,MaxCyclomaticStrict,MaxNesting\n'
             'File,commit1\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit2\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit3\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit4\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit5\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit6\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit7\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit8\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit9\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit10\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit11\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit12\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit13\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit14\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit15\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit16\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit17\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit18\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit19\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit20\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit21\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit22\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit23\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit24\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit25\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit26\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit27\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit28\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit29\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit30\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit31\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit32\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit33\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit34\\file.java,0,0,0,0,0,0,0,0,0\n'
             'File,commit35\\file.java,0,0,0,0,0,0,0,0,0\n'), "Il file non contiene i valori attesi"

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {'file.java': """class Persona:
            def __init__(self, nome, eta):
                self.nome = nome
                self.eta = eta
        
            def saluta(self):
                return f"Ciao, mi chiamo {self.nome} e ho {self.eta} anni."""}}
    ], indirect=True)
    def test_case_13(self, setup_environment, create_temp_file):
        self.main.run_software_metrics()
        log_path = os.path.join(self.BASE_DIR, "Software_Metrics", "software_metrics.log")
        with open(log_path, 'r') as file_log:
            content_log = file_log.read()
        assert content_log == ("ERROR - Errore nell'analisi del file commit1\\file.java: Il file presenta un "
         'carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit2\\file.java: Il file presenta un "
         'carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit3\\file.java: Il file presenta un "
         'carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit4\\file.java: Il file presenta un "
         'carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit5\\file.java: Il file presenta un "
         'carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit6\\file.java: Il file presenta un "
         'carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit7\\file.java: Il file presenta un "
         'carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit8\\file.java: Il file presenta un "
         'carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit9\\file.java: Il file presenta un "
         'carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit10\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit11\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit12\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit13\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit14\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit15\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit16\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit17\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit18\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit19\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit20\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit21\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit22\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit23\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit24\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit25\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit26\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit27\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit28\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit29\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit30\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit31\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit32\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit33\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit34\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'
         "ERROR - Errore nell'analisi del file commit35\\file.java: Il file presenta "
         'un carattere o una sequenza di caratteri non valida.\n'), "Il file non contiene i valori attesi"
        file_path = os.path.join(self.BASE_DIR, "Software_Metrics", "mining_results_sm_final.csv")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == (
            'Kind,Name,CountLineCode,CountDeclClass,CountDeclFunction,CountLineCodeDecl,SumEssential,SumCyclomaticStrict,MaxEssential,MaxCyclomaticStrict,MaxNesting\n'
             'File,commit1\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit2\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit3\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit4\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit5\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit6\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit7\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit8\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit9\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit10\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit11\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit12\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit13\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit14\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit15\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit16\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit17\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit18\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit19\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit20\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit21\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit22\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit23\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit24\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit25\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit26\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit27\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit28\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit29\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit30\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit31\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit32\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit33\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit34\\file.java,6,1,0,7,0,0,0,0,0\n'
             'File,commit35\\file.java,6,1,0,7,0,0,0,0,0\n'), "Il file non contiene i valori attesi"

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {'file.java': """class Persona:
                def __init__(self, nome, eta):
                    self.nome = nome
                    self.eta = eta

                def saluta(self):
                    return f"Ciao, mi chiamo {self.nome} e ho {self.eta} anni."""}}
    ], indirect=True)
    def test_case_14(self, setup_environment, create_temp_file):
        create_temp_file(self.BASE_DIR + "/Software_Metrics/software_metrics.log", "PRIMO ERRORE\n")
        self.main.run_software_metrics()
        log_path = os.path.join(self.BASE_DIR, "Software_Metrics", "software_metrics.log")
        with open(log_path, 'r') as file_log:
            content_log = file_log.read()
        assert content_log == ("PRIMO ERRORE\nERROR - Errore nell'analisi del file commit1\\file.java: Il file presenta un "
                               'carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit2\\file.java: Il file presenta un "
                               'carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit3\\file.java: Il file presenta un "
                               'carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit4\\file.java: Il file presenta un "
                               'carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit5\\file.java: Il file presenta un "
                               'carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit6\\file.java: Il file presenta un "
                               'carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit7\\file.java: Il file presenta un "
                               'carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit8\\file.java: Il file presenta un "
                               'carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit9\\file.java: Il file presenta un "
                               'carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit10\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit11\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit12\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit13\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit14\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit15\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit16\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit17\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit18\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit19\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit20\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit21\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit22\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit23\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit24\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit25\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit26\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit27\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit28\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit29\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit30\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit31\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit32\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit33\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit34\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'
                               "ERROR - Errore nell'analisi del file commit35\\file.java: Il file presenta "
                               'un carattere o una sequenza di caratteri non valida.\n'), "Il file non contiene i valori attesi"
        file_path = os.path.join(self.BASE_DIR, "Software_Metrics", "mining_results_sm_final.csv")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == (
            'Kind,Name,CountLineCode,CountDeclClass,CountDeclFunction,CountLineCodeDecl,SumEssential,SumCyclomaticStrict,MaxEssential,MaxCyclomaticStrict,MaxNesting\n'
            'File,commit1\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit2\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit3\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit4\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit5\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit6\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit7\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit8\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit9\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit10\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit11\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit12\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit13\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit14\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit15\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit16\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit17\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit18\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit19\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit20\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit21\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit22\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit23\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit24\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit25\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit26\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit27\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit28\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit29\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit30\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit31\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit32\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit33\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit34\\file.java,6,1,0,7,0,0,0,0,0\n'
            'File,commit35\\file.java,6,1,0,7,0,0,0,0,0\n'), "Il file non contiene i valori attesi"

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {'file.java': """public class Esempio {
            // Primo metodo con if-else, for e una classe anonima
            public void metodoUno(int numero) {
                if (numero > 0) {
                    for (int i = 0; i < numero; i++) {
                        System.out.println("Contatore: " + i);
                    }
                } else {
                    Runnable runnable = new Runnable() {
                        @Override
                        public void run() {
                            System.out.println("Numero non positivo!");
                        }
                    };
                    runnable.run();
                }
            }
        
            // Secondo metodo con if senza else, while, e switch
            public void metodoDue(String tipo) {
                int contatore = 0;
        
                while (contatore < 3) {
                    System.out.println("Ciclo while, contatore: " + contatore);
                    contatore++;
        
                    switch (tipo) {
                        case "A":
                            System.out.println("Tipo A selezionato");
                            break;
                        case "B":
                            System.out.println("Tipo B selezionato");
                            break;
                        default:
                            System.out.println("Tipo sconosciuto");
                            break;
                    }
                }
        
                if (contatore == 3) {
                    System.out.println("Ciclo while completato");
                }
            }
        
            // Terzo metodo con do-while e if annidati
            public void metodoTre(int valore) {
                int i = 0;
        
                do {
                    if (valore > 10) {
                        if (valore % 2 == 0) {
                            System.out.println("Valore maggiore di 10 e pari: " + valore);
                        } else {
                            System.out.println("Valore maggiore di 10 e dispari: " + valore);
                        }
                    } else {
                        System.out.println("Valore minore o uguale a 10: " + valore);
                    }
                    i++;
                } while (i < 5);
            }
        
            // Interfaccia dichiarata all'interno della classe
            interface Azione {
                void esegui();
            }
        
            public static void main(String[] args) {
                Esempio esempio = new Esempio();
                esempio.metodoUno(3);
                esempio.metodoDue("A");
                esempio.metodoTre(12);
            }
        }
        """}}
    ], indirect=True)
    def test_case_15(self, setup_environment, create_temp_file):
        self.main.run_software_metrics()

        log_path = os.path.join(self.BASE_DIR, "Software_Metrics", "software_metrics.log")
        with open(log_path, 'r') as file_log:
            content_log = file_log.read()
        assert content_log == "", "Il file non contiene i valori attesi"
        file_path = os.path.join(self.BASE_DIR, "Software_Metrics", "mining_results_sm_final.csv")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == (
            'Kind,Name,CountLineCode,CountDeclClass,CountDeclFunction,CountLineCodeDecl,SumEssential,SumCyclomaticStrict,MaxEssential,MaxCyclomaticStrict,MaxNesting\n'
            'File,commit1\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit2\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit3\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit4\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit5\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit6\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit7\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit8\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit9\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit10\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit11\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit12\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit13\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit14\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit15\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit16\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit17\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit18\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit19\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit20\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit21\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit22\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit23\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit24\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit25\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit26\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit27\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit28\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit29\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit30\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit31\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit32\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit33\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit34\\file.java,62,3,6,15,4,13,1,5,3\n'
             'File,commit35\\file.java,62,3,6,15,4,13,1,5,3\n'), "Il file non contiene i valori attesi"

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {'file.java': """public class Esempio {
                // Primo metodo con if-else, for e una classe anonima
                public void metodoUno(int numero) {
                    if (numero > 0) {
                        for (int i = 0; i < numero; i++) {
                            System.out.println("Contatore: " + i);
                        }
                    } else {
                        Runnable runnable = new Runnable() {
                            @Override
                            public void run() {
                                System.out.println("Numero non positivo!");
                            }
                        };
                        runnable.run();
                    }
                }

                // Secondo metodo con if senza else, while, e switch
                public void metodoDue(String tipo) {
                    int contatore = 0;

                    while (contatore < 3) {
                        System.out.println("Ciclo while, contatore: " + contatore);
                        contatore++;

                        switch (tipo) {
                            case "A":
                                System.out.println("Tipo A selezionato");
                                break;
                            case "B":
                                System.out.println("Tipo B selezionato");
                                break;
                            default:
                                System.out.println("Tipo sconosciuto");
                                break;
                        }
                    }

                    if (contatore == 3) {
                        System.out.println("Ciclo while completato");
                    }
                }

                // Terzo metodo con do-while e if annidati
                public void metodoTre(int valore) {
                    int i = 0;

                    do {
                        if (valore > 10) {
                            if (valore % 2 == 0) {
                                System.out.println("Valore maggiore di 10 e pari: " + valore);
                            } else {
                                System.out.println("Valore maggiore di 10 e dispari: " + valore);
                            }
                        } else {
                            System.out.println("Valore minore o uguale a 10: " + valore);
                        }
                        i++;
                    } while (i < 5);
                }

                // Interfaccia dichiarata all'interno della classe
                interface Azione {
                    void esegui();
                }

                public static void main(String[] args) {
                    Esempio esempio = new Esempio();
                    esempio.metodoUno(3);
                    esempio.metodoDue("A");
                    esempio.metodoTre(12);
                }
            }
            """}}
    ], indirect=True)
    def test_case_16(self, setup_environment, create_temp_file):
        create_temp_file(self.BASE_DIR + "/Software_Metrics/csv_mining_final.csv", "Prima riga del csv\n")

        self.main.run_software_metrics()

        log_path = os.path.join(self.BASE_DIR, "Software_Metrics", "software_metrics.log")
        with open(log_path, 'r') as file_log:
            content_log = file_log.read()
        assert content_log == "", "Il file non contiene i valori attesi"
        file_path = os.path.join(self.BASE_DIR, "Software_Metrics", "mining_results_sm_final.csv")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == (
            'Kind,Name,CountLineCode,CountDeclClass,CountDeclFunction,CountLineCodeDecl,SumEssential,SumCyclomaticStrict,MaxEssential,MaxCyclomaticStrict,MaxNesting\n'
            'File,commit1\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit2\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit3\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit4\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit5\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit6\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit7\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit8\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit9\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit10\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit11\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit12\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit13\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit14\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit15\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit16\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit17\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit18\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit19\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit20\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit21\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit22\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit23\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit24\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit25\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit26\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit27\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit28\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit29\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit30\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit31\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit32\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit33\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit34\\file.java,62,3,6,15,4,13,1,5,3\n'
            'File,commit35\\file.java,62,3,6,15,4,13,1,5,3\n'), "Il file non contiene i valori attesi"

    @pytest.mark.parametrize('setup_environment', [
        {'levels': 4, 'base_dir': BASE_DIR, 'files': {'file.txt': ''}}
    ], indirect=True)
    def test_case_17(self, setup_environment):
        self.main.run_software_metrics()
        file_path = os.path.join(self.BASE_DIR, "Software_Metrics", "mining_results_sm_final.csv")
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == (
            "Kind,Name,CountLineCode,CountDeclClass,CountDeclFunction,CountLineCodeDecl,SumEssential,SumCyclomaticStrict,MaxEssential,MaxCyclomaticStrict,MaxNesting\n"), "Il file non contiene solo l'header del CSV"
