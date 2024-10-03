

class DictGenerator:
    def __init__(self, file):
        self.file = file
        self.rules_list = {}
        self.vulnerabilities = []

    def generate_rules_dict(self):
        with open(self.file, "r") as csv:
            # Skip the first line
            csv.readline()

            for line in csv:
                value_list = line.strip().split(";")
                if value_list[8] == "VULNERABILITY":
                    self.rules_list[value_list[3]] = 0

        return self.rules_list

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
                        "component": "/".join(value_list[9].split(":")[-2:]),
                        "CLS": value_list[-1]
                    }
                    self.vulnerabilities.append(dict_app)
        return self.vulnerabilities