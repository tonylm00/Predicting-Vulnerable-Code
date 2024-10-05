from .JavaTextMining import JavaTextMining


class CSVWriter:
    def __init__(self, filtered_dict, mining_dict, output_csv_name):
        """
        Initializes the class with two dictionaries:
        - filtered_dict: Dictionary from FilteredTextMining
        - mining_dict: Dictionary of dictionaries from java_text_mining.txt files
        """
        self.filtered_dict = filtered_dict
        self.mining_dict = mining_dict
        self.csv_sorted = sorted(filtered_dict.keys())
        self.output_csv_name = output_csv_name

    def write_header(self):
        """
        Writes the header of the CSV file.
        """
        with open(self. output_csv_name, "w+", encoding="utf-8") as final_csv:
            final_csv.write("Name")
            for element in self.csv_sorted:
                final_csv.write(", " + str(element))
            final_csv.write(", CLS")
            final_csv.write("\n")

    def write_rows(self):
        """
        Writes the rows of the CSV file based on the mining_dict.
        """
        with open(self.output_csv_name, "a", encoding="utf-8") as final_csv:
            for commit_name, current_dict in self.mining_dict.items():
                final_csv.write(commit_name)
                dict = JavaTextMining.splitDict(current_dict[0])  # Splitting the Java class words by CamelCase
                for element in self.csv_sorted:
                    if element in dict.keys():
                        final_csv.write("," + str(dict[element]))
                    else:
                        final_csv.write(",0")
                final_csv.write(f", {current_dict[1]}")
                final_csv.write("\n")