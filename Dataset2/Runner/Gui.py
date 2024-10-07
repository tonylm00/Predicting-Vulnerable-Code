import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import os
import TKinterModernThemes as Tkmt
import pandas as pd
from Dataset2.AI_Module.RandomForest import predict_csv
from Dataset2.main import Main


class Gui:
    def __init__(self):
        self.directory_destinazione = '..'
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
        self.results_button = None

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
                                    command=lambda: self.download_analysis_csv('text_mining'), state=tk.DISABLED)
        self.sm_button = ttk.Button(self.results_frame, text="Download Software Metrics Results",
                                    command=lambda: self.download_analysis_csv('software_metrics'), state=tk.DISABLED)
        self.asa_button = ttk.Button(self.results_frame, text="Download ASA Results",
                                     command=lambda: self.download_analysis_csv('asa'), state=tk.DISABLED)

        self.results_button = ttk.Button(self.results_frame, text="Download Predictions",
                                     command=lambda: self.download_results_csv(), state=tk.NORMAL)


        self.tm_button.pack(pady=5, fill="x")
        self.sm_button.pack(pady=5, fill="x")
        self.asa_button.pack(pady=5, fill="x")
        self.results_button.pack(pady=5, fill="x")

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
    def download_analysis_csv(file_type):

        # Ask the user where to save the zip file
        saving_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv"),
                                                                ("All Files", "*.*")],
                                                     title="Save the CSV file as")

        if saving_path:  # Check if user selected a file location
            try:
                run = Main()

                run.download_analysis_results(file_type, saving_path)

                # Display a success message
                messagebox.showinfo("Success", f"File saved successfully at {saving_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save the file: {e}")
        else:
            messagebox.showwarning("Cancelled", "File save operation was cancelled.")

    def download_results_csv(self):
        tm = self.tm_checkbox.get() == 1
        sm = self.sm_checkbox.get() == 1
        asa = self.asa_checkbox.get() == 1

        results_type = {'text_mining': tm, 'software_metrics': sm, 'asa': asa}

        saving_path = filedialog.asksaveasfilename(defaultextension=".zip",
                                                     filetypes=[("ZIP files", "*.zip")],
                                                     title="Save ZIP file as")

        if saving_path:  # Check if user selected a file location
            try:
                run = Main()

                run.download_results(results_type, saving_path)

                # Display a success message
                messagebox.showinfo("Success", f"File saved successfully at {saving_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save the file: {e}")
        else:
            messagebox.showwarning("Cancelled", "File save operation was cancelled.")



    def predict(self):
        tm = self.tm_checkbox.get() == 1
        sm = self.sm_checkbox.get() == 1
        asa = self.asa_checkbox.get() == 1
        run = Main()
        if self.switch_input_value.get() == "csv":
            if self.csv_label['text'] == "":
                messagebox.showwarning("Errore", "Carica un file CSV per continuare.")
                continue_exec = False
            else:
                messagebox.showinfo("Predict", f"Predizione con file CSV: {self.csv_label['text']} \n")
                continue_exec = True
                #run.run_repo_mining(self.csv_label['text'])
        else:
            commit_id = self.commit_id_entry.get().strip()
            repo_url = self.repo_url_entry.get().strip()
            if not (commit_id and repo_url):
                messagebox.showwarning("Errore", "Inserisci commit_id e repo_url per continuare.")
                continue_exec = False
            else:
                messagebox.showinfo("Predict", f"Predizione per commit_id: {commit_id}, repo_url: {repo_url}")
                continue_exec = True
                df = pd.DataFrame({'cve_id': [0], 'repo_url': [repo_url], 'commit_id': [commit_id]})
                df.to_csv('../repository.csv', index=False)
                run.run_repo_mining("repository.csv")
        if continue_exec:
            if tm:
                run.run_text_mining()
                predict_csv("mining_results/csv_mining_final.csv",
                            "AI_Module/model/random_forest_TM.pkl",
                            "AI_Module/label_encoder.pkl", "AI_Module/vocab/original_vocab_TM.pkl",
                            "Predict/Predict_TM.csv")

            if sm:
                run.run_software_metrics()
                predict_csv("Software_Metrics/metrics_results_sm_final.csv",
                            "AI_Module/model/random_forest_SM.pkl",
                            "AI_Module/label_encoder.pkl", "AI_Module/vocab/original_vocab_SM.pkl",
                            "Predict/Predict_SM.csv")

            if asa:
                run.run_ASA(self.sonarcloud_host_entry, self.sonarcloud_token_entry, self.sonarcloud_path_entry)
                predict_csv("mining_results_ASA/csv_ASA_final.csv",
                            "AI_Module/model/random_forest_ASA.pkl",
                            "AI_Module/label_encoder.pkl", "AI_Module/vocab/original_vocab_ASA.pkl",
                            "Predict/Predict_ASA.csv")
            if tm and sm and asa:
                run.total_combination()
                predict_csv("Union/3COMBINATION.csv",
                            "AI_Module/model/random_forest_3Combination.pkl",
                            "AI_Module/label_encoder.pkl", "AI_Module/vocab/original_vocab_3Combination.pkl",
                            "Predict/Predict_3Combination.csv")
            elif tm and sm:
                run.combine_tm_sm()
                predict_csv("Union/Union_TM_SM.csv",
                            "AI_Module/model/random_forest_TMSM.pkl",
                            "AI_Module/label_encoder.pkl", "AI_Module/vocab/original_vocab_TMSM.pkl",
                            "Predict/Predict_TMSM.csv")
            elif tm and asa:
                run.combine_tm_asa()
                predict_csv("Union/Union_TM_ASA.csv",
                            "AI_Module/model/random_forest_TMASA.pkl",
                            "AI_Module/label_encoder.pkl", "AI_Module/vocab/original_vocab_TMASA.pkl",
                            "Predict/Predict_TMASA.csv")
            elif sm and asa:
                run.combine_sm_asa()
                predict_csv("Union/Union_SM_ASA.csv",
                            "AI_Module/model/random_forest_SMASA.pkl",
                            "AI_Module/label_encoder.pkl", "AI_Module/vocab/original_vocab_SMASA.pkl",
                            "Predict/Predict_SMASA.csv")
        self.show_results_frame()

    def start(self):
        self.window.mainloop()

if __name__ == '__main__':
    gui = Gui()
    gui.start()
