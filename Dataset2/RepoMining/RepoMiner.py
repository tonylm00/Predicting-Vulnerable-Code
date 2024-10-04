import csv
import requests
import os
from pydriller import RepositoryMining


class RepoMiner:

    def __init__(self, base_dir):
        self.base_dir=base_dir


    def initialize_repo_mining(self, mini_dataset_name):

        dataset_divided_path = os.path.join(self.base_dir, "Dataset_Divided")

        repo_name = 'RepositoryMining' + str(mini_dataset_name)

        os.chdir(dataset_divided_path)
        name_dataset = str(mini_dataset_name) + '.csv'
        with open(name_dataset, mode='r') as csv_file:
            os.chdir("..")
            os.chdir("mining_results")
            if repo_name not in os.listdir():
                os.mkdir(repo_name)
            os.chdir(repo_name)
            csv_reader = csv.DictReader(csv_file)
            data = dict()
            i = 0
            for riga in csv_reader:
                data[i] = riga
                i += 1
            self.start_mining_repo(data, repo_name)
            os.chdir(self.base_dir)

    def start_mining_repo(self, data, repo_name):
        statusOK = "OK!\n"
        statusNE = "NOT EXIST COMMIT\n"
        statusNR = "REPO NOT AVAILABLE\n"
        statusVE = "VALUE ERROR! COMMIT HASH NOT EXISTS\n"
        file1 = open("CHECK.txt", "a")
        file2 = open("ERRORS.txt", "a")
        j = 0
        for line in data:
            link = data[line]['repo_url'] + '.git'
            # per chiamare la seconda api e controllare che il commit esiste
            link1 = data[line]['repo_url']
            commit_id = data[line]['commit_id']
            cve_id = data[line]['cve_id']
            status = ""
            toWrite = "indice: " + str(j + 1) + " link repo: " + str(link1) + " status: "
            response = requests.get(link)
            if response:
                response1 = requests.get(link1 + "/commit/" + commit_id)
                if response1:
                    try:
                        for commit in RepositoryMining(link, commit_id).traverse_commits():
                            for mod in commit.modifications:
                                print("MOD:", mod.filename)
                                if ".java" in mod.filename:
                                    if cve_id not in os.listdir():
                                        os.mkdir(cve_id)
                                    os.chdir(cve_id)
                                    if commit_id not in os.listdir():
                                        os.mkdir(commit_id)
                                    os.chdir(commit_id)
                                    if mod.source_code_before != None:
                                        javafile = open(mod.filename, "w+", encoding='utf-8')
                                        javafile.write(mod.source_code_before)
                                    os.chdir(os.path.join(self.base_dir, 'mining_results', repo_name))
                        status = statusOK
                        toWrite = toWrite + status
                        file1.write(toWrite)
                        j += 1
                    except ValueError:
                        status = statusVE
                        toWrite = toWrite + status
                        file1.write(toWrite)
                        file2.write(toWrite + "," + commit_id)
                        j += 1
                else:
                    print(statusNE)
                    status = statusNE
                    toWrite = toWrite + status
                    file1.write(toWrite)
                    j += 1
            else:
                print(statusNR)
                status = statusNR
                toWrite = toWrite + status
                file1.write(toWrite)
                j += 1
        file1.close()
        file2.close()










