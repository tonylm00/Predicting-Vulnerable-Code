from json import JSONDecodeError
from os import read
from unittest.mock import call

import pytest
from Dataset2.mining_results_asa.creator_csv_for_ASA import main

class TestMainCreatorCSVForASA:

    VULN_DICT_NAME = 'ASA_dict.csv'
    RULES_DICT_NAME = 'ASA_rules_dict.csv'
    RESULT_CSV_NAME = "csv_ASA_final.csv"

    VULN_DICT_DATA_REP = "[{'type': 'VULNERABILITY', 'rule': 'java:S2386', 'component': '17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java', 'class': 'neg'}, {'type': 'VULNERABILITY', 'rule': 'java:S2386', 'component': '17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java', 'class': 'neg'}]"

    VULN_DICT_DATA_NO_REP = "[{'type': 'VULNERABILITY', 'rule': 'java:S2386', 'component': '17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java', 'class': 'neg'}]"

    VULN_DICT_DATA_NO_REP_MORE_RECORDS = "[{'type': 'VULNERABILITY', 'rule': 'java:S2386', 'component': '17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java', 'class': 'neg'}, {'type': 'VULNERABILITY', 'rule': 'java:S2658', 'component': '17ce298b98df08e413e81a61f209912ea7fe36ef/ShutdownMonitor.java', 'class': 'neg'}]"

    VULN_DICT_DATA_NO_REP_DOUBLE_CLASS = "[{'type': 'VULNERABILITY', 'rule': 'java:S2386', 'component': '17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java', 'class': 'neg'}, {'type': 'VULNERABILITY', 'rule': 'java:S2386', 'component': '17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java', 'class': 'pos'}]"

    VULN_DICT_DATA_REP_DOUBLE_CLASS = "[{'type': 'VULNERABILITY', 'rule': 'java:S2386', 'component': '17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java', 'class': 'neg'}, {'type': 'VULNERABILITY', 'rule': 'java:S2386', 'component': '17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java', 'class': 'neg'}," \
                                      "{'type': 'VULNERABILITY', 'rule': 'java:S2658', 'component': '17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java', 'class': 'neg'}, {'type': 'VULNERABILITY', 'rule': 'java:S2658', 'component': '17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java', 'class': 'pos'}]"


    RULES_DICT_DATA_WITH_MATCH = "{'java:S2386':0}"

    RULES_DICT_DATA_WITH_NO_MATCH = "{'java:S2386':0, 'java:S2658':0}"

    def assert_environment(self, mock_files, oracle_items, oracle_rules):
        expected_vuln_dict_calls = [
            call(self.VULN_DICT_NAME, 'r+'),  # Expecting the file to be opened
            call().read()  # Expecting the file's read method to be called
        ]

        expected_rules_dict_calls = [
            call(self.RULES_DICT_NAME, 'r+'),  # Expecting the file to be opened
            call().read()  # Expecting the file's read method to be called
        ]

        expected_calls = [call('Name')]  # Initial opening bracket

        for rule in oracle_rules:
            expected_calls.append(call(", " + rule))

        expected_calls.append(call(', class'))
        expected_calls.append(call('\n'))

        for component, frequencies, vuln_class in oracle_items:

            expected_calls.append(call('\n'))
            expected_calls.append(call(component))

            for freq in frequencies:
                expected_calls.append(call(', ' + str(freq)))

            expected_calls.append(call(', ' + vuln_class))

        mock_files[self.RESULT_CSV_NAME]().write.assert_has_calls(expected_calls)
        mock_files[self.VULN_DICT_NAME].assert_has_calls(expected_vuln_dict_calls)
        mock_files[self.RULES_DICT_NAME].assert_has_calls(expected_rules_dict_calls)


    @pytest.mark.parametrize('mock_op_fail', [VULN_DICT_NAME], indirect=True )
    @pytest.mark.parametrize('mock_files', [
        {RULES_DICT_NAME: RULES_DICT_DATA_WITH_NO_MATCH}
    ], indirect=True)
    def test_case_1_csv_for_ASA(self, mock_op_fail, mock_files):
        try:
            main()
        except FileNotFoundError as e:
            assert self.VULN_DICT_NAME in str(e)

            # Ensure the exception is correctly raised
            assert isinstance(e, FileNotFoundError)
        else:
            # Fail the test if no exception is raised
            pytest.fail("Expected FileNotFoundError was not raised")

    @pytest.mark.parametrize('mock_op_fail', [RULES_DICT_NAME], indirect=True)
    @pytest.mark.parametrize('mock_files', [
        {VULN_DICT_NAME: VULN_DICT_DATA_NO_REP_MORE_RECORDS}
    ], indirect=True)
    def test_case_2_csv_for_ASA(self, mock_op_fail, mock_files):
        try:
            main()
        except FileNotFoundError as e:
            assert self.RULES_DICT_NAME in str(e)

            # Ensure the exception is correctly raised
            assert isinstance(e, FileNotFoundError)
        else:
            # Fail the test if no exception is raised
            pytest.fail("Expected FileNotFoundError was not raised")

    @pytest.mark.parametrize('mock_op_permission_err', [RESULT_CSV_NAME], indirect=True)
    def test_case_3_csv_for_ASA(self, mock_op_permission_err):
        with pytest.raises(PermissionError):
            main()

    @pytest.mark.parametrize('mock_files', [
        {VULN_DICT_NAME: VULN_DICT_DATA_NO_REP + "}", RULES_DICT_NAME: RULES_DICT_DATA_WITH_NO_MATCH}
    ], indirect=True)
    def test_case_4_csv_for_ASA(self, mock_files):
        with pytest.raises(JSONDecodeError):
            main()

    @pytest.mark.parametrize('mock_files', [
        {VULN_DICT_NAME: VULN_DICT_DATA_NO_REP_MORE_RECORDS , RULES_DICT_NAME: RULES_DICT_DATA_WITH_MATCH + '}'}
    ], indirect=True)
    def test_case_5_csv_for_ASA(self, mock_files):
        with pytest.raises(JSONDecodeError):
            main()

    @pytest.mark.parametrize('mock_files', [
        {VULN_DICT_NAME: VULN_DICT_DATA_NO_REP, RULES_DICT_NAME: RULES_DICT_DATA_WITH_MATCH, RESULT_CSV_NAME: None}
    ], indirect=True)
    def test_case_6_csv_for_ASA(self, mock_files):
        main()


        oracle_items = [
            ('17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java', [1], 'neg')
        ]

        oracle_rules = ['java:S2386']

        self.assert_environment(mock_files, oracle_items, oracle_rules)


    @pytest.mark.parametrize('mock_files', [
        {VULN_DICT_NAME: VULN_DICT_DATA_REP, RULES_DICT_NAME: RULES_DICT_DATA_WITH_MATCH, RESULT_CSV_NAME: None}
    ], indirect=True)
    def test_case_7_csv_for_ASA(self, mock_files):
        main()

        oracle_items = [
            ('17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java', [2], 'neg')
        ]

        oracle_rules = [
            'java:S2386'
        ]

        self.assert_environment(mock_files, oracle_items, oracle_rules)



    @pytest.mark.parametrize('mock_files', [
        {VULN_DICT_NAME: VULN_DICT_DATA_NO_REP_MORE_RECORDS, RULES_DICT_NAME: RULES_DICT_DATA_WITH_NO_MATCH, RESULT_CSV_NAME: None}
    ], indirect=True)
    def test_case_8_csv_for_ASA(self, mock_files):
        main()

        oracle_items = [
            ('17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java', [1,0], 'neg'),
            ('17ce298b98df08e413e81a61f209912ea7fe36ef/ShutdownMonitor.java', [0,1], 'neg')
        ]

        oracle_rules = [
            'java:S2386',
            'java:S2658'
        ]

        self.assert_environment(mock_files, oracle_items, oracle_rules)

    @pytest.mark.parametrize('mock_files', [
        {VULN_DICT_NAME: "[]", RULES_DICT_NAME: RULES_DICT_DATA_WITH_NO_MATCH,
         RESULT_CSV_NAME: None}
    ], indirect=True)
    def test_case_9_csv_for_ASA(self, mock_files):
        main()

        oracle_rules = [
            'java:S2386',
            'java:S2658'
        ]

        self.assert_environment(mock_files, [], oracle_rules)


    @pytest.mark.parametrize('mock_files', [
        {VULN_DICT_NAME: VULN_DICT_DATA_NO_REP, RULES_DICT_NAME: "{}",
         RESULT_CSV_NAME: None}
    ], indirect=True)
    def test_case_10_csv_for_ASA(self, mock_files):
        main()

        oracle_items = [
            ('17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java', [], 'neg')
        ]

        self.assert_environment(mock_files, oracle_items, [])


    @pytest.mark.parametrize('mock_files', [
        {VULN_DICT_NAME: '[]', RULES_DICT_NAME: "{}",
         RESULT_CSV_NAME: None}
    ], indirect=True)
    def test_case_11_csv_for_ASA(self, mock_files):
        main()

        self.assert_environment(mock_files, [], [])




