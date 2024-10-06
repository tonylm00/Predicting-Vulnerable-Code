import csv
import os
import subprocess
import time
import requests


class SonarAnalyzer:
    """
    SonarAnalyzer class that provides functionalities to analyze Java projects with SonarQube,
    collect the issues found, and store them in a CSV file.

    Attributes:
        sonar_host (str): The URL of the SonarQube server.
        sonar_token (str): The authentication token for the SonarQube server.
        sonar_path (str): The path to the SonarScanner executable.
        output_csv (str): The name of the output CSV file for storing issues.
        existing_project_keys (set): A set of project keys already analyzed and stored in the CSV.
    """

    def __init__(self, sonar_host, sonar_token, sonar_path, file_name):
        """
        Initializes the SonarAnalyzer class with the provided SonarQube server details.

        Args:
            sonar_host (str): The URL of the SonarQube server.
            sonar_token (str): The authentication token for SonarQube.
            sonar_path (str): The path to the SonarScanner executable.

        Attributes:
            self.output_csv (str): The name of the output CSV file.
            self.existing_project_keys (set): The project keys already saved in the output CSV.
        """
        self.sonar_host = sonar_host
        self.sonar_token = sonar_token
        self.sonar_path = sonar_path
        self.output_csv = file_name

    @staticmethod
    def create_sonar_properties(project_key, commit_dir):
        """
        Creates the sonar-project.properties file in the specified directory with SonarQube project details.

        Args:
            project_key (str): The unique SonarQube project key.
            commit_dir (str): The directory containing the project source code.
        """
        sonar_properties_content = f"""
        # Chiave univoca del progetto per SonarQube
        sonar.projectKey={project_key}

        # Nome del progetto che apparirà nell'interfaccia di SonarQube
        sonar.projectName={project_key}

        # Percorso delle sorgenti da analizzare
        sonar.sources={commit_dir}

        # Indica che il progetto è scritto in Java
        sonar.language=java

        # Disabilita l'integrazione con il sistema SCM (Git)
        sonar.scm.disabled=true

        # Escludi file .txt e altri tipi di file non rilevanti
        sonar.exclusions=**/*.txt, **/*.md, **/*.csv
        """
        with open(os.path.join(commit_dir, "sonar-project.properties"), "w") as f:
            f.write(sonar_properties_content)

    def run_sonar_scanner(self, sonar_project_key, commit_dir):
        """
        Runs the SonarScanner to analyze the source code in the specified directory.

        Args:
            sonar_project_key (str): The unique SonarQube project key.
            commit_dir (str): The directory containing the project source code.

        Raises:
            subprocess.CalledProcessError: If there is an error during the execution of the SonarScanner.
            FileNotFoundError: If the SonarScanner executable is not found.
        """
        sources_dir = os.path.abspath(commit_dir)
        if not os.path.exists(sources_dir):
            print(f"Errore: la directory {sources_dir} non esiste.")
            return

        command = [
            f"{self.sonar_path}",  # Path to SonarScanner
            f"-Dsonar.projectKey={sonar_project_key}",  # Project key based on directory name
            f"-Dsonar.sources={sources_dir}",  # Absolute path to the source directory
            f"-Dsonar.host.url={self.sonar_host}",  # SonarQube server URL
            f"-Dsonar.token={self.sonar_token}",  # Authentication token
            f"-Dsonar.issueTypes=VULNERABILITY",
            f"-Dsonar.exclusions=**/*.txt, **/*.md, **/*.csv",  # Exclude non-source files
            f"-Dsonar.java.binaries={sources_dir}"
        ]

        try:
            result = subprocess.run(command, cwd=commit_dir, capture_output=True, text=True)
            if result.stderr:
                print(f"Errore di SonarScanner: {result.returncode} - {result.stderr}")

        except subprocess.CalledProcessError as e:
            print(f"Errore durante l'esecuzione di SonarScanner: {e}")
            print(f"Output di errore: {e.stderr}")
        except FileNotFoundError as e:
            print(f"Errore: comando sonar-scanner non trovato: {e}")
        except Exception as e:
            print(f"Errore generico: {e}")

    def get_analysis_id(self, project_key):
        """
        Retrieves the analysis task ID for a given SonarQube project.

        Args:
            project_key (str): The unique SonarQube project key.

        Returns:
            str: The task ID of the current or most recent analysis, or None if no task is found.
        """
        url = f"{self.sonar_host}/api/ce/component?component={project_key}"
        headers = {"Authorization": f"Bearer {self.sonar_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Errore nel recuperare il task di analisi per il progetto: {response.status_code}")
            return None

        tasks = response.json().get("queue", [])
        if tasks:
            return tasks[0].get("id", None)

        current_task = response.json().get("current", {})
        if current_task and current_task.get("status") == "SUCCESS":
            return current_task.get("id", None)

        return None

    def check_analysis_status(self, analysis_id):
        """
        Checks the status of the analysis task in SonarQube.

        Args:
            analysis_id (str): The ID of the analysis task to check.

        Returns:
            str: The current status of the task (e.g., 'SUCCESS', 'FAILED'), or None if not found.
        """
        url = f"{self.sonar_host}/api/ce/task?id={analysis_id}"
        headers = {"Authorization": f"Bearer {self.sonar_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Errore nel recuperare lo stato dell'analisi: {response.status_code}")
            return None

        return response.json().get("task", {}).get("status", None)

    def wait_for_analysis_completion(self, analysis_id, timeout=600):
        """
        Waits for the analysis task to complete, with a timeout.

        Args:
            analysis_id (str): The ID of the analysis task.
            timeout (int): The maximum time to wait for the task to complete (in seconds).

        Returns:
            bool: True if the analysis completed successfully, False if it failed or timed out.
        """
        elapsed_time = 0
        wait_time = 0.5
        while elapsed_time < timeout:
            status = self.check_analysis_status(analysis_id)
            if status == "SUCCESS":
                return True
            elif status == "FAILED":
                return False
            else:
                time.sleep(wait_time)
                elapsed_time += wait_time

        print("Timeout raggiunto in attesa del completamento dell'analisi.")
        return False

    def get_project_issues(self, project_key):
        """
        Retrieves the list of issues for a SonarQube project after the analysis completes.

        Args:
            project_key (str): The unique SonarQube project key.

        Returns:
            list: A list of issues (as dictionaries) found in the project, or an empty list if no issues are found.
        """
        analysis_id = self.get_analysis_id(project_key)
        if analysis_id:
            success = self.wait_for_analysis_completion(analysis_id)
            if not success:
                print("L'analisi non è riuscita o non è stata completata nei tempi previsti.")
                return []

        url = f"{self.sonar_host}/api/issues/search?components={project_key}"
        headers = {"Authorization": f"Bearer {self.sonar_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Errore nell'ottenere le issue del progetto: {response.status_code}")
            return []

        return response.json().get("issues", [])

    def save_issues_to_csv(self, issues):
        """
        Saves the list of issues to a CSV file. If no issues are found, records a placeholder entry.

        Args:
            issues (list): The list of issues (dictionaries) found in the project.

        Creates:
            A CSV file or appends the issues to an existing CSV file.
        """
        fieldnames = ["severity", "updateDate", "line", "rule", "project", "effort", "message", "creationDate", "type",
                      "component", "textRange", "debt", "key", "hash", "status", "class"]
        file_exists = os.path.isfile(self.output_csv)

        with open(self.output_csv, mode="a", newline="\n") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
            if not file_exists:
                writer.writeheader()

            if issues:
                for issue in issues:
                    writer.writerow({
                        "severity": issue.get("severity", ""),
                        "updateDate": issue.get("updateDate", ""),
                        "line": issue.get("line", ""),
                        "rule": issue.get("rule", ""),
                        "project": issue.get("project", ""),
                        "effort": issue.get("effort", ""),
                        "message": issue.get("message", ""),
                        "creationDate": issue.get("creationDate", ""),
                        "type": issue.get("type", ""),
                        "component": issue.get("component", ""),
                        "textRange": str(issue.get("textRange", "")),
                        "debt": issue.get("debt", ""),
                        "key": issue.get("key", ""),
                        "hash": issue.get("hash", ""),
                        "status": issue.get("status", ""),
                        "class": self.get_project_class(issue.get("project", "").split(":")[-1])
                    })

    def process_repositories(self):
        """
        Processes the repositories in the 'mining_results' folder, analyzes them using SonarQube, and saves the issues.
        The function iterates through different directories (repository, CVE, and commits) and performs analysis
        if the project key is not already in the CSV file.
        """

        for folder in os.listdir("../mining_results"):
            if "RepositoryMining" in folder:
                for cve_id in os.listdir("../mining_results/" + folder):

                    if cve_id == "CHECK.txt" or cve_id == "ERRORS.txt" or cve_id == ".DS_Store":
                        continue

                    if os.path.isdir("../mining_results/" + folder + "/" + cve_id):
                        for commit_id in os.listdir("../mining_results/" + folder + "/" + cve_id):

                            if commit_id == ".DS_Store":
                                continue

                            source_dir = "../mining_results/" + folder + "/" + cve_id + "/" + commit_id

                            # RepositoryMiningX:Directory:commit
                            sonar_project_key = ':'.join(source_dir.split('/')[-3:])

                            self.create_sonar_properties(sonar_project_key, source_dir)
                            self.run_sonar_scanner(sonar_project_key, source_dir)
                            issues = self.get_project_issues(sonar_project_key)
                            print(f"Progetto: {sonar_project_key} - Trovate {len(issues)} issue(s).")
                            self.save_issues_to_csv(issues)

    @staticmethod
    def get_project_class(commit_id):
        """
        Retrieves the class associated with a specific commit_id from the dataset.

        Args:
            commit_id (str): The commit ID to search for in the dataset.

        Returns:
            str: The class associated with the commit ID, or 'Unknown' if not found.
        """
        try:
            with open("../initial_Dataset.csv", mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["commit_id"] == commit_id:
                        return row["cls"]
        except FileNotFoundError:
            print(f"Errore: il file initial_Dataset non è stato trovato.")
        except KeyError:
            print("Errore: il dataset non contiene la colonna 'commit_id' o 'class'.")

        return "Unknown"

