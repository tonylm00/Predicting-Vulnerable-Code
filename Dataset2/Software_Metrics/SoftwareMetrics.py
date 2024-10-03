import csv
import os
import re

import lizard
import javalang
from tree_sitter import Language, Parser
import tree_sitter_java as tjava

# Carica la libreria Java per tree-sitter (assicurati che il file sia corretto)
JAVA_LANGUAGE = Language(tjava.language())

class SoftwareMetrics:
    def __init__(self, file_path, file_content):
        self.file_path = file_path
        #non sono utili al conteggio delle metriche, potrebbero anche compromettere il conteggio
        self.file_content = self.__remove_comments(file_content)
        self.metrics = {
            "CountLineCode": 0,
            "CountDeclClass": 0,
            "CountDeclFunction": 0,
            "CountLineCodeDecl": 0,
            "SumEssential": 0,
            "SumCyclomaticStrict": 0,
            "MaxEssential": 0,
            "MaxCyclomaticStrict": 0,
            "MaxNesting": 0
        }

    def __remove_comments(self, text):
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

    # problema con classi anonime
    def calculate_max_nesting(self):
        parser = Parser()
        parser.language = JAVA_LANGUAGE

        # Parsing del sorgente Java
        tree = parser.parse(bytes(self.file_content, "utf8"))
        root_node = tree.root_node

        # Suddividi il contenuto in righe per ottenere la posizione di fine
        righe = self.file_content.splitlines()
        nested_types = ['if_statement', 'for_statement', 'enhanced_for_statement', 'while_statement',
                        'switch_expression', 'do_statement', 'try_statement']

        max_nesting = 0

        # Funzione ricorsiva per attraversare l'albero AST
        def visit_node(node, current_nesting, else_flat=False):
            nonlocal max_nesting
            # Se il nodo corrente è una struttura nidificata
            if node.type in nested_types:
                if not else_flat:# and not in_finally:
                    current_nesting += 1
                else:
                    else_flat = False
                    #in_finally = False
                max_nesting = max(max_nesting, current_nesting)

            # Attraversiamo i figli del nodo
            for child in node.children:
                #if "finally" in child.type:
                #    in_finally = True
                if child.type == "else":
                    linea = child.start_point[0]
                    stripped_line = righe[linea].strip()
                    else_pos = stripped_line.find("else") + 4
                    next_linea = True
                    linea_corrente = linea
                    while next_linea and linea_corrente < len(righe):
                        stripped_line = righe[linea_corrente].strip()
                        if linea_corrente == linea:
                            stripped_line = stripped_line[else_pos:]
                        for char in stripped_line:
                            if char == " ":
                                continue
                            if char == "{":
                                else_flat = False
                                next_linea = False
                                break
                            if char != "{" and char != " ":
                                else_flat = True
                                next_linea = False
                                break
                        linea_corrente += 1
                visit_node(child, current_nesting, else_flat)

        # Chiamata iniziale al nodo radice
        visit_node(root_node, 0, False)

        return max_nesting


    def count_declarative_lines(self):
        # Inizializza il parser e setta la lingua Java
        parser = Parser()
        parser.language = JAVA_LANGUAGE

        # Parsing del sorgente Java
        tree = parser.parse(bytes(self.file_content, "utf8"))
        root_node = tree.root_node

        # Inizializza un set per memorizzare le linee con dichiarazioni (evita duplicati)
        linee_dichiarative = set()
        # Suddividi il contenuto in righe per ottenere la posizione di fine
        righe = self.file_content.splitlines()

        # Funzione ricorsiva per iterare i nodi dell'albero
        def visita_nodo(node):  # Identificare i tipi di dichiarazione che ci interessano
            linea_inizio = node.start_point[0]
            # Tree-sitter usa 0-index, quindi sommiamo 1
            if node.type in ('interface_declaration', 'enum_declaration', 'import_declaration', 'package_declaration',
                             'annotation_type_declaration', 'enum_constant'):
                # print(node.type + " - " + righe[node.start_point[0]].strip())
                # print(linea_inizio)
                linee_dichiarative.add(linea_inizio)
            elif node.type in ('class_declaration', 'constructor_declaration'):
                linea_fine = linea_inizio
                # print(node.type + " - " + righe[node.start_point[0]].strip())
                # print(linea_inizio)
                for i in range(linea_inizio, len(righe)):
                    if '{' in righe[i]:
                        linea_fine = i
                        if righe[i].strip() == '{':
                            linea_fine -= 1
                        break
                for l in range(linea_inizio, linea_fine + 1):
                    linee_dichiarative.add(l)
                    # print(l)
            elif node.type == 'method_declaration':
                linea_fine = linea_inizio
                # print(node.type + " - " + righe[node.start_point[0]].strip())
                # print(linea_inizio)
                # print(node.parent.type)
                if node.parent.type == 'interface_body' or "abstract" in righe[linea_inizio]:
                    search = ";"
                else:
                    search = "{"
                for i in range(linea_inizio, len(righe)):
                    if search in righe[i]:
                        linea_fine = i
                        if righe[i].strip() == search:
                            linea_fine -= 1
                        break
                for l in range(linea_inizio, linea_fine + 1):
                    linee_dichiarative.add(l)
                    # print(l)
            elif node.type in ('field_declaration', 'variable_declarator', 'costant_declaration'):
                linee_dichiarative.add(linea_inizio)
                # print(node.type + " - " + righe[node.start_point[0]].strip())
                # print(linea_inizio)
                if not righe[linea_inizio].strip().endswith(';'):
                    linea_fine = linea_inizio
                    for i in range(linea_inizio, len(righe)):
                        if ';' in righe[i]:
                            linea_fine = i
                            break
                    for l in range(linea_inizio, linea_fine + 1):
                        linee_dichiarative.add(l)
                        # print(l)
            elif node.type in ('annotation'):
                linee_dichiarative.add(linea_inizio)
                # print(node.type + " - " + righe[node.start_point[0]].strip())
                # print(linea_inizio)
                # Verifica se dopo l'annotazione c'è una parola chiave come `public`, `private`, ecc.
                linea_successiva = righe[linea_inizio]
                parole_chiave = ['public', 'private', 'protected', 'static', 'final', 'abstract', 'native',
                                 'synchronized']

                # Verifica se una qualsiasi parola chiave è contenuta nella riga
                if any(parola in linea_successiva for parola in parole_chiave):
                    # print(f"Annotazione breve terminata alla linea {linea_inizio}")
                    pass
                else:
                    # Calcola la linea di fine per annotazioni ramificate
                    parentesi_tonde_aperta = 0
                    parentesi_graffa_aperta = 0
                    linea_fine = linea_inizio

                    for i in range(linea_inizio, len(righe)):
                        # Controlliamo se troviamo parentesi aperte e chiuse per annotazioni complesse
                        parentesi_tonde_aperta += righe[i].count('(')
                        parentesi_tonde_aperta -= righe[i].count(')')
                        parentesi_graffa_aperta += righe[i].count('{')
                        parentesi_graffa_aperta -= righe[i].count('}')

                        # Se tutte le parentesi sono chiuse, l'annotazione è terminata
                        if parentesi_tonde_aperta <= 0 and parentesi_graffa_aperta <= 0:
                            linea_fine = i
                            break

                    # Aggiungi le linee fino alla linea finale
                    if linea_fine > linea_inizio:
                        # print(f"Linea finale stimata per l'annotazione: {linea_fine}")
                        for l in range(linea_inizio, linea_fine + 1):
                            linee_dichiarative.add(l)
                            # print(l)

            # Itera sui figli
            for child in node.children:
                visita_nodo(child)

        # Avvia la visita ricorsiva dall'albero radice
        visita_nodo(root_node)
        return len(linee_dichiarative)

    def count_lines_of_code(self):
        lines = self.file_content.splitlines()
        code_lines = 0
        for line in lines:
            if line.strip() == "":
                continue
            else:
                code_lines += 1
        return code_lines

    def count_method_declarations(self):
        parser = Parser()
        parser.language = JAVA_LANGUAGE

        # Parsing del sorgente Java
        tree = parser.parse(bytes(self.file_content, "utf8"))
        root_node = tree.root_node
        count = 0
        stack = [root_node]  # Inizia dal nodo radice
        while stack:
            current_node = stack.pop()

            # Controlla se il nodo è una dichiarazione di metodo, costruttore o lambda
            if current_node.type == 'method_declaration' or \
                    current_node.type == 'constructor_declaration' or \
                    current_node.type == 'lambda_expression':
                count += 1

            # Aggiungi i figli del nodo alla pila per continuare la ricerca
            stack.extend(current_node.children)

        return count

    def count_class_declarations(self):
        tree = javalang.parse.parse(self.file_content)
        count = 0
        # Conta il numero di classi e linee di codice
        for _, node in tree:
            if isinstance(node, javalang.tree.ClassDeclaration) or isinstance(node, javalang.tree.InterfaceDeclaration):
                count += 1
            elif isinstance(node, javalang.tree.ClassCreator):
                if node.body is not None:
                    count += 1
        return count

    def analyze(self):
        lizard_analysis = lizard.analyze_file.analyze_source_code(self.file_path, self.file_content)
        try:
            for lizard_function in lizard_analysis.function_list:
                self.metrics["SumCyclomaticStrict"] += lizard_function.cyclomatic_complexity
                self.metrics["MaxCyclomaticStrict"] = max(self.metrics["MaxCyclomaticStrict"],
                                                          lizard_function.cyclomatic_complexity)
                essential_complexity = 0
                self.metrics["SumEssential"] += essential_complexity
                self.metrics["MaxEssential"] = max(self.metrics["MaxEssential"], essential_complexity)

            self.metrics["CountLineCodeDecl"] = self.count_declarative_lines()
            self.metrics["MaxNesting"] = max(self.metrics["MaxNesting"], self.calculate_max_nesting())
            self.metrics["CountDeclClass"] = self.count_class_declarations()
            self.metrics["CountDeclFunction"] = self.count_method_declarations()
            self.metrics["CountLineCode"] = self.count_lines_of_code()

        except Exception as e:
            print(self.file_path, e)

        return self.metrics
