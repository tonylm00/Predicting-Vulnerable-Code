import os
import shutil


class DatasetDivider:
    def __init__(self, base_dir, dataset_name):
        self.dataset_name = dataset_name
        self.base_dir = base_dir

    def divide_dataset(self):
        dataset_path = os.path.join(self.base_dir, self.dataset_name)
        divide_dataset_path = os.path.join(self.base_dir, 'Dataset_Divided')

        csvfile = open(dataset_path, 'r').readlines()
        filename = 1

        os.makedirs(divide_dataset_path, exist_ok=True)

        header = csvfile[0]
        csvfile = csvfile[1:]

        if len(csvfile) == 0:
            new_file_path = os.path.join(divide_dataset_path, str(filename) + '.csv')
            with open(new_file_path, 'w+') as new_file:
                new_file.writelines([header])
        else:
            for i in range(0, len(csvfile), 50):
                new_file_path = os.path.join(divide_dataset_path, str(filename) + '.csv')
                with open(new_file_path, 'w+') as new_file:
                    new_file.write(header)
                    new_file.writelines(csvfile[i:i + 50])
                filename += 1