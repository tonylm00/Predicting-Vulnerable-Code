class DictGenerator:
    def __init__(self, file):
        self.file = file
        self.rules = {}
        self.vulnerabilities = []

    def generate_rules_dict(self):
        with open(self.file, "r") as csv:
            csv.readline()

            for line in csv:
                value_list = line.strip().split(";")
                if value_list[8] == "VULNERABILITY":
                    self.rules[value_list[3]] = 0

        return self.rules

    def generate_vulnerability_dict(self):
        with open(self.file, "r") as csv:
            # Skip the first line
            csv.readline()

            for line in csv:
                value_list = line.strip().split(";")

                if value_list[8] == "VULNERABILITY":
                    dict_app = {
                        "type": value_list[8],
                        "rule": value_list[3],
                        "component": "\\".join(value_list[9].split(":")[-2:])
                    }
                    self.vulnerabilities.append(dict_app)
                elif value_list[8] == "NO_ISSUES_FOUND":
                    dict_app = {
                        "type": value_list[8],
                        "rule": "N/A",
                        "component": "\\".join(value_list[9].split(":")[-2:])
                    }
                    self.vulnerabilities.append(dict_app)
        return self.vulnerabilities
