import os

from Dataset_Divider import DatasetDivider
from RepoMiner import RepoMiner


if __name__ == '__main__':
	os.chdir('..')

	dataset_div = DatasetDivider(os.getcwd(), 'initial_Dataset.csv')
	dataset_div.divide_dataset()

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