import os
from Dataset2.Text_Mining.CSVWriter import CSVWriter
from Dataset2.Text_Mining.JavaTextMining import JavaTextMining

def runTextMining():
	tm_dict = {}
	dict_java_files = {}
	os.chdir("..")
	cwd = os.getcwd()
	repo_name = "RepositoryMining"
	os.chdir(cwd+"/mining_results")
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
								for file in os.listdir():
									if file != ".DS_Store":
										if file.endswith(".java"):
											java_file_name = file
											analyzer = JavaTextMining(java_file_name)
											dict = analyzer.takeJavaClass()
											with open(java_file_name+"_text_mining.txt", "w+", encoding="utf-8") as file:
												file.write(str(dict))
											file_cls = "pos"
											if count > 18:
												file_cls = "neg"
											dict_java_files[folder + "/" + java_file_name] = [dict, file_cls]
											tm_dict = JavaTextMining.mergeDict(tm_dict, dict)
									else:
										print(".DS_Store occured")
								os.chdir("..")
						os.chdir("..")
				os.chdir("..")
	#with open("text_mining_dict.txt", "w+", encoding="utf-8") as file:
	#	file.write(str(tm_dict))
	split_dict = JavaTextMining.splitDict(tm_dict)
	# with open("FilteredTextMining.txt", "w+", encoding="utf-8") as file:
	#	file.write(str(split_dict))
	csv_final = CSVWriter(split_dict, dict_java_files, "csv_mining_final.csv")
	csv_final.write_header()
	csv_final.write_rows()

if __name__ == '__main__':
	runTextMining()