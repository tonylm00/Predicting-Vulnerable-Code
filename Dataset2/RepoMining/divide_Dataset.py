import os
'''
Divide the entire dataset in small pieces of 50 commits.
'''
os.chdir("..")
cwd = os.getcwd()
csvfile = open('initial_Dataset.csv', 'r').readlines()
filename = 1
if "Dataset_Divided" not in os.listdir():
	os.mkdir("Dataset_Divided")
os.chdir(cwd + "/Dataset_Divided")
header = csvfile[0]

csvfile = csvfile[1:]

if len(csvfile)==0:
	with open(str(filename) + '.csv', 'w+') as new_file:
		new_file.writelines([header])
else:
	for i in range(0, len(csvfile)):
		if i % 50 == 0:
			with open(str(filename) + '.csv', 'w+') as new_file:
				new_file.write(header)
				new_file.writelines(csvfile[i:i + 50])
			filename += 1