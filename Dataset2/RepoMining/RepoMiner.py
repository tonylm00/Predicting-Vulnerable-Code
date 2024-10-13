import os
import shutil
import csv
import requests
from pydriller import RepositoryMining


class RepoMiner:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def initialize_repo_mining(self, mini_dataset_name):
        dataset_divided_path = os.path.join(self.base_dir, "Dataset_Divided")
        repo_name = 'RepositoryMining' + str(mini_dataset_name)
        mining_results_path = os.path.join(self.base_dir, 'mining_results')

        # Percorso del dataset
        name_dataset = os.path.join(dataset_divided_path, str(mini_dataset_name) + '.csv')

        # Legge il CSV
        with open(name_dataset, mode='r') as csv_file:
            # Se esiste già la cartella mining_results, la elimina e la ricrea
            if os.path.exists(mining_results_path):
                shutil.rmtree(mining_results_path)
            os.makedirs(mining_results_path)

            repo_path = os.path.join(mining_results_path, repo_name)
            if not os.path.exists(repo_path):
                os.mkdir(repo_path)

            # Legge i dati dal CSV
            csv_reader = csv.DictReader(csv_file)
            data = {}
            i = 0
            for riga in csv_reader:
                data[i] = riga
                i += 1

            # Avvia il mining del repository
            self.start_mining_repo(data, repo_path)

    def start_mining_repo(self, data, repo_path):
        statusOK = "OK!\n"
        statusNE = "NOT EXIST COMMIT\n"
        statusNR = "REPO NOT AVAILABLE\n"
        statusVE = "VALUE ERROR! COMMIT HASH NOT EXISTS\n"

        # File di log
        check_file_path = os.path.join(repo_path, "CHECK.txt")
        errors_file_path = os.path.join(repo_path, "ERRORS.txt")
        file1 = open(check_file_path, "a")
        file2 = open(errors_file_path, "a")

        j = 0
        for line in data:
            link = data[line]['repo_url'] + '.git'
            link1 = data[line]['repo_url']
            commit_id = data[line]['commit_id']
            cve_id = data[line]['cve_id']
            status = ""
            toWrite = f"indice: {j + 1} link repo: {link1} status: "

            response = requests.get(link)
            if response.ok:
                response1 = requests.get(f"{link1}/commit/{commit_id}")
                if response1.ok:
                    try:
                        for commit in RepositoryMining(link, commit_id).traverse_commits():
                            cve_path = os.path.join(repo_path, cve_id)
                            commit_path = os.path.join(cve_path, commit_id)
                            self.analyze_commit(commit, cve_path, commit_path)

                        status = statusOK
                        toWrite += status
                        file1.write(toWrite)
                        j += 1
                    except ValueError:
                        status = statusVE
                        toWrite += status
                        file1.write(toWrite)
                        file2.write(toWrite + "," + commit_id + "\n")
                        j += 1
                else:
                    status = statusNE
                    toWrite += status
                    file1.write(toWrite)
                    j += 1
            else:
                status = statusNR
                toWrite += status
                file1.write(toWrite)
                j += 1

        file1.close()
        file2.close()

    def analyze_commit(self, commit, cve_path, commit_path):
        for mod in commit.modifications:
            print("MOD:", mod.filename)
            if ".java" in mod.filename:

                # Creazione directory CVE e commit
                if not os.path.exists(cve_path):
                    os.mkdir(cve_path)
                if not os.path.exists(commit_path):
                    os.mkdir(commit_path)

                # Scrive il file Java se esiste il codice sorgente prima del commit
                if mod.source_code_before is not None:
                    java_file_path = os.path.join(commit_path, mod.filename)
                    with open(java_file_path, "w+", encoding='utf-8') as javafile:
                        javafile.write(mod.source_code_before)

