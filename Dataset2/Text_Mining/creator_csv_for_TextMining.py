import ast
import os
import re
from . import less_element_text_mining #CamelCase splitting module
'''
This script takes the "FilteredTextMining" dictionary and every single text mining file to perform a new dataset 
that contains the frequency analysis for each java class that contains that word.
WARNING: RepositoryMining18 is collected inside the RepositoryMining17 for the positive
istances, and RepositoryMining19 the negative ones.
'''
def main():
	dict_file_name="FilteredTextMining.txt"
	final_csv_name = "csv_mining_final.csv"
	os.chdir("..")
	cwd = os.getcwd()
	repo_name = "RepositoryMining"
	os.chdir(cwd+"/mining_results")
	final_csv = open(final_csv_name, "w+", encoding="utf-8")
	big_dict_file = open(dict_file_name, "r+", encoding="utf-8")
	big_dict = ast.literal_eval(big_dict_file.read())
	csv_sorted = sorted(big_dict.keys())
	final_csv.write("NameClass")
	for element in csv_sorted:
		final_csv.write(" ," + str(element))
	final_csv.write(" ,class")
	final_csv.write("\n\n")
	for count in range(1,36,1):
		if count != 18:
			repo = repo_name + str(count)
			if repo != ".DS_Store":
				os.chdir(repo)
				for cvd_id in os.listdir():
					if cvd_id not in [".DS_Store", "CHECK.txt", "ERRORS.txt"]:
						print(cvd_id)
						os.chdir(cvd_id)
						print(os.listdir())
						for folder in os.listdir():
							if folder != ".DS_Store":
								os.chdir(folder)
								commit_name = folder
								for file in os.listdir():
									if file != ".DS_Store":
										if re.match(r'^[A-Z][\w]*\.java_text_mining\.txt$', file):
											current_file = open(file, "r", encoding="utf-8")
											#convert the single text mining file in a dictionary.
											current_dict = ast.literal_eval(current_file.read())
											current_dict = less_element_text_mining.splitCamelCase(current_dict) #splitting the current dict of the java class in more words by CamelCase
											name_of_file_for_csv = file.replace("text_mining.txt", "")
											final_csv.write(commit_name + "/" + name_of_file_for_csv)
											for element in csv_sorted:
												if element in current_dict.keys():
													final_csv.write(",")
													final_csv.write(str(current_dict[element]))	
												else:		
													final_csv.write(",")		
													final_csv.write(str(0))
											if count < 18:
												final_csv.write(", pos")
											else:
												if count >18:
													final_csv.write(", neg")
											final_csv.write("\n")
									else:
										print(".DS_Store occured")
								os.chdir("..")
						os.chdir("..")
				os.chdir("..")
	final_csv.close()
	print("BUILD SUCCESS !")

if __name__ == '__main__':
	main()
