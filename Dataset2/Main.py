import os
import shutil
import zipfile
import joblib
import pandas as pd
from Dataset2.RepoMining.DatasetDivider import DatasetDivider
from Dataset2.RepoMining.RepoMiner import RepoMiner
from Dataset2.Software_Metrics.MetricsWriter import MetricsWriter
from Dataset2.Software_Metrics.SoftwareMetrics import SoftwareMetrics
from Dataset2.Text_Mining.JavaTextMining import JavaTextMining
from Dataset2.Text_Mining.CSVWriter import CSVWriter
from Dataset2.Union.DatasetCombiner import DatasetCombiner
from Dataset2.mining_results_asa.CsvCreatorForAsa import CsvCreatorForASA
from Dataset2.mining_results_asa.DictGenerator import DictGenerator
from Dataset2.mining_results_asa.SonarAnalyzer import SonarAnalyzer


class Main:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def run_repo_mining(self, dataset_name):
        dataset_div = DatasetDivider(self.base_dir, dataset_name)
        dataset_div.divide_dataset()

        repo_miner = RepoMiner(self.base_dir)

        dataset_divided_path = os.path.join(self.base_dir, "Dataset_Divided")
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
        tm_dict = {}
        dict_java_files = {}

        # Definisco i percorsi relativi in base a base_dir
        dataset_divided_path = os.path.join(self.base_dir, "Dataset_Divided")
        mining_results_path = os.path.join(self.base_dir, "mining_results")

        # Conta il numero di repository
        num_repos = len(os.listdir(dataset_divided_path))
        repo_name = "RepositoryMining"

        for count in range(1, num_repos + 1, 1):
            repo = repo_name + str(count)
            repo_path = os.path.join(mining_results_path, repo)

            if os.path.isdir(repo_path):  # Controlla che sia una directory valida
                for cvd_id in os.listdir(repo_path):
                    cvd_id_path = os.path.join(repo_path, cvd_id)

                    if cvd_id not in [".DS_Store", "CHECK.txt", "ERRORS.txt"] and os.path.isdir(cvd_id_path):

                        for folder in os.listdir(cvd_id_path):
                            folder_path = os.path.join(cvd_id_path, folder)

                            if folder != ".DS_Store" and os.path.isdir(folder_path):
                                for file in os.listdir(folder_path):
                                    if file != ".DS_Store" and file.endswith(".java"):
                                        java_file_path = os.path.join(folder_path, file)
                                        analyzer = JavaTextMining(java_file_path)
                                        dict = analyzer.takeJavaClass()
                                        # Salva i risultati del text mining
                                        text_mining_file_path = java_file_path + "_text_mining.txt"
                                        with open(text_mining_file_path, "w+", encoding="utf-8") as java_file:
                                            java_file.write(str(dict))

                                        dict_java_files[os.path.join(folder, file)] = dict
                                        tm_dict = JavaTextMining.mergeDict(tm_dict, dict)

        # Salva il dizionario finale del text mining
        text_mining_dict_path = os.path.join(mining_results_path, "text_mining_dict.txt")
        with open(text_mining_dict_path, "w+", encoding="utf-8") as java_file:
            java_file.write(str(tm_dict))

        # Divide il dizionario
        split_dict = JavaTextMining.splitDict(tm_dict)

        # Salva il dizionario filtrato del text mining
        filtered_text_mining_path = os.path.join(mining_results_path, "FilteredTextMining.txt")
        with open(filtered_text_mining_path, "w+", encoding="utf-8") as java_file:
            java_file.write(str(split_dict))

        # Scrivi il file CSV
        csv_file_path = os.path.join(mining_results_path, "csv_mining_final.csv")
        csv_final = CSVWriter(split_dict, dict_java_files, csv_file_path)
        csv_final.write_header()
        csv_final.write_rows()

    def run_software_metrics(self):
        # Percorso assoluto per il file CSV
        csv_file = os.path.join(self.base_dir, "Software_Metrics", "mining_results_sm_final.csv")
        csv_writer = MetricsWriter(csv_file)
        csv_writer.write_header()  # Scrive l'header una volta sola

        # Percorsi per dataset e risultati mining
        dataset_divided_path = os.path.join(self.base_dir, "Dataset_Divided")
        mining_results_path = os.path.join(self.base_dir, "mining_results")

        # Numero di repository
        num_repos = len(os.listdir(dataset_divided_path))
        repo_name = "RepositoryMining"

        for count in range(1, num_repos + 1, 1):
            repo = repo_name + str(count)
            repo_path = os.path.join(mining_results_path, repo)

            if os.path.isdir(repo_path):  # Verifica se è una directory valida
                for cvd_id in os.listdir(repo_path):
                    cvd_id_path = os.path.join(repo_path, cvd_id)

                    if cvd_id not in [".DS_Store", "CHECK.txt", "ERRORS.txt"] and os.path.isdir(cvd_id_path):
                        for folder in os.listdir(cvd_id_path):
                            folder_path = os.path.join(cvd_id_path, folder)

                            if folder != ".DS_Store" and os.path.isdir(folder_path):
                                for file in os.listdir(folder_path):

                                    if file != ".DS_Store" and file.endswith(".java"):
                                        java_file_path = os.path.join(folder_path, file)
                                        # Legge il contenuto del file .java
                                        with open(java_file_path, "r", encoding='utf-8') as java_file:
                                            file_content = java_file.read()

                                        # Analizza le metriche
                                        analyzer = SoftwareMetrics(self.base_dir, os.path.join(folder, file),
                                                                   file_content)
                                        metrics = analyzer.analyze()

                                        # Scrive i risultati delle metriche nel CSV
                                        csv_writer.write_metrics("File", os.path.join(folder, file), metrics)

    def run_ASA(self, sonar_host, sonar_token, sonar_path):
        sonar_analyzer = SonarAnalyzer(
            sonar_host=sonar_host,
            sonar_token=sonar_token,
            sonar_path=sonar_path,
            file_name="mining_results_asa\RepositoryMining_ASAResults.csv",
            base_dir=self.base_dir
        )
        sonar_analyzer.process_repositories()
        asa_result_path = os.path.join(self.base_dir, "mining_results_asa", "RepositoryMining_ASAResults.csv")
        generator = DictGenerator(asa_result_path)

        if os.path.exists(asa_result_path):

            rules = generator.generate_rules_dict()
            vulnerability = generator.generate_vulnerability_dict()
            creator = CsvCreatorForASA(os.path.join(self.base_dir, "mining_results_asa", "csv_ASA_final.csv"), rules,
                                       vulnerability)
            creator.create_csv()
        else:
            with open(os.path.join(self.base_dir, "mining_results_asa", "csv_ASA_final.csv"), 'w') as file:
                file.write("Name\n")

    def combine_tm_sm(self):
        combiner = DatasetCombiner(os.path.join(self.base_dir, "Union", "Union_TM_SM.csv"))
        tm_csv = os.path.join(self.base_dir, "mining_results", "csv_mining_final.csv")
        sm_csv = os.path.join(self.base_dir, "Software_Metrics", "mining_results_sm_final.csv")
        combiner.merge(tm_csv, sm_csv)

    def combine_tm_asa(self):
        combiner = DatasetCombiner(os.path.join(self.base_dir, "Union", "Union_TM_ASA.csv"))
        tm_csv = os.path.join(self.base_dir, "mining_results", "csv_mining_final.csv")
        asa_csv = os.path.join(self.base_dir, "mining_results_asa", "csv_ASA_final.csv")
        combiner.merge(tm_csv, asa_csv)

    def combine_sm_asa(self):
        combiner = DatasetCombiner(os.path.join(self.base_dir, "Union", "Union_SM_ASA.csv"))
        sm_csv = os.path.join(self.base_dir, "Software_Metrics", "mining_results_sm_final.csv")
        asa_csv = os.path.join(self.base_dir, "mining_results_asa", "csv_ASA_final.csv")
        combiner.merge(sm_csv, asa_csv)

    def total_combination(self):
        combiner = DatasetCombiner(os.path.join(self.base_dir, "Union", "3COMBINATION.csv"))
        tm_csv = os.path.join(self.base_dir, "mining_results", "csv_mining_final.csv")
        sm_csv = os.path.join(self.base_dir, "Software_Metrics", "mining_results_sm_final.csv")
        asa_csv = os.path.join(self.base_dir, "mining_results_asa", "csv_ASA_final.csv")
        combiner.merge(sm_csv, tm_csv, asa_csv)

    def run_prediction(self, input_csv_path, model_path, label_encoder_path, vocab_path, path_csv):
        original_vocab = joblib.load(vocab_path)
        model = joblib.load(model_path)
        label_encoder = joblib.load(label_encoder_path)

        df_new = pd.read_csv(input_csv_path)

        if len(df_new) == 0:
            return []

        aligned_data = pd.DataFrame(0, index=df_new.index, columns=original_vocab)

        # Fill the aligned DataFrame with the values from df_new where the column names match
        for column in df_new.columns:
            if column in original_vocab:
                aligned_data[column] = df_new[column]

        X_new = aligned_data.to_numpy()

        # Make predictions for all rows
        predictions = model.predict(X_new)

        # Riconverti la predizione in pos o neg
        predicted_classes = label_encoder.inverse_transform(predictions)

        df = pd.DataFrame({'Name': df_new['Name'], 'CLS': predicted_classes})
        os.makedirs(os.path.dirname(path_csv), exist_ok=True)
        df.to_csv(path_csv, index=False)

        return predicted_classes.tolist()

    def download_results(self, result_kind, results_type, path_to_save):
        file_paths = []
        tm = results_type['text_mining']
        sm = results_type['software_metrics']
        asa = results_type['asa']

        is_prediction = result_kind == 'prediction'

        if is_prediction:
            path_to_results_TM = os.path.join(self.base_dir, "Predict", "Predict_TM.csv")
            path_to_results_SM = os.path.join(self.base_dir, "Predict", "Predict_SM.csv")
            path_to_results_ASA = os.path.join(self.base_dir, "Predict", "Predict_ASA.csv")
            path_to_results_3_comb = os.path.join(self.base_dir, "Predict", "Predict_3Combination.csv")
            path_to_results_TM_SM = os.path.join(self.base_dir, "Predict", "Predict_TMSM.csv")
            path_to_results_TM_ASA = os.path.join(self.base_dir, "Predict", "Predict_TMASA.csv")
            path_to_results_SM_ASA = os.path.join(self.base_dir, "Predict", "Predict_SMASA.csv")
        else:
            path_to_results_TM = os.path.join(self.base_dir, "mining_results", "csv_mining_final.csv")
            path_to_results_SM = os.path.join(self.base_dir, "Software_Metrics", "mining_results_sm_final.csv")
            path_to_results_ASA = os.path.join(self.base_dir, "mining_results_asa", "csv_ASA_final.csv")
            path_to_results_3_comb = os.path.join(self.base_dir, "Union", "3Combination.csv")
            path_to_results_TM_SM = os.path.join(self.base_dir, "Union", "Union_TM_SM.csv")
            path_to_results_TM_ASA = os.path.join(self.base_dir, "Union", "Union_TM_ASA.csv")
            path_to_results_SM_ASA = os.path.join(self.base_dir, "Union", "Union_SM_ASA.csv")
            path_to_log_SM = os.path.join(self.base_dir, "Software_Metrics", "software_metrics.log")
            path_to_log_ASA = os.path.join(self.base_dir, "mining_results_asa", "asa.log")
            path_to_log_repo = os.path.join(self.base_dir, "mining_results", "repo_mining.log")
            if os.path.isfile(path_to_log_SM):
                file_paths.append(path_to_log_SM)

            if os.path.isfile(path_to_log_ASA):
                file_paths.append(path_to_log_ASA)

            if os.path.isfile(path_to_log_repo):
                file_paths.append(path_to_log_repo)

        if tm:
            if os.path.isfile(path_to_results_TM):
                file_paths.append(path_to_results_TM)

        if sm:
            if os.path.isfile(path_to_results_SM):
                file_paths.append(path_to_results_SM)

        if asa:
            if os.path.isfile(path_to_results_ASA):
                file_paths.append(path_to_results_ASA)

        if tm and sm and asa:
            if os.path.isfile(path_to_results_3_comb):
                file_paths.append(path_to_results_3_comb)

        if tm and sm:
            if os.path.isfile(path_to_results_TM_SM):
                file_paths.append(path_to_results_TM_SM)

        if tm and asa:
            if os.path.isfile(path_to_results_TM_ASA):
                file_paths.append(path_to_results_TM_ASA)

        if sm and asa:
            if os.path.isfile(path_to_results_SM_ASA):
                file_paths.append(path_to_results_SM_ASA)

        with zipfile.ZipFile(path_to_save, 'w') as zipf:
            for file in file_paths:
                zipf.write(file, os.path.basename(file))
        print(f"ZIP file created: {path_to_save}")
        return file_paths.__len__()

    def clean_up(self):
        print("Cleaning up...")

        if os.path.isdir(os.path.join(self.base_dir, "mining_results")):
            print("Removing mining_results...")
            shutil.rmtree(os.path.join(self.base_dir, "mining_results"))

        if os.path.isdir(os.path.join(self.base_dir, "Dataset_Divided")):
            print("Removing Dataset_Divided...")
            shutil.rmtree(os.path.join(self.base_dir, "Dataset_Divided"))

        if os.path.isdir(os.path.join(self.base_dir, "Predict")):
            print("Removing Predict...")
            shutil.rmtree(os.path.join(self.base_dir, "Predict"))

        if os.path.isfile(os.path.join(self.base_dir, "mining_results_asa", "RepositoryMining_ASAResults.csv")):
            print("Removing ASA...")
            os.remove(os.path.join(self.base_dir, "mining_results_asa", "RepositoryMining_ASAResults.csv"))

        if os.path.isfile(os.path.join(self.base_dir, "mining_results_asa", "csv_ASA_final.csv")):
            print("Removing ASA...")
            os.remove(os.path.join(self.base_dir, "mining_results_asa", "csv_ASA_final.csv"))

        if os.path.isfile(os.path.join(self.base_dir, "Software_Metrics", "mining_results_sm_final.csv")):
            print("Removing SM...")
            os.remove(os.path.join(self.base_dir, "Software_Metrics", "mining_results_sm_final.csv"))

        if os.path.isfile(os.path.join(self.base_dir, "Union", "3Combination.csv")):
            print("Removing 3Combination.csv...")
            os.remove(os.path.join(self.base_dir, "Union", "3Combination.csv"))

        if os.path.isfile(os.path.join(self.base_dir, "Union", "Union_TM_SM.csv")):
            print("Removing Union_TM_SM.csv...")
            os.remove(os.path.join(self.base_dir, "Union", "Union_TM_SM.csv"))

        if os.path.isfile(os.path.join(self.base_dir, "Union", "Union_TM_ASA.csv")):
            print("Removing Union_TM_ASA.csv...")
            os.remove(os.path.join(self.base_dir, "Union", "Union_TM_ASA.csv"))

        if os.path.isfile(os.path.join(self.base_dir, "Union", "Union_SM_ASA.csv")):
            print("Removing Union_SM_ASA.csv...")
            os.remove(os.path.join(self.base_dir, "Union", "Union_SM_ASA.csv"))

        if os.path.isfile(os.path.join(self.base_dir, "repository.csv")):
            os.remove(os.path.join(self.base_dir, "repository.csv"))

        if os.path.isfile(os.path.join(self.base_dir, "Software_Metrics", "software_metrics.log")):
            os.remove(os.path.join(self.base_dir, "Software_Metrics", "software_metrics.log"))

        if os.path.isfile(os.path.join(self.base_dir, "mining_results_asa", "asa.log")):
            os.remove(os.path.join(self.base_dir, "mining_results_asa", "asa.log"))

        if os.path.isfile(os.path.join(self.base_dir, "mining_results", "repo_mining.log")):
            os.remove(os.path.join(self.base_dir, "mining_results", "repo_mining.log"))

        print("Clean up completed.")
