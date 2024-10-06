import os
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

def run_repo_mining():
	dataset_div = DatasetDivider(os.getcwd(), 'initial_Dataset.csv')
	dataset_div.divide_dataset()

	os.chdir('..')

	repo_miner = RepoMiner(os.getcwd())

	dataset_divided_path = os.path.join(os.getcwd(), "Dataset_Divided")
	num_repos = len(os.listdir(dataset_divided_path))
	print(num_repos)
	for count in range(1, num_repos + 1, 1):
		print("Starting file:")
		print(count)
		repo_miner.initialize_repo_mining(count)
		print("------------------")
		print("The file:")
		print(count)
		print(" is Ready!!!")
		print("------------------")

def run_text_mining():
    tm_dict = {}
    dict_java_files = {}
    cwd = os.getcwd()
    repo_name = "RepositoryMining"
    os.chdir(cwd + "/mining_results")

    for count in range(1, 36):
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

                                        file_cls = "pos"
                                        if count > 18:
                                            file_cls = "neg"

                                        dict_java_files[folder + "/" + java_file_name] = [dict, file_cls]
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



def run_software_metrics():
    csv_file = os.path.abspath("Software_Metrics/metrics_results_sm_final.csv")
    csv_writer = MetricsWriter(csv_file)
    csv_writer.write_header()
    # Crea il file CSV con l'header una volta sola, prima del ciclo for
    cwd = os.getcwd()
    repo_name = "RepositoryMining"
    os.chdir(cwd + "/mining_results")
    for count in range(1, 36, 1):
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
                                            file_cls = "pos"
                                            if count > 18:
                                                file_cls = "neg"
                                            csv_writer.write_metrics("File", java_file_path, metrics, file_cls)
                                os.chdir("..")
                        os.chdir("..")
                os.chdir("..")
    os.chdir("..")


def run_sonar_analyzer():
    sonar_analyzer = SonarAnalyzer(
        sonar_host="http://localhost:9000",
        sonar_token="squ_95089cde86a31904f6f2f0191e033099beb06c27",
        sonar_path=r"C:\Program Files\SonarScanner\bin\sonar-scanner.bat",
        file_name="mining_results_asa\RepositoryMining_ASAResults.csv"
    )
    sonar_analyzer.process_repositories()

def run_ASA():
    generator = DictGenerator("mining_results_asa\RepositoryMining_ASAResults.csv")
    rules = generator.generate_rules_dict()
    print(f"Rules: {rules}")

    vulnerability = generator.generate_vulnerability_dict()
    print(f"Vulnerability: {vulnerability}")

    creator = CsvCreatorForASA("mining_results_asa\csv_ASA_final.csv", rules, vulnerability)
    creator.create_csv()

def combine_tm_sm():
    combiner = DatasetCombiner("Union/Union_TM_SM.csv")
    tm_csv = "mining_results/csv_mining_final.csv"
    sm_csv = "Software_Metrics/mining_results_sm_final.csv"
    combiner.merge(tm_csv, sm_csv)


def combine_tm_asa():
    combiner = DatasetCombiner("Union/Union_TM_ASA.csv")
    tm_csv = "mining_results/csv_mining_final.csv"
    asa_csv = "mining_results_asa/csv_ASA_final.csv"
    combiner.merge(tm_csv, asa_csv)


def combine_sm_asa():
    combiner = DatasetCombiner("Union/Union_SM_ASA.csv")
    sm_csv = "Software_Metrics/mining_results_sm_final.csv"
    asa_csv = "mining_results_asa/csv_ASA_final.csv"
    combiner.merge(sm_csv, asa_csv)


def total_combination():
    combiner = DatasetCombiner("Union/3COMBINATION.csv")
    tm_csv = "mining_results/csv_mining_final.csv"
    sm_csv = "Software_Metrics/mining_results_sm_final.csv"
    asa_csv = "mining_results_asa/csv_ASA_final.csv"
    combiner.merge(sm_csv, tm_csv, asa_csv)


if __name__ == "__main__":
    run_repo_mining()
    run_text_mining()
    run_software_metrics()
    combine_tm_sm()
    #combine_sm_asa()
    #combine_tm_asa()
    #total_combination()