import os
import shutil
import csv
import requests
from git import GitCommandError
from requests.exceptions import MissingSchema
from requests.exceptions import ConnectionError
from pydriller import RepositoryMining
import logging




class RepoMiner:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.index = 0
        self.mining_result_path = os.path.join(base_dir, 'mining_results')
        self.logger = logging.getLogger('Dataset2.RepoMining.RepoMiner')
        self.logger.setLevel(logging.INFO)


    def initialize_repo_mining(self, mini_dataset_name):
        dataset_divided_path = os.path.join(self.base_dir, "Dataset_Divided")
        repo_name = 'RepositoryMining' + str(mini_dataset_name)
        mining_results_path = os.path.join(self.base_dir, 'mining_results')

        # Percorso del dataset
        name_dataset = os.path.join(dataset_divided_path, str(mini_dataset_name) + '.csv')

        # Legge il CSV
        with open(name_dataset, mode='r') as csv_file:
            # Se esiste già la cartella mining_results, la elimina e la ricrea

            os.makedirs(self.mining_result_path, exist_ok=True)

            expected_headers = ['cve_id', 'repo_url', 'commit_id']

            # Legge i dati dal CSV
            csv_reader = csv.DictReader(csv_file)
            dataset_headers = csv_reader.fieldnames
            if dataset_headers == expected_headers:
                repo_path = os.path.join(mining_results_path, repo_name)
                if not os.path.exists(repo_path):
                    os.mkdir(repo_path)

                data = {}
                i = 0
                for riga in csv_reader:
                    data[i] = riga
                    i += 1

                # Avvia il mining del repository
                self.start_mining_repo(data, repo_path)
            else:
                print(dataset_headers)
                print(expected_headers)
                raise ValueError("Not valid dataset headers")


    def start_mining_repo(self, data, repo_path):
        statusOK = "OK!"
        statusNE = "NOT EXIST COMMIT"
        statusNR = "REPO NOT AVAILABLE"
        statusVE = "VALUE ERROR! COMMIT HASH NOT EXISTS"
        statusGCE = "GIT COMMAND ERROR"
        statusMS = 'INVALID URL'
        statusCE = 'CONNECTION ERROR'

        print("CIAO LOG")

        logging.basicConfig(filename=os.path.join(self.mining_result_path, 'repo_mining.log'), level=logging.CRITICAL,
                            format='%(levelname)s:%(message)s', force=True)

        for line in data:
            link = data[line]['repo_url'] + '.git'
            link1 = data[line]['repo_url']
            commit_id = data[line]['commit_id']
            cve_id = data[line]['cve_id']
            status = ""
            toWrite = f"indice: {self.index + 1} link repo: {link1} status: "

            try:
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
                            self.logger.info(toWrite)
                            self.index+= 1
                        except ValueError:
                            status = statusVE
                            toWrite += status
                            self.logger.error(toWrite + "," + commit_id)
                            self.index+= 1
                        except GitCommandError:
                            status = statusGCE
                            toWrite += status
                            self.logger.error(toWrite + "," + commit_id)
                            self.index+= 1

                    else:
                        status = statusNE
                        toWrite += status
                        self.logger.error(toWrite)
                        self.index+= 1
                else:
                    status = statusNR
                    toWrite += status
                    self.logger.error(toWrite)
                    self.index+= 1
            except MissingSchema:
                status = statusMS
                toWrite += status
                self.logger.error(toWrite)
                self.index += 1

            except ConnectionError:
                status = statusCE
                toWrite += status
                self.logger.error(toWrite)
                self.index += 1



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
                        print(mod.source_code_before)
                        javafile.write(mod.source_code_before)

