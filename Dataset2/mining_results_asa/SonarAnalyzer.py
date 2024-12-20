import csv
import logging
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
    """

    def __init__(self, sonar_host, sonar_token, sonar_path, file_name, base_dir):
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
        self.base_dir = base_dir

        # logger separato per questa classe
        self.logger = logging.getLogger('SonarAnalyzerLogger')
        self.logger.setLevel(logging.ERROR)

        # handler per scrivere i log su file
        file_handler = logging.FileHandler(os.path.join(self.base_dir, "mining_results_asa", 'asa.log'))
        file_handler.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

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

        command = [
            f"{self.sonar_path}",  # Path to SonarScanner
            f"-Dsonar.projectKey={sonar_project_key}",  # Project key based on directory name
            f"-Dsonar.sources={sources_dir}",  # Absolute path to the source directory
            f"-Dsonar.host.url={self.sonar_host}",  # SonarQube server URL
            f"-Dsonar.token={self.sonar_token}",  # Authentication token
            f"-Dsonar.exclusions=**/*.txt, **/*.md, **/*.csv",  # Exclude non-source files
            f"-Dsonar.java.binaries={sources_dir}"
        ]

        try:
            result = subprocess.run(command, cwd=commit_dir, capture_output=True, text=True)

            if result.stderr:
                print(result.stderr)
                if "Unable to parse" in result.stderr:
                    self.logger.error(f"Project with CommitID: {commit_dir.split('/')[-1]} contains parsing errors.")
                    pass
                if "Connection refused" in result.stderr:
                    message = "SonarQube is not reported to be active. " \
                              "Remember to activate it and check if the host is correct."
                    self.logger.error(message)
                    raise Exception(message)
                if "Error status returned by url" in result.stderr:
                    message = "SonarQube Error. Check if the token entered is correct."
                    self.logger.error(message)
                    raise Exception(message)

        except FileNotFoundError:
            self.logger.error("SonarScanner not found.")
            raise Exception("SonarScanner not found.")

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
                self.logger.error(f"SonarQube error: Timeout reached for project analysis {project_key}.")
                return []

        url = f"{self.sonar_host}/api/issues/search?types=VULNERABILITY&components={project_key}"
        headers = {"Authorization": f"Bearer {self.sonar_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            self.logger.error(f"SonarQube error {response.status_code} for project {project_key}.")
            return []

        return response.json().get("issues", [])

    def save_issues_to_csv(self, issues, project):
        """
        Saves the list of issues to a CSV file. If no issues are found, records a placeholder entry.

        Args:
            issues (list): The list of issues (dictionaries) found in the project.

        Creates:
            A CSV file or appends the issues to an existing CSV file.
        """
        fieldnames = ["severity", "updateDate", "line", "rule", "project", "effort", "message", "creationDate", "type",
                      "component", "textRange", "debt", "key", "hash", "status"]
        file_exists = os.path.isfile(os.path.join(self.base_dir, self.output_csv))

        with open(os.path.join(self.base_dir, self.output_csv), mode="a", newline="\n") as file:
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
                        "status": issue.get("status", "")
                    })
            else:
                for file in os.listdir(project):
                    if file.endswith(".java"):
                        component = ':'.join(os.path.join(project, file).replace("\\", "/").split('/')[-4:])
                        writer.writerow({
                            "severity": "N/A",
                            "updateDate": "N/A",
                            "line": "N/A",
                            "rule": "N/A",
                            "project": "N/A",
                            "effort": "N/A",
                            "message": "N/A",
                            "creationDate": "N/A",
                            "type": "NO_ISSUES_FOUND",
                            "component": component,
                            "textRange": "N/A",
                            "debt": "N/A",
                            "key": "N/A",
                            "hash": "N/A",
                            "status": "N/A"
                        })

    def process_repositories(self):
        """
        Processes the repositories in the 'mining_results' folder, analyzes them using SonarQube, and saves the issues.
        The function iterates through different directories (repository, CVE, and commits) and performs analysis
        if the project key is not already in the CSV file.
        """

        for folder in os.listdir(os.path.join(self.base_dir, "mining_results")):
            if "RepositoryMining" in folder:
                repo_dir_path = os.path.join(self.base_dir, "mining_results", folder)
                for cve_id in os.listdir(repo_dir_path):
                    if cve_id == "CHECK.txt" or cve_id == "ERRORS.txt" or cve_id == ".DS_Store":
                        continue

                    cve_dir_path = os.path.join(self.base_dir, "mining_results", folder, cve_id)
                    if os.path.isdir(cve_dir_path):
                        for commit_id in os.listdir(cve_dir_path):
                            if commit_id == ".DS_Store":
                                continue

                            source_dir = os.path.join(self.base_dir, "mining_results", folder, cve_id, commit_id)
                            # RepositoryMiningX:Directory:commit
                            sonar_project_key = ':'.join(source_dir.split('\\')[-3:])

                            self.create_sonar_properties(sonar_project_key, source_dir)
                            self.run_sonar_scanner(sonar_project_key, source_dir)
                            try:
                                issues = self.get_project_issues(sonar_project_key)
                            except ConnectionError:
                                self.logger.error(f"Host unreachable: {self.sonar_host}")
                                raise Exception("Host unreachable")

                            self.save_issues_to_csv(issues, source_dir)
