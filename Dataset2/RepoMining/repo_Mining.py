import csv
import requests
import os
from pydriller import RepositoryMining
from git import GitCommandError


import tempfile
""""
Execution of the repository mining from the initial_Dataset.csv with pyDriller.
This script takes all tha java classes that are declared as Vulnerable or not.
The aim is to take the Before Image of the commit that fixes the vulnerability.
"""

'''
@Param miniDatasetName : name of the mini dataset created from the script divide_Dataset.py
1. Collect the commits in a python dict and call the function StartMiningRepo.
'''
def initialize(miniDatasetName):
    # Determina la directory base del progetto, rimuovendo "RepoMining" dal percorso corrente del file

    print("CWD-initialize:", os.getcwd())

    cwd = os.getcwd()

    index = cwd.index('RepoMining') + len('RepoMining')
    base_dir = cwd[:index]
    # print(f"Base_dir: {base_dir}")
    print("base-dir:", base_dir)


    # Costruisce i percorsi per le directory dei dataset divisi e dei risultati del mining
    dataset_divided_dir = os.path.join(base_dir, "Dataset_Divided")
    print("dataset_divided_dir:", dataset_divided_dir)
    # print(f"dataset_divided_dir: {dataset_divided_dir}")

    mining_results_dir = os.path.join(base_dir, "mining_results")

    # print(f"mining_results_dir: {mining_results_dir}")
    repoName = 'RepositoryMining'+str(miniDatasetName)
    os.chdir(dataset_divided_dir)
    name_dataset = str(miniDatasetName)+'.csv'
    with open(name_dataset, mode='r') as csv_file:
            os.chdir("..")
            os.chdir("mining_results")
            print("OS-INITIALIZE:", os.listdir())
            if repoName not in os.listdir():
                os.mkdir(repoName)
            print("OS-INITIALIZE-POST:", os.listdir())
            os.chdir(repoName)
            csv_reader = csv.DictReader(csv_file)
            first = 0
            data = dict()
            i = 0
            for riga in csv_reader:
                data[i]=riga
                i+=1
            startMiningRepo(data, mining_results_dir, repoName)
            os.chdir(base_dir)
'''
@Param data: the line that contains the commits.
@Param cwd: the current directory.
@Param repoName: the name of the destination repo folder.
Check the existence of the Repository and the commit with API.
For each commit, takes all the before images and create the java files that are modified with pyDriller.
Create the resulting ERROR, CHECK files that contins the different status of each commit.
'''
def startMiningRepo(data, cwd, repoName):
    statusOK = "OK!\n"
    statusNE = "NOT EXIST COMMIT\n"
    statusNR = "REPO NOT AVAILABLE\n"
    statusVE = "VALUE ERROR! COMMIT HASH NOT EXISTS\n"
    statusG = "GIT COMMAND ERROR\n"
    file1 = open("CHECK.txt", "a")
    file2 = open("ERRORS.txt","a")
    j = 0
    for line in data:
        link=data[line]['repo_url']+'.git'
        #per chiamare la seconda api e controllare che il commit esiste
        link1=data[line]['repo_url']
        commit_id=data[line]['commit_id']
        cve_id=data[line]['cve_id']
        print(link)
        print(commit_id)
        status = ""
        toWrite = "indice: " + str(j+1) + " link repo: " + str(link1) + " status: "
        response = requests.get(link)
        if response:
            response1 = requests.get(link1+"/commit/"+commit_id)
            if response1:
                try:
                    for commit in RepositoryMining(link, commit_id).traverse_commits():
                       for mod in commit.modifications:
                          if ".java" in mod.filename:
                             if cve_id not in os.listdir():
                                 os.mkdir(cve_id)
                             os.chdir(cve_id)
                             if commit_id not in os.listdir():
                                os.mkdir(commit_id)
                             os.chdir(commit_id)
                             if mod.source_code_before != None:
                                javafile=open(mod.filename,"w+")
                                javafile.write(mod.source_code_before)
                             print("I AM HERE")
                             print(cwd+"/"+repoName)
                             os.chdir(cwd+"/"+repoName)
                             print(os.getcwd())
                    status = statusOK
                    toWrite = toWrite + status
                    file1.write(toWrite)
                    j+=1
                except ValueError:
                    print("ValueError:SHA for commit not defined ")
                    status= statusVE
                    toWrite = toWrite +status
                    file1.write(toWrite)
                    file2.write(toWrite+","+commit_id)
                    j+=1
                except GitCommandError:
                    # Gestione di errori generici, come problemi di rete o errori di lettura/scrittura
                    print("GitCommandError")
                    status = statusG
                    toWrite = toWrite + status
                    file1.write(toWrite)
                    file2.write(toWrite + "," + commit_id)
                    j += 1

            else:
                print(statusNE)
                status = statusNE
                toWrite = toWrite + status
                file1.write(toWrite)
                j+=1    
        else:
            print(statusNR)
            status = statusNR
            toWrite = toWrite + status
            file1.write(toWrite)
            j+=1
    file1.close()
    file2.close()
def main():
    initialize()
if __name__ == '__main__':
    main()