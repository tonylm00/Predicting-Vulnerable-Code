import os

from Dataset2.Software_Metrics.MetricsWriter import MetricsWriter
from Dataset2.Software_Metrics.SoftwareMetrics import SoftwareMetrics

def runSoftwareMetrics():
    csv_file = os.path.abspath("../../Dataset2/Software_Metrics/metrics_results.csv")
    csv_writer = MetricsWriter(csv_file)
    csv_writer.write_header()
    # Crea il file CSV con l'header una volta sola, prima del ciclo for
    os.chdir("..")
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

if __name__ == '__main__':
    runSoftwareMetrics()