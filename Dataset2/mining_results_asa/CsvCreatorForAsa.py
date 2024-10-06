from Dataset2.mining_results_asa.DictGenerator import DictGenerator


class CsvCreatorForASA:
    def __init__(self, final_csv_name, rules_dict, vulnerabilities):
        self.final_csv_name = final_csv_name
        self.big_dict = {}
        self.rules_dict = rules_dict
        self.vulnerabilities = vulnerabilities

    def create_csv(self):
        self.process_vulnerabilities()
        self.write_final_csv()
        print(f"{self.final_csv_name} creato con successo")

    def process_vulnerabilities(self):
        for el in self.vulnerabilities:
            component = el["component"]
            rule = el["rule"]
            if component in self.big_dict:
                if rule in self.big_dict[component]:
                    self.big_dict[component][rule] += 1
                else:
                    self.big_dict[component][rule] = 1
            else:
                self.big_dict[component] = {"CLS": el["CLS"], rule: 1}

    def write_final_csv(self):
        with open(self.final_csv_name, "w") as final_csv:
            final_csv.write("Name")
            for key in self.rules_dict.keys():
                final_csv.write("," + key)
            final_csv.write(",CLS\n")

            for java_class_key, java_class_dict in self.big_dict.items():
                print(f"Java class: {java_class_key}")
                print(f"Java class dict: {java_class_dict}")
                print(f"Big dict: {self.big_dict}")
                final_csv.write(java_class_key)
                for rule in self.rules_dict:
                    final_csv.write("," + str(java_class_dict.get(rule, 0)))
                final_csv.write("," + java_class_dict["CLS"] + "\n")





