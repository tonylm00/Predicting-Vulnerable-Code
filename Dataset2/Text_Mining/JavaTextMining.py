import re

class JavaTextMining:
    def __init__(self, java_file_path):
        self.java_file_path = java_file_path

    def stringTokenizer(self, s):
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
        withoutAlpha = self.removeNotAlpha(tokens)
        return withoutAlpha

    def removeComments(self, java_file):
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

    def takeJavaClass(self):
        final = []
        current = []
        dic = {}
        with open(self.java_file_path, "r", encoding="utf-8") as java_file:
            text = self.removeComments(java_file)
            for line in text.splitlines():
                current = self.stringTokenizer(line)
                final += current
                for eachElem in current:
                    if eachElem in dic:
                        dic[eachElem] += 1
                    else:
                        dic[eachElem] = 1
            return dic

    def removeNotAlpha(self, tokens):
        rightOne = []
        for element in tokens:
            if (element.isalpha()):
                rightOne.append(element)
        return rightOne

    @staticmethod
    def splitDict(dict):
        regexForCCSplit = '.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)'
        split_dic = {}
        for key in dict:
            matches = re.finditer(regexForCCSplit, key)
            # Per ogni split in ottenuto dalla regex
            for m in matches:
                # se lo split è già nel dizionario allora aggiorna solo il valore, altrimenti inseriscilo
                if m.group(0).lower() in split_dic:
                    split_dic[m.group(0).lower()] += dict[key]
                else:
                    split_dic[m.group(0).lower()] = dict[key]
        return split_dic

    @staticmethod
    def mergeDict(dict1, dict2):
        for key in dict2:
            if key in dict1:
                dict1[key] += dict2[key]
            else:
                dict1[key] = dict2[key]
        return dict1