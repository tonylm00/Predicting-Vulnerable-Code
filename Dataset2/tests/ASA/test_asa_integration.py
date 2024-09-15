
import pytest
from Dataset2.mining_results_asa.ASA_vulnerability_dict_generator import main as main_vuln
from Dataset2.mining_results_asa.rules_dict_generator_ASA import main as main_rule
from Dataset2.mining_results_asa.creator_csv_for_ASA import main as main_create


class TestASAIntegration:

    RES_NEG_NAME = 'RepositoryMining_ASAResults_neg.csv'
    RES_POS_NAME = 'RepositoryMining_ASAResults_pos.csv'
    DICT_VUL_NAME = 'ASA_dict.csv'
    DICT_RUL_NAME = 'ASA_rules_dict.csv'
    RESULT_CSV_NAME = "csv_ASA_final.csv"



    HEADER = '''severity\tupdateDate\tcomments\tline\tauthor\trule\tproject\teffort\tmessage\tcreationDate\ttype\ttags\tcomponent\tflows\torganization\ttextRange\tdebt\tkey\thash\tstatus'''

    DATA_NEG_NO_REP = HEADER + '''\nMINOR\t2020-07-03T17:57:05+0200\t\t71.0\t\tjava:S2386\tProva_Mining_Second_Part\t15min\t"Make this member ""protected""."\t2020-07-03T17:57:05+0200\tVULNERABILITY\t\tProva_Mining_Second_Part:src/RepositoryMining19/866/17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\tdefault-organization\t{startLine=71.0, endLine=71.0, startOffset=33.0, endOffset=59.0}\t15min\tAXMVa5NrkLspzIj1dA_E\tcef48bca33fc27fd295ef071f478584d\tOPEN'''

    DATA_POS_NO_REP = HEADER + '''\nMINOR\t2020-07-03T17:57:05+0200\t\t71.0\t\tjava:S2385\tProva_Mining_Second_Part\t15min\t"Make this member ""protected""."\t2020-07-03T17:57:05+0200\tVULNERABILITY\t\tProva_Mining_Second_Part:src/RepositoryMining19/866/17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\tdefault-organization\t{startLine=71.0, endLine=71.0, startOffset=33.0, endOffset=59.0}\t15min\tAXMVa5NrkLspzIj1dA_E\tcef48bca33fc27fd295ef071f478584d\tOPEN'''

    DATA_NEG_REP = HEADER + '''\nMINOR\t2020-07-03T17:57:05+0200\t\t71.0\t\tjava:S2386\tProva_Mining_Second_Part\t15min\t"Make this member ""protected""."\t2020-07-03T17:57:05+0200\tVULNERABILITY\t\tProva_Mining_Second_Part:src/RepositoryMining19/866/17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\tdefault-organization\t{startLine=71.0, endLine=71.0, startOffset=33.0, endOffset=59.0}\t15min\tAXMVa5NrkLspzIj1dA_E\tcef48bca33fc27fd295ef071f478584d\tOPEN
    MINOR\t2020-07-03T17:57:05+0200\t\t564.0\t\tjava:S2386\tProva_Mining_Second_Part\t10min\tUse a logger to log this exception.\t2020-07-03T17:57:05+0200\tVULNERABILITY\t\tProva_Mining_Second_Part:src/RepositoryMining19/866/17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\tdefault-organization\t{startLine=564.0, endLine=564.0, startOffset=14.0, endOffset=29.0}\t10min\tAXMVa5NrkLspzIj1dA_D\t2dc1665d31b37f9aa7408939a0365027\tOPEN'''

    DATA_POS_REP = HEADER + '''\nMINOR\t2020-07-03T17:57:05+0200\t\t71.0\t\tjava:S2385\tProva_Mining_Second_Part\t15min\t"Make this member ""protected""."\t2020-07-03T17:57:05+0200\tVULNERABILITY\t\tProva_Mining_Second_Part:src/RepositoryMining19/866/17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\tdefault-organization\t{startLine=71.0, endLine=71.0, startOffset=33.0, endOffset=59.0}\t15min\tAXMVa5NrkLspzIj1dA_E\tcef48bca33fc27fd295ef071f478584d\tOPEN
    MINOR\t2020-07-03T17:57:05+0200\t\t564.0\t\tjava:S2385\tProva_Mining_Second_Part\t10min\tUse a logger to log this exception.\t2020-07-03T17:57:05+0200\tVULNERABILITY\t\tProva_Mining_Second_Part:src/RepositoryMining19/866/17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\tdefault-organization\t{startLine=564.0, endLine=564.0, startOffset=14.0, endOffset=29.0}\t10min\tAXMVa5NrkLspzIj1dA_D\t2dc1665d31b37f9aa7408939a0365027\tOPEN'''

    DATA_NEG_WITH_NO_VULN = HEADER + '''\nMINOR\t2020-07-03T17:57:05+0200\t\t71.0\t\tjava:S2385\tProva_Mining_Second_Part\t15min\t"Make this member ""protected""."\t2020-07-03T17:57:05+0200\tBUG\t\tProva_Mining_Second_Part:src/RepositoryMining19/866/17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\tdefault-organization\t{startLine=71.0, endLine=71.0, startOffset=33.0, endOffset=59.0}\t15min\tAXMVa5NrkLspzIj1dA_E\tcef48bca33fc27fd295ef071f478584d\tOPEN'''

    DATA_POS_WITH_NO_VULN = HEADER + '''\nMINOR\t2020-07-03T17:57:05+0200\t\t71.0\t\tjava:S2386\tProva_Mining_Second_Part\t15min\t"Make this member ""protected""."\t2020-07-03T17:57:05+0200\tBUG\t\tProva_Mining_Second_Part:src/RepositoryMining19/866/17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\tdefault-organization\t{startLine=71.0, endLine=71.0, startOffset=33.0, endOffset=59.0}\t15min\tAXMVa5NrkLspzIj1dA_E\tcef48bca33fc27fd295ef071f478584d\tOPEN'''

    INVALID_DATA = HEADER + '''\nMINOR\t2020-07-03T17:57:05+0200\t\t71.0\t\tjava:S2386\tProva_Mining_Second_Part\t15min'''

    COMPONENT_NEG = '17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java'
    COMPONENT_POS = 'b2f5416fcd923457e73a1cad3b94d6e3e7bf24ba/ServletHandler.java'

    SHARED_COMPONENT = 'aa469239860778eb46e09dd7b390aee08f152480/QueryDataFunction.java'

    def execute_pipeline(self):
        main_vuln()
        main_rule()
        main_create()

    @pytest.mark.parametrize('manage_temp_input_files',
                             [{RES_POS_NAME}],
                             indirect=True)
    @pytest.mark.parametrize('remove_result_file', [{DICT_VUL_NAME, DICT_RUL_NAME, RESULT_CSV_NAME}], indirect=True)
    @pytest.mark.parametrize('prepare_content_data', [(
            {'file_name': RES_NEG_NAME, 'number_of_records': 1, 'is_rule_repeated': False,
             'component': COMPONENT_NEG},
            {'file_name': RES_POS_NAME, 'number_of_records': 1, 'is_rule_repeated': False,
             'component': COMPONENT_POS}
    )
    ], indirect=True)
    def test_case_1(self, manage_temp_input_files, prepare_content_data, remove_result_file):
        self.execute_pipeline()

        with open(self.RESULT_CSV_NAME, 'r') as file:
            lines = file.readlines()

        # Skip the header line and filter out any empty lines
        for line in lines[1:]:
            # Strip whitespace and continue if the line is empty
            if line.strip() == '':
                continue

            # Split the line by commas to get all elements
            elements = line.strip().split(',')

            # Get the last element
            last_element = elements[-1].strip()

            # Assert that the last element is 'neg'
            assert last_element == 'pos', f"Expected 'pos' but got '{last_element}' for line: {line.strip()}"

    @pytest.mark.parametrize('manage_temp_input_files',
                             [{RES_NEG_NAME}],
                             indirect=True)
    @pytest.mark.parametrize('remove_result_file', [{DICT_VUL_NAME, DICT_RUL_NAME, RESULT_CSV_NAME}], indirect=True)
    @pytest.mark.parametrize('prepare_content_data', [(
            {'file_name': RES_NEG_NAME, 'number_of_records': 1, 'is_rule_repeated': False,
             'component': COMPONENT_NEG},
            {'file_name': RES_POS_NAME, 'number_of_records': 1, 'is_rule_repeated': False,
             'component': COMPONENT_POS}
    )
    ], indirect=True)
    def test_case_2(self, prepare_content_data, manage_temp_input_files, remove_result_file):
        self.execute_pipeline()

        with open(self.RESULT_CSV_NAME, 'r') as file:
            lines = file.readlines()

        # Skip the header line and filter out any empty lines
        for line in lines[1:]:
            # Strip whitespace and continue if the line is empty
            if line.strip() == '':
                continue

            # Split the line by commas to get all elements
            elements = line.strip().split(',')

            # Get the last element
            last_element = elements[-1].strip()

            # Assert that the last element is 'neg'
            assert last_element == 'neg', f"Expected 'neg' but got '{last_element}' for line: {line.strip()}"

    @pytest.mark.parametrize('manage_temp_input_files',
                             [{RES_NEG_NAME, RES_POS_NAME}],
                             indirect=True)
    @pytest.mark.parametrize('remove_result_file', [{DICT_VUL_NAME, DICT_RUL_NAME, RESULT_CSV_NAME}], indirect=True)
    @pytest.mark.parametrize('prepare_content_data', [(
            {'file_name': RES_NEG_NAME, 'number_of_records': 1, 'is_rule_repeated': False,
             'component': COMPONENT_NEG, 'no_vuln': True, 'is_invalid': True},
            {'file_name': RES_POS_NAME, 'number_of_records': 1, 'is_rule_repeated': False,
             'component': COMPONENT_POS, 'no_vuln': True}
    )
    ], indirect=True)
    def test_case_3(self, prepare_content_data, manage_temp_input_files, remove_result_file):
        with pytest.raises(IndexError):
            self.execute_pipeline()

    @pytest.mark.parametrize('manage_temp_input_files',
                             [{RES_NEG_NAME, RES_POS_NAME}],
                             indirect=True)
    @pytest.mark.parametrize('remove_result_file', [{DICT_VUL_NAME, DICT_RUL_NAME, RESULT_CSV_NAME}], indirect=True)
    @pytest.mark.parametrize('prepare_content_data', [(
            {'file_name': RES_NEG_NAME, 'number_of_records': 1, 'is_rule_repeated': False,
             'component': COMPONENT_NEG, 'no_vuln': True},
            {'file_name': RES_POS_NAME, 'number_of_records': 1, 'is_rule_repeated': False,
             'component': COMPONENT_POS, 'no_vuln': True,
             'is_invalid':True}
    )
    ], indirect=True)
    def test_case_4(self, prepare_content_data, manage_temp_input_files, remove_result_file):
        with pytest.raises(IndexError):
            self.execute_pipeline()

    @pytest.mark.parametrize('manage_temp_input_files',
                             [{RES_NEG_NAME, RES_POS_NAME}],
                             indirect=True)
    @pytest.mark.parametrize('remove_result_file', [{DICT_VUL_NAME, DICT_RUL_NAME, RESULT_CSV_NAME}], indirect=True)
    @pytest.mark.parametrize('prepare_content_data', [(
            {'file_name': RES_NEG_NAME, 'number_of_records': 1, 'is_rule_repeated': False,
             'component': COMPONENT_NEG, 'no_vuln':True},
            {'file_name': RES_POS_NAME, 'number_of_records': 1, 'is_rule_repeated': False,
             'component': COMPONENT_POS, 'no_vuln':True}
    )
    ], indirect=True)
    def test_case_5(self, prepare_content_data, manage_temp_input_files, remove_result_file):
        self.execute_pipeline()

        with open(self.RESULT_CSV_NAME, 'r') as file:
            text = file.read()

            assert text == "Name, class\n"


    @pytest.mark.parametrize('manage_temp_input_files',
                             [{RES_NEG_NAME, RES_POS_NAME}],
                             indirect=True)
    @pytest.mark.parametrize('remove_result_file', [{DICT_VUL_NAME, DICT_RUL_NAME, RESULT_CSV_NAME}], indirect=True)
    @pytest.mark.parametrize('prepare_content_data', [(
            {'file_name': RES_NEG_NAME, 'number_of_records': 2, 'is_rule_repeated': False,
             'component': COMPONENT_NEG},
            {'file_name': RES_POS_NAME, 'number_of_records': 2, 'is_rule_repeated': False,
             'component': COMPONENT_POS}
    )
    ], indirect=True)
    def test_case_6(self, prepare_content_data, manage_temp_input_files, remove_result_file):
        self.execute_pipeline()

        oracle_header = "Name, java:S2386, java:S2385, class\n"

        oracle_neg_output = "\n" + self.COMPONENT_NEG + ", 1, 1, neg"
        oracle_pos_output = "\n" + self.COMPONENT_POS + ", 1, 1, pos"

        with open(self.RESULT_CSV_NAME, 'r') as file:
            content = file.read()

        assert content == oracle_header + oracle_neg_output + oracle_pos_output


    @pytest.mark.parametrize('manage_temp_input_files',
                             [{RES_NEG_NAME, RES_POS_NAME}],
                             indirect=True)
    @pytest.mark.parametrize('remove_result_file', [{DICT_VUL_NAME, DICT_RUL_NAME, RESULT_CSV_NAME}], indirect=True)
    @pytest.mark.parametrize('prepare_content_data', [(
            {'file_name': RES_NEG_NAME, 'number_of_records': 2, 'is_rule_repeated': True,
             'component': COMPONENT_NEG},
            {'file_name': RES_POS_NAME, 'number_of_records': 2, 'is_rule_repeated': True,
             'component': COMPONENT_POS}
    )
    ], indirect=True)
    def test_case_7(self, prepare_content_data, manage_temp_input_files, remove_result_file):
        self.execute_pipeline()

        oracle_header = "Name, java:S2385, class\n"

        oracle_neg_output = "\n" + self.COMPONENT_NEG +  ", 2, neg"
        oracle_pos_output = "\n" + self.COMPONENT_POS +  ", 2, pos"

        with open(self.RESULT_CSV_NAME, 'r') as file:
            content = file.read()

        assert content == oracle_header + oracle_neg_output + oracle_pos_output

    @pytest.mark.parametrize('manage_temp_input_files',
                             [{RES_NEG_NAME, RES_POS_NAME}],
                             indirect=True)
    @pytest.mark.parametrize('remove_result_file', [{DICT_VUL_NAME, DICT_RUL_NAME, RESULT_CSV_NAME}], indirect=True)
    @pytest.mark.parametrize('prepare_content_data', [(
            {'file_name': RES_NEG_NAME, 'number_of_records': 0},
            {'file_name': RES_POS_NAME, 'number_of_records': 0}
    )
    ], indirect=True)
    def test_case_8(self, prepare_content_data, manage_temp_input_files, remove_result_file):
        self.execute_pipeline()

        with open(self.RESULT_CSV_NAME, 'r') as file:
            text = file.read()

            assert text == "Name, class\n"




























