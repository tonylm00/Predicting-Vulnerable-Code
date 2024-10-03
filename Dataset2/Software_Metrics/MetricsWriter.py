import csv

class MetricsWriter:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.fieldnames = ["Kind", "Name", "CountLineCode", "CountDeclClass", "CountDeclFunction", "CountLineCodeDecl",
                           "SumEssential", "SumCyclomaticStrict", "MaxEssential", "MaxCyclomaticStrict", "MaxNesting", "CLS"]

    def write_header(self):
        try:
            with open(self.csv_file, mode="w", newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
        except IOError as e:
            print(f"Errore durante l'apertura del file: {e}")

    def write_metrics(self, kind, name, metrics, file_cls):
        try:
            with open(self.csv_file, mode="a", newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                csv_data = {
                    "Kind": kind,
                    "Name": name,
                    **metrics,
                    "CLS": file_cls
                }
                writer.writerow(csv_data)
        except IOError as e:
            print(f"Errore durante la scrittura nel file: {e}")
