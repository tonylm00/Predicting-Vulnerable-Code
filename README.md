# Perseverance
![logo](https://i.postimg.cc/hjPdPZRz/PERSEVERANCE-removebg-preview.png)

Perseverance is a tool developed in Python for analyzing repositories using Pydriller. It works with a dataset of open-source projects labeled as vulnerable or non-vulnerable. The tool extracts three distinct data models from Java code preceding vulnerability-fixing commits:

- **Text Mining**: Creates a dictionary containing keywords found in the file and their frequency within it.
- **Software Metrics**: Uses the tool Understand to calculate nine different metrics assessing the complexity of the file.
- **Static Analysis**: Uses SonarQube to identify vulnerabilities in the file, referring to applicable Java rules.
These models are used to train and evaluate various machine learning classifiers, including Logistic Regression, Naive Bayes, Support Vector Machine, and Random Forest, which are not included in the original version of the system.

# Pre-Requirements

1. **Set up the Python environment**: Ensure you have Python installed on your system. It's recommended to use a virtual environment to manage dependencies.

    ```bash
    python -m venv venv
    source venv/bin/activate  
    # On Windows use `venv\Scripts\activate`
    ```

2. **Install dependencies**: Use `requirements.txt` to install all necessary packages.

    ```bash
    pip install -r requirements.txt
    ```


3. **Install SonarScanner and SonarQube**: SonarScanner and SonarQube are required for static analysis. Please follow the official installation instructions:

   - [SonarScanner](https://docs.sonarsource.com/sonarqube/latest/analysis/scan/sonarscanner/)
   - [SonarQube](https://docs.sonarsource.com/sonarqube/latest/setup/install-server/)

   Ensure that SonarQube is running locally or accessible from your environment for analysis.

4. **Generate a SonarQube User Token**: A user token is required for authentication with the SonarQube server. You can generate one by logging into SonarQube, navigating to your user account settings, and selecting Security > Generate Token. Save this token as you will need it to configure the analysis.

# How to use Perseverance
![tutorial](https://i.postimg.cc/gcVCPMkq/final.png)
