import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import os
import TKinterModernThemes as Tkmt

from Dataset2.RepoMining.Dataset_Divider import DatasetDivider
from Dataset2.RepoMining.RepoMiner import RepoMiner


class Gui:
    def __init__(self):
        self.directory_destinazione = 'data/'
        self.main_frame = Tkmt.ThemedTKinterFrame("Perseverance", "sun-valley", "dark")
        self.window = self.main_frame.root
        self.window.title("Perseverance")
        self.window.geometry("400x700")
        self.window.resizable(False, False)

        # checkboxes for options frame
        self.tm_checkbox = tk.IntVar()
        self.sm_checkbox = tk.IntVar()
        self.asa_checkbox = tk.IntVar()
        self.switch_input_value = tk.StringVar(value='csv')

        # GUI components for asa option
        self.sonarcloud_path_label = None
        self.sonarcloud_path_entry = None
        self.sonarcloud_token_label = None
        self.sonarcloud_token_entry = None
        self.sonarcloud_host_label = None
        self.sonarcloud_host_entry = None

        # GUI components for predict frame
        self.commit_id_label = None
        self.commit_id_entry = None
        self.repo_url_label = None
        self.repo_url_entry = None
        self.switch_csv = None
        self.csv_label = None
        self.upload_csv_button = None

        # frames
        self.predict_frame = None
        self.options_frame = None
        self.results_frame = None
        self.start_frame = None

        # buttons for results frame
        self.tm_button = None
        self.sm_button = None
        self.asa_button = None

        self.build_predict_frame()
        self.build_options_frame()
        self.build_results_frame()
        self.build_start_frame()

    def build_predict_frame(self):
        self.predict_frame = ttk.LabelFrame(self.window, text="Predict", padding=(10, 10))
        self.predict_frame.pack(padx=10, pady=10, fill="both")

        self.switch_csv = ttk.Checkbutton(self.predict_frame, text="Usa Commit",
                                          command=self.manage_switch, style='Switch.TCheckbutton')
        self.switch_csv.pack(pady=(0, 10))

        self.csv_label = ttk.Label(self.predict_frame, text="", state=tk.NORMAL, width=25)
        self.csv_label.pack()

        self.upload_csv_button = ttk.Button(self.predict_frame, text="Upload CSV", command=self.load_file,
                                            style="Accent.TButton")
        self.upload_csv_button.pack(pady=(0, 5))

        self.commit_id_label = ttk.Label(self.predict_frame, text="Commit ID:")
        self.commit_id_entry = ttk.Entry(self.predict_frame, width=25)
        self.repo_url_label = ttk.Label(self.predict_frame, text="Repo URL:")
        self.repo_url_entry = ttk.Entry(self.predict_frame, width=25)

        # Initially hidden
        self.commit_id_label.pack_forget()
        self.commit_id_entry.pack_forget()
        self.repo_url_label.pack_forget()
        self.repo_url_entry.pack_forget()

    def build_options_frame(self):
        self.options_frame = ttk.LabelFrame(self.window, text="Options", padding=(10, 10))
        self.options_frame.pack(padx=10, pady=10, fill="both")

        ttk.Checkbutton(self.options_frame, text="Text Mining", variable=self.tm_checkbox).pack(anchor="w")
        ttk.Checkbutton(self.options_frame, text="Software Metrics", variable=self.sm_checkbox).pack(anchor="w")
        ttk.Checkbutton(self.options_frame, text="ASA", variable=self.asa_checkbox,
                        command=self.manage_asa_fields).pack(anchor="w")

        self.sonarcloud_path_label = ttk.Label(self.options_frame, text="SonarCloud Path:")
        self.sonarcloud_path_entry = ttk.Entry(self.options_frame, width=25)

        self.sonarcloud_token_label = ttk.Label(self.options_frame, text="SonarCloud UserToken:")
        self.sonarcloud_token_entry = ttk.Entry(self.options_frame, width=25)

        self.sonarcloud_host_label = ttk.Label(self.options_frame, text="SonarCloud Host:")
        self.sonarcloud_host_entry = ttk.Entry(self.options_frame, width=25)

        # Initially hidden
        self.sonarcloud_path_label.pack_forget()
        self.sonarcloud_path_entry.pack_forget()
        self.sonarcloud_token_label.pack_forget()
        self.sonarcloud_token_entry.pack_forget()
        self.sonarcloud_host_label.pack_forget()
        self.sonarcloud_host_entry.pack_forget()

    def build_results_frame(self):
        self.results_frame = ttk.LabelFrame(self.window, text="Results", padding=(10, 10))
        self.results_frame.pack(padx=10, pady=10, fill="both")
        self.results_frame.pack_forget()

        self.tm_button = ttk.Button(self.results_frame, text="Download Text Mining Results",
                                    command=lambda: self.download_csv('text_mining'), state=tk.DISABLED)
        self.sm_button = ttk.Button(self.results_frame, text="Download Software Metrics Results",
                                    command=lambda: self.download_csv('software_metrics'), state=tk.DISABLED)
        self.asa_button = ttk.Button(self.results_frame, text="Download ASA Results",
                                     command=lambda: self.download_csv('asa'), state=tk.DISABLED)

        self.tm_button.pack(pady=5, fill="x")
        self.sm_button.pack(pady=5, fill="x")
        self.asa_button.pack(pady=5, fill="x")

    def build_start_frame(self):
        start_frame = tk.LabelFrame(self.window, bd=0)
        start_frame.pack(padx=10, pady=10)
        predict_button = ttk.Button(start_frame, text="Start", style="Accent.TButton", command=self.predict)
        predict_button.grid(row=5, column=1, pady=10, columnspan=2)

    def show_results_frame(self):
        self.results_frame.pack(padx=10, pady=10, fill="both")
        if self.tm_checkbox.get():
            self.tm_button.config(state=tk.NORMAL)
        if self.sm_checkbox.get():
            self.sm_button.config(state=tk.NORMAL)
        if self.asa_checkbox.get():
            self.asa_button.config(state=tk.NORMAL)

    def manage_switch(self):
        if self.switch_input_value.get() == "commit":
            self.switch_input_value.set('csv')
            self.switch_csv.config(text='Usa Commit')
            self.csv_label.pack()
            self.upload_csv_button.pack()
            self.commit_id_label.pack_forget()
            self.commit_id_entry.pack_forget()
            self.repo_url_label.pack_forget()
            self.repo_url_entry.pack_forget()
        else:
            self.switch_input_value.set('commit')
            self.switch_csv.config(text='Usa CSV')
            self.csv_label.pack_forget()
            self.upload_csv_button.pack_forget()
            self.commit_id_label.pack()
            self.commit_id_entry.pack()
            self.repo_url_label.pack()
            self.repo_url_entry.pack()

    def manage_asa_fields(self):
        if self.asa_checkbox.get() == 1:
            self.sonarcloud_path_label.pack(anchor="w", padx=10, pady=2)
            self.sonarcloud_path_entry.pack(anchor="w", padx=10, pady=2)
            self.sonarcloud_token_label.pack(anchor="w", padx=10, pady=2)
            self.sonarcloud_token_entry.pack(anchor="w", padx=10, pady=2)
            self.sonarcloud_host_label.pack(anchor="w", padx=10, pady=2)
            self.sonarcloud_host_entry.pack(anchor="w", padx=10, pady=2)
        else:
            self.sonarcloud_path_label.pack_forget()
            self.sonarcloud_path_entry.pack_forget()
            self.sonarcloud_token_label.pack_forget()
            self.sonarcloud_token_entry.pack_forget()
            self.sonarcloud_host_label.pack_forget()
            self.sonarcloud_host_entry.pack_forget()

    def load_file(self):
        file_path = filedialog.askopenfilename(title="Load CSV", filetypes=[("CSV files", "*.csv")])
        if file_path:
            if not os.path.exists(self.directory_destinazione):
                os.makedirs(self.directory_destinazione)
            file_name = os.path.basename(file_path)
            destinazione_file = os.path.join(self.directory_destinazione, file_name)
            shutil.copy(file_path, destinazione_file)
            self.csv_label.config(text=file_name)
            self.commit_id_entry.delete(0, tk.END)
            self.repo_url_entry.delete(0, tk.END)

    def get_selected_options(self):
        options = {
            'Text Mining': self.tm_checkbox.get(),
            'Software Metrics': self.sm_checkbox.get(),
            'ASA': self.asa_checkbox.get(),
        }
        return options

    @staticmethod
    def download_csv(file_type):
        file_map = {
            'text_mining': 'text_mining_results.csv',
            'software_metrics': 'software_metrics_results.csv',
            'asa': 'asa_results.csv'
        }
        file_name = file_map.get(file_type)
        if file_name:
            messagebox.showinfo("Download", f"Downloading {file_name}")

    def predict(self):
        if self.switch_input_value.get() == "csv":
            if self.csv_label['text'] == "":
                messagebox.showwarning("Errore", "Carica un file CSV per continuare.")
            else:
                messagebox.showinfo("Predict", f"Predizione con file CSV: {self.csv_label['text']} \n")
                self.pipeline(self.csv_label['text'])
        else:
            commit_id = self.commit_id_entry.get().strip()
            repo_url = self.repo_url_entry.get().strip()
            if not (commit_id and repo_url):
                messagebox.showwarning("Errore", "Inserisci commit_id e repo_url per continuare.")
            else:
                messagebox.showinfo("Predict", f"Predizione per commit_id: {commit_id}, repo_url: {repo_url}")

    def pipeline(self, dataset_name):
        dataset_divider = DatasetDivider(os.path.join(os.getcwd(), 'data'), dataset_name)
        dataset_divider.divide_dataset()

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

        self.show_results_frame()

    def start(self):
        self.window.mainloop()


if __name__ == '__main__':
    gui = Gui()
    gui.start()
