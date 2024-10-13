import re
import shutil
import threading
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import os
import TKinterModernThemes as Tkmt
import pandas as pd
from Dataset2.AI_Module.RandomForest import predict_csv
from Dataset2.Main import Main


class Gui:
    def __init__(self):
        self.directory_destinazione = '..'
        self.main_frame = Tkmt.ThemedTKinterFrame("Perseverance", "sun-valley", "dark")
        self.window = self.main_frame.root
        self.window.title("Perseverance")
        self.window.geometry("500x900")
        self.window.resizable(False, False)
        self.set_icon()

        # checkboxes for options frame
        self.tm_checkbox = tk.IntVar()
        self.sm_checkbox = tk.IntVar()
        self.asa_checkbox = tk.IntVar()
        self.tm_checkbox_button = None
        self.sm_checkbox_button = None
        self.asa_checkbox_button = None
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

        # GUI components for start frame
        self.progress_bar = None

        # frames
        self.predict_frame = None
        self.options_frame = None
        self.results_frame = None
        self.start_frame = None

        # buttons for results frame
        self.analysis_button = None
        self.results_button = None

        self.build_predict_frame()
        self.build_options_frame()
        self.build_results_frame()
        self.build_start_frame()

        #values for analysis
        self.tm_value = 0
        self.sm_value = 0
        self.asa_value = 0

        self.base_dir = os.path.dirname(os.getcwd())
        self.run = Main(self.base_dir)
        self.run.clean_up()

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
        self.commit_id_entry = ttk.Entry(self.predict_frame, width=40)
        self.repo_url_label = ttk.Label(self.predict_frame, text="Repo URL:")
        self.repo_url_entry = ttk.Entry(self.predict_frame, width=40)

        self.commit_id_entry.insert(0, "57f2ccb66946943fbf3b3f2165eac1c8eb6b1523")
        self.repo_url_entry.insert(0, "https://github.com/spring-projects/spring-webflow")

        # Initially hidden
        self.commit_id_label.pack_forget()
        self.commit_id_entry.pack_forget()
        self.repo_url_label.pack_forget()
        self.repo_url_entry.pack_forget()

    def build_options_frame(self):
        self.options_frame = ttk.LabelFrame(self.window, text="Options", padding=(10, 10))
        self.options_frame.pack(padx=10, pady=10, fill="both")

        self.tm_checkbox_button = ttk.Checkbutton(self.options_frame, text="Text Mining", variable=self.tm_checkbox)
        self.tm_checkbox_button.pack(anchor="w")
        self.sm_checkbox_button = ttk.Checkbutton(self.options_frame, text="Software Metrics", variable=self.sm_checkbox)
        self.sm_checkbox_button.pack(anchor="w")
        self.asa_checkbox_button = ttk.Checkbutton(self.options_frame, text="ASA", variable=self.asa_checkbox,
                        command=self.manage_asa_fields)
        self.asa_checkbox_button.pack(anchor="w")

        self.sonarcloud_path_label = ttk.Label(self.options_frame, text="SonarScanner Path:")
        self.sonarcloud_path_entry = ttk.Entry(self.options_frame, width=50)

        self.sonarcloud_token_label = ttk.Label(self.options_frame, text="SonarCloud UserToken:")
        self.sonarcloud_token_entry = ttk.Entry(self.options_frame, width=50)

        self.sonarcloud_host_label = ttk.Label(self.options_frame, text="SonarCloud Host:")
        self.sonarcloud_host_entry = ttk.Entry(self.options_frame, width=50)

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

        self.analysis_button = ttk.Button(self.results_frame, text="Download Analysis Results",
                                          command=lambda: self.download_results_csv('analysis'), state=tk.DISABLED)

        self.results_button = ttk.Button(self.results_frame, text="Download Predictions",
                                         command=lambda: self.download_results_csv('prediction'), state=tk.DISABLED)

        self.analysis_button.pack(pady=5, fill="x")
        self.results_button.pack(pady=5, fill="x")

    def build_start_frame(self):
        start_frame = tk.LabelFrame(self.window, bd=0)
        start_frame.pack(padx=10, pady=10)

        self.progress_bar = ttk.Progressbar(start_frame, orient="horizontal", mode="determinate", length=280)
        self.progress_bar.grid(row=6, column=1, columnspan=2, padx=10, pady=20)

        self.progress_label = ttk.Label(start_frame, text="")
        self.progress_label.grid(row=7, column=1, columnspan=2, padx=10, pady=20)


        predict_button = ttk.Button(start_frame, text="Start", style="Accent.TButton", command=self.start_predict)
        predict_button.grid(row=5, column=1, pady=10, columnspan=2)

    def show_results_frame(self):
        self.results_frame.pack(padx=10, pady=10, fill="both")
        if self.tm_checkbox.get() or self.sm_checkbox.get() or self.asa_checkbox.get():
            self.analysis_button.config(state=tk.NORMAL)
            self.results_button.config(state=tk.NORMAL)

    def change_state_options(self, enable=True):
        if enable:
            self.tm_checkbox_button.config(state=tk.NORMAL)
            self.sm_checkbox_button.config(state=tk.NORMAL)
            self.asa_checkbox_button.config(state=tk.NORMAL)
        else:
            print("SEGNALE DI FUNGO")
            self.tm_checkbox_button.config(state=tk.DISABLED)
            print(self.tm_checkbox_button['state'])
            self.sm_checkbox_button.config(state=tk.DISABLED)
            self.asa_checkbox_button.config(state=tk.DISABLED)

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
            self.sonarcloud_path_entry.insert(0, r"C:\Program Files\SonarScanner\bin\sonar-scanner.bat")
            self.sonarcloud_token_label.pack(anchor="w", padx=10, pady=2)
            self.sonarcloud_token_entry.pack(anchor="w", padx=10, pady=2)
            self.sonarcloud_token_entry.insert(0, "squ_95089cde86a31904f6f2f0191e033099beb06c27")
            self.sonarcloud_host_label.pack(anchor="w", padx=10, pady=2)
            self.sonarcloud_host_entry.pack(anchor="w", padx=10, pady=2)
            self.sonarcloud_host_entry.insert(0, "http://localhost:9000")
        else:
            self.sonarcloud_path_label.pack_forget()
            self.sonarcloud_path_entry.pack_forget()
            self.sonarcloud_token_label.pack_forget()
            self.sonarcloud_token_entry.pack_forget()
            self.sonarcloud_host_label.pack_forget()
            self.sonarcloud_host_entry.pack_forget()

    def set_max_progress(self, value):
        self.progress_bar.config(maximum=value)

    def update_progress_label(self, text):
        self.progress_label.config(text=text)

    def start_progress(self):
        self.progress_bar.start()

    def stop_progress(self):
        self.progress_bar.stop()

    def form_validation(self):
        if self.switch_input_value.get() == "csv":
            if self.csv_label['text'] == "":
                messagebox.showwarning("Error - Predict Frame", "Carica un file CSV per continuare.")
                return False
        else:
            if self.commit_id_entry.get().strip() == "" or self.repo_url_entry.get().strip() == "":
                messagebox.showwarning("Error - Options Frame", "Inserisci commit_id e repo_url per continuare.")
                return False
            else:
                if not re.match(r'^https:\/\/github\.com\/[a-zA-Z0-9-]+\/[a-zA-Z0-9-]+$',
                                self.repo_url_entry.get().strip()):
                    messagebox.showwarning("Error - Options Frame",
                                           f"L'URL {self.repo_url_entry.get().strip()} non è valido")
                    return False
                if not re.match(r'^[a-z0-9]+$', self.commit_id_entry.get().strip()):
                    messagebox.showwarning("Error - Options Frame",
                                           f"Il commit {self.commit_id_entry.get().strip()} non è valido")
                    return False
        if self.asa_checkbox.get() == 1:
            if self.sonarcloud_path_entry.get().strip() == "" or self.sonarcloud_token_entry.get().strip() == "" or \
                    self.sonarcloud_host_entry.get().strip() == "":
                messagebox.showwarning("Error - Options Frame", "Inserisci i dati di SonarCloud per continuare.")
                return False

        return True

    def set_icon(self):
        icon_path = 'icon.ico'
        try:
            self.window.iconbitmap(icon_path)
        except Exception as e:
            print(f"Impossibile caricare l'icona: {e}")

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

    def download_results_csv(self, result_kind):

        results_type = {'text_mining': self.tm, 'software_metrics': self.sm, 'asa': self.asa}

        saving_path = filedialog.asksaveasfilename(defaultextension=".zip",
                                                   filetypes=[("ZIP files", "*.zip")],
                                                   title="Save ZIP file as")

        if saving_path:  # Check if user selected a file location
            try:
                self.run.download_results(result_kind, results_type, saving_path)

                # Display a success message
                messagebox.showinfo("Success", f"File saved successfully at {saving_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save the file: {e}")
        else:
            messagebox.showwarning("Cancelled", "File save operation was cancelled.")

    def start_predict(self):
        predict = threading.Thread(target=self.predict)
        predict.start()


    def predict(self):
        if not self.form_validation():
            return

        self.tm = self.tm_checkbox.get() == 1
        self.sm = self.sm_checkbox.get() == 1
        self.asa = self.asa_checkbox.get() == 1

        tm, sm, asa = self.tm, self.sm, self.asa

        if not (tm or sm or asa):
            self.window.after(0, lambda: messagebox.showwarning("Errore", "Bro qualcosa devi fa"))
            return

        self.window.after(0, lambda: self.change_state_options(False))

        # Set the progress bar max value based on the number of tasks
        num_tasks = tm + sm + asa + (tm * sm) + (tm * asa) + (sm * asa) + (
                    tm * sm * asa) + 1  # Calculate how many tasks are selected
        self.window.after(0, lambda: self.set_max_progress(num_tasks))

        if self.switch_input_value.get() == "csv":
            if self.csv_label['text'] == "":
                self.window.after(0,
                                  lambda:
                                  messagebox.showwarning("Errore", "Carica un file CSV per continuare."))
                continue_exec = False
            else:
                continue_exec = True

                self.window.after(0, self.progress_bar.step, 0.5)
                self.window.after(0, lambda: self.update_progress_label("Mining repositories..."))

                try:
                    self.run.run_repo_mining(self.csv_label['text'])
                except ValueError as e:
                    self.window.after(0,
                                      lambda:
                                      messagebox.showwarning("Errore", "Dataset header non valido."))
                    continue_exec = False
                    self.window.after(0, self.stop_progress)
                    self.window.after(0, lambda: self.update_progress_label("Execution error"))


        else:
            commit_id = self.commit_id_entry.get().strip()
            repo_url = self.repo_url_entry.get().strip()
            if not (commit_id and repo_url):
                self.window.after(0,
                                  lambda: messagebox.showwarning("Error", "Enter commit_id and repo_url to continue."))
                continue_exec = False
            else:
                continue_exec = True
                df = pd.DataFrame({'cve_id': [0], 'repo_url': [repo_url], 'commit_id': [commit_id]})
                df.to_csv(os.path.join(self.base_dir, 'repository.csv'), index=False)

                self.window.after(0, self.progress_bar.step, 0.5)
                self.window.after(0, lambda: self.update_progress_label("Mining repositories..."))

                self.run.run_repo_mining("repository.csv")

        if continue_exec:

            self.window.after(0, self.progress_bar.step, 0.5)
            self.window.after(0, lambda: self.update_progress_label("Mining Repositories completed..."))

            if tm:
                self.window.after(0, lambda: self.update_progress_label("Text Mining running..."))
                self.run.run_text_mining()
                self.run.run_prediction(
                    os.path.join(self.base_dir, "mining_results", "csv_mining_final.csv"),
                    os.path.join(self.base_dir, "AI_Module", "model", "random_forest_TM.pkl"),
                    os.path.join(self.base_dir, "AI_Module", "label_encoder.pkl"),
                    os.path.join(self.base_dir, "AI_Module", "vocab", "original_vocab_TM.pkl"),
                    os.path.join(self.base_dir, "Predict", "Predict_TM.csv")
                )
                self.window.after(0, self.progress_bar.step, 1)

            if sm:
                self.window.after(0, lambda: self.update_progress_label("Metrics computation running..."))
                self.run.run_software_metrics()
                self.run.run_prediction(
                    os.path.join(self.base_dir, "Software_Metrics", "mining_results_sm_final.csv"),
                    os.path.join(self.base_dir, "AI_Module", "model", "random_forest_SM.pkl"),
                    os.path.join(self.base_dir, "AI_Module", "label_encoder.pkl"),
                    os.path.join(self.base_dir, "AI_Module", "vocab", "original_vocab_SM.pkl"),
                    os.path.join(self.base_dir, "Predict", "Predict_SM.csv")
                )
                self.window.after(0, self.progress_bar.step, 1)

            if asa:
                self.window.after(0, lambda: self.update_progress_label("Static Analysis running..."))

                try:
                    self.run.run_ASA(self.sonarcloud_host_entry.get(), self.sonarcloud_token_entry.get(), self.sonarcloud_path_entry.get())

                    self.run.run_prediction(
                        os.path.join(self.base_dir, "mining_results_ASA", "csv_ASA_final.csv"),
                        os.path.join(self.base_dir, "AI_Module", "model", "random_forest_ASA.pkl"),
                        os.path.join(self.base_dir, "AI_Module", "label_encoder.pkl"),
                        os.path.join(self.base_dir, "AI_Module", "vocab", "original_vocab_ASA.pkl"),
                        os.path.join(self.base_dir, "Predict", "Predict_ASA.csv")
                    )

                except Exception:
                    self.window.after(0, lambda: messagebox.showwarning("Error", f"Error in static analysis, check "
                                                                                 f"the logs!"))
                    self.asa_checkbox.set(0)
                    asa = False

                self.window.after(0, self.progress_bar.step, 1)

            if tm and sm and asa:
                self.window.after(0, lambda: self.update_progress_label("Combining results..."))
                self.run.total_combination()
                self.run.run_prediction(
                    os.path.join(self.base_dir, "Union", "3COMBINATION.csv"),
                    os.path.join(self.base_dir, "AI_Module", "model", "random_forest_3Combination.pkl"),
                    os.path.join(self.base_dir, "AI_Module", "label_encoder.pkl"),
                    os.path.join(self.base_dir, "AI_Module", "vocab", "original_vocab_3Combination.pkl"),
                    os.path.join(self.base_dir, "Predict", "Predict_3Combination.csv")
                )
                self.window.after(0, self.progress_bar.step, 1)

            if tm and sm:
                self.window.after(0, lambda: self.update_progress_label("Combining results..."))
                self.run.combine_tm_sm()
                self.run.run_prediction(
                    os.path.join(self.base_dir, "Union", "Union_TM_SM.csv"),
                    os.path.join(self.base_dir, "AI_Module", "model", "random_forest_TMSM.pkl"),
                    os.path.join(self.base_dir, "AI_Module", "label_encoder.pkl"),
                    os.path.join(self.base_dir, "AI_Module", "vocab", "original_vocab_TMSM.pkl"),
                    os.path.join(self.base_dir, "Predict", "Predict_TMSM.csv")
                )
                self.window.after(0, self.progress_bar.step, 1)

            if tm and asa:
                self.window.after(0, lambda: self.update_progress_label("Combining results..."))
                self.run.combine_tm_asa()
                self.run.run_prediction(
                    os.path.join(self.base_dir, "Union", "Union_TM_ASA.csv"),
                    os.path.join(self.base_dir, "AI_Module", "model", "random_forest_TMASA.pkl"),
                    os.path.join(self.base_dir, "AI_Module", "label_encoder.pkl"),
                    os.path.join(self.base_dir, "AI_Module", "vocab", "original_vocab_TMASA.pkl"),
                    os.path.join(self.base_dir, "Predict", "Predict_TMASA.csv")
                )
                self.window.after(0, self.progress_bar.step, 1)

            if sm and asa:
                self.window.after(0, lambda: self.update_progress_label("Combining results..."))
                self.run.combine_sm_asa()
                self.run.run_prediction(
                    os.path.join(self.base_dir, "Union", "Union_SM_ASA.csv"),
                    os.path.join(self.base_dir, "AI_Module", "model", "random_forest_SMASA.pkl"),
                    os.path.join(self.base_dir, "AI_Module", "label_encoder.pkl"),
                    os.path.join(self.base_dir, "AI_Module", "vocab", "original_vocab_SMASA.pkl"),
                    os.path.join(self.base_dir, "Predict", "Predict_SMASA.csv")
                )
                self.window.after(0, self.progress_bar.step, 1)

            self.window.after(0, lambda: self.update_progress_label("Execution Completed"))

            # Reset progress bar before starting
            self.window.after(0, self.stop_progress)
            self.window.after(0, self.show_results_frame)
            self.window.after(0, lambda: self.change_state_options(True))

    def start(self):
        self.window.mainloop()

if __name__ == '__main__':
    gui = Gui()
    gui.start()
