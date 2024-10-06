import os


class DatasetDivider:
    def __init__(self, base_dir, dataset_name):
        self.dataset_name = dataset_name
        self.base_dir = base_dir

    def divide_dataset(self):
        dataset_path = os.path.join(self.base_dir, self.dataset_name)
        divide_dataset_path = os.path.join(self.base_dir, 'Dataset_Divided')
        csvfile = open(dataset_path, 'r').readlines()
        filename = 1
        if "Dataset_Divided" not in os.listdir():
            os.mkdir("Dataset_Divided")
        os.chdir(divide_dataset_path)

        header = csvfile[0]
        csvfile = csvfile[1:]

        if len(csvfile) == 0:
            with open(str(filename) + '.csv', 'w+') as new_file:
                new_file.writelines([header])
        else:
            for i in range(0, len(csvfile)):
                if i % 50 == 0:
                    with open(str(filename) + '.csv', 'w+') as new_file:
                        new_file.write(header)
                        new_file.writelines(csvfile[i:i + 50])
                    filename += 1