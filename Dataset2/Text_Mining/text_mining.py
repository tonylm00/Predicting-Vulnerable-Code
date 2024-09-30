import re
import os
'''
This script takes every java class and return a dictionary of words in order to 
perform the Text Mining.
'''


'''
@Param s: Input String.
Delete the constant value inside the string line and return a vector of unigrams.
'''
def stringTokenizer(s):
    # Prendi i valori di stringa
    discard_list = re.findall(r'\"(.+?)\"', s)
    tokens = re.findall(r"[\w']+|[^\w\s']", s)
    # Dividi i valori di stringa in parole
    for string in discard_list:
        word_vector = string.split(" ")
        # Rimuovi ogni parola nei tokens
        for word in word_vector:
            if word in tokens:
                tokens.remove(word)
    withoutAlpha = removeNotAlpha(tokens)
    return withoutAlpha

'''
@Param java_file: file object 
Delete all types of comments inside the "java_file".
'''
# problema con // all'interno di stringhe
def removeComments(java_file):
	text = java_file.read()
	# Pattern per stringhe (sia con virgolette doppie che singole)
	string_pattern = r'"(\\.|[^"\\])*"|\'(\\.|[^\'\\])*\''

	# Pattern per commenti multi-linea
	multiline_comment_pattern = r'/\*(.|\n)*?\*/'

	# Pattern per commenti single-line
	singleline_comment_pattern = r'//.*'

	# Prima, rimuoviamo i commenti multi-linea e single-line solo se NON sono dentro stringhe
	def replacer(match):
		# Se il match corrisponde a una stringa, la restituiamo com'è
		if re.match(string_pattern, match.group(0)):
			return match.group(0)
		# Altrimenti, è un commento, lo sostituiamo con uno spazio
		else:
			return ' '

	# Uniamo tutti i pattern: stringhe e commenti
	combined_pattern = f'{string_pattern}|{multiline_comment_pattern}|{singleline_comment_pattern}'

	# Applichiamo il replacer al testo per rimuovere i commenti fuori dalle stringhe
	result = re.sub(combined_pattern, replacer, text)

	return result

'''
@Param java_file_name: name of the file.
Execute the Tokenization deleting the comments, strings and no-Alpha characters.
'''
def takeJavaClass(java_file_name):
	final = []
	current = []
	dic ={}
	with open(java_file_name, "r", encoding="utf-8") as java_file:
		text=removeComments(java_file)
		for line in text.splitlines():
			current = stringTokenizer(line)
			print(current)
			final+=current
			for eachElem in current:
				if eachElem in dic:
					dic[eachElem] += 1
				else:
					dic[eachElem] = 1
		return dic

'''
@Param tokens: list of words.
Return the list of words without no-Alpha characters.
'''
def removeNotAlpha(tokens):
	rightOne = []
	for element in tokens:
		if(element.isalpha()):
			rightOne.append(element)
	return rightOne

def main():
	java_file_name=""
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
										java_file_name = file
										dic = takeJavaClass(java_file_name)
										file = open(java_file_name+"_text_mining.txt", "w+", encoding="utf-8")
										file.write(str(dic))
										file.close()
									else:
										print(".DS_Store occured")
								os.chdir("..")
						os.chdir("..")
				os.chdir("..")

if __name__ == '__main__':
	main()