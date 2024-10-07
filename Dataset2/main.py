import os
import shutil
import zipfile

from Dataset2.AI_Module.RandomForest import predict_dict
from Dataset2.RepoMining.Dataset_Divider import DatasetDivider
from Dataset2.RepoMining.RepoMiner import RepoMiner
from Dataset2.Software_Metrics.MetricsWriter import MetricsWriter
from Dataset2.Software_Metrics.SoftwareMetrics import SoftwareMetrics
from Dataset2.Text_Mining.JavaTextMining import JavaTextMining
from Dataset2.Text_Mining.CSVWriter import CSVWriter
from Dataset2.Union.DatasetCombiner import DatasetCombiner
from Dataset2.mining_results_asa.CsvCreatorForAsa import CsvCreatorForASA
from Dataset2.mining_results_asa.DictGenerator import DictGenerator
from Dataset2.mining_results_asa.SonarAnalyzer import SonarAnalyzer

class Main():
    def run_repo_mining(self, dataset_name):
        os.chdir('..')
        dataset_div = DatasetDivider(os.getcwd(), dataset_name)
        dataset_div.divide_dataset()

        os.chdir('..')

        repo_miner = RepoMiner(os.getcwd())

        dataset_divided_path = os.path.join(os.getcwd(), "Dataset_Divided")
        num_repos = len(os.listdir(dataset_divided_path))
        for count in range(1, num_repos + 1, 1):
            print("Starting file:")
            print(count)
            repo_miner.initialize_repo_mining(count)
            print("------------------")
            print("The file:")
            print(count)
            print(" is Ready!!!")
            print("------------------")

    def run_text_mining(self):
        #os.chdir('..')
        tm_dict = {}
        dict_java_files = {}
        cwd = os.getcwd()
        dataset_divided_path = os.path.join(cwd, "Dataset_Divided")
        num_repos = len(os.listdir(dataset_divided_path))
        repo_name = "RepositoryMining"
        os.chdir(cwd + "/mining_results")

        for count in range(1, num_repos + 1, 1):
            if count != 18:
                repo = repo_name + str(count)
                if repo != ".DS_Store":
                    os.chdir(repo)

                    for cvd_id in os.listdir():
                        if cvd_id not in [".DS_Store", "CHECK.txt", "ERRORS.txt"]:
                            print(cvd_id)
                            os.chdir(cvd_id)
                            print(os.listdir())

                            for folder in os.listdir():
                                if folder != ".DS_Store":
                                    os.chdir(folder)

                                    for file in os.listdir():
                                        if file != ".DS_Store" and file.endswith(".java"):
                                            java_file_name = file
                                            analyzer = JavaTextMining(java_file_name)
                                            dict = analyzer.takeJavaClass()

                                            with open(java_file_name + "_text_mining.txt", "w+", encoding="utf-8") as file:
                                                file.write(str(dict))

                                            dict_java_files[folder + "\\" + java_file_name] = dict
                                            tm_dict = JavaTextMining.mergeDict(tm_dict, dict)

                                    os.chdir("..")  # Torna alla cartella principale del cvd_id

                            os.chdir("..")  # Torna alla cartella repo
                    os.chdir("..")  # Torna alla cartella mining_results

        with open("text_mining_dict.txt", "w+", encoding="utf-8") as file:
            file.write(str(tm_dict))

        split_dict = JavaTextMining.splitDict(tm_dict)
        with open("FilteredTextMining.txt", "w+", encoding="utf-8") as file:
            file.write(str(split_dict))

        csv_final = CSVWriter(split_dict, dict_java_files, "csv_mining_final.csv")
        csv_final.write_header()
        csv_final.write_rows()
        os.chdir("..")  # Torna alla cartella di lavoro principale


    def run_software_metrics(self):
        csv_file = os.path.abspath("Software_Metrics/metrics_results_sm_final.csv")
        csv_writer = MetricsWriter(csv_file)
        csv_writer.write_header()
        # Crea il file CSV con l'header una volta sola, prima del ciclo for
        cwd = os.getcwd()
        dataset_divided_path = os.path.join(cwd, "Dataset_Divided")
        num_repos = len(os.listdir(dataset_divided_path))
        repo_name = "RepositoryMining"
        os.chdir(cwd + "/mining_results")
        for count in range(1, num_repos + 1, 1):
            if count != 18:
                repo = repo_name + str(count)
                if repo != ".DS_Store":
                    os.chdir(repo)
                    for cvd_id in os.listdir():
                        if cvd_id not in [".DS_Store", "CHECK.txt", "ERRORS.txt"]:
                            os.chdir(cvd_id)
                            for folder in os.listdir():
                                if folder != ".DS_Store":
                                    os.chdir(folder)
                                    for file in os.listdir():
                                        if file != ".DS_Store":
                                            if file.endswith(".java"):
                                                java_file_path = os.path.join(folder, file)
                                                with open(file, "r", encoding='utf-8') as java_file:
                                                    file_content = java_file.read()
                                                analyzer = SoftwareMetrics(java_file_path, file_content)
                                                metrics = analyzer.analyze()
                                                csv_writer.write_metrics("File", java_file_path, metrics)
                                    os.chdir("..")
                            os.chdir("..")
                    os.chdir("..")
        os.chdir("..")


    def run_ASA(self, sonar_host, sonar_token, sonar_path):
        sonar_analyzer = SonarAnalyzer(
            sonar_host=sonar_host,
            sonar_token=sonar_token,
            sonar_path=sonar_path,
            file_name="mining_results_asa/RepositoryMining_ASAResults.csv"
        )
        sonar_analyzer.process_repositories()

        generator = DictGenerator("mining_results_asa/RepositoryMining_ASAResults.csv")
        rules = generator.generate_rules_dict()
        print(f"Rules: {rules}")

        vulnerability = generator.generate_vulnerability_dict()
        print(f"Vulnerability: {vulnerability}")

        creator = CsvCreatorForASA("mining_results_asa/csv_ASA_final.csv", rules, vulnerability)
        creator.create_csv()

    def combine_tm_sm(self):
        combiner = DatasetCombiner("Union/Union_TM_SM.csv")
        tm_csv = "mining_results/csv_mining_final.csv"
        sm_csv = "Software_Metrics/metrics_results_sm_final.csv"
        combiner.merge(tm_csv, sm_csv)


    def combine_tm_asa(self):
        combiner = DatasetCombiner("Union/Union_TM_ASA.csv")
        tm_csv = "mining_results/csv_mining_final.csv"
        asa_csv = "mining_results_asa/csv_ASA_final.csv"
        combiner.merge(tm_csv, asa_csv)


    def combine_sm_asa(self):
        combiner = DatasetCombiner("Union/Union_SM_ASA.csv")
        sm_csv = "Software_Metrics/metrics_results_sm_final.csv"
        asa_csv = "mining_results_asa/csv_ASA_final.csv"
        combiner.merge(sm_csv, asa_csv)


    def total_combination(self):
        combiner = DatasetCombiner("Union/3COMBINATION.csv")
        tm_csv = "mining_results/csv_mining_final.csv"
        sm_csv = "Software_Metrics/metrics_results_sm_final.csv"
        asa_csv = "mining_results_asa/csv_ASA_final.csv"
        combiner.merge(sm_csv, tm_csv, asa_csv)

    def download_analysis_results(self, file_type, saving_path):
        path_to_TM = os.path.join("mining_results", "csv_mining_final.csv")
        path_to_SM = os.path.join("Software_Metrics", "metrics_results_sm_final.csv")
        path_to_ASA = os.path.join("mining_results_asa", "csv_ASA_final.csv")

        file_map = {'text_mining': path_to_TM,
                    'software_metrics': path_to_SM,
                    'asa': path_to_ASA}

        file_path = file_map[file_type]

        if file_path:
            shutil.copyfile(file_path, saving_path)

    def download_results(self, results_type, path_to_save):
        file_paths = []
        tm = results_type['text_mining']
        sm = results_type['software_metrics']
        asa = results_type['asa']

        if tm:
            path_to_results_TM = os.path.join("Predict", "Predict_TM.csv")
            file_paths.append(path_to_results_TM)

        if sm:
            path_to_results_SM = os.path.join("Predict", "Predict_SM.csv")
            file_paths.append(path_to_results_SM)

        if asa:
            path_to_results_ASA = os.path.join("Predict", "Predict_ASA.csv")
            file_paths.append(path_to_results_ASA)

        if tm and sm and asa:
            path_to_results_3_comb = os.path.join("Predict", "Predict_3Combination.csv")
            file_paths.append(path_to_results_3_comb)
        elif tm and sm:
            path_to_results_TM_SM = os.path.join("Predict", "Predict_TMSM.csv")
            file_paths.append(path_to_results_TM_SM)
        elif tm and asa:
            path_to_results_TM_ASA = os.path.join("Predict", "Predict_TMASA.csv")
            file_paths.append(path_to_results_TM_ASA)
        else:
            path_to_results_SM_ASA = os.path.join("Predict", "Predict_SMASA.csv")
            file_paths.append(path_to_results_SM_ASA)


        with zipfile.ZipFile(path_to_save, 'w') as zipf:
            for file in file_paths:
                zipf.write(file, os.path.basename(file))  # Add each file to the zip
        print(f"ZIP file created: {path_to_save}")