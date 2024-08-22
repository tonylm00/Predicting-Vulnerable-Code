import csv
import os
import shutil
import stat
from unittest.mock import patch, call
import pandas as pd

import json

from Dataset2.mining_results_asa.ASA_vulnerability_dict_generator import main
import pytest

class TestMainASAVulnDictGen:

    RES_NEG_NAME = 'RepositoryMining_ASAResults_neg.csv'
    RES_POS_NAME = 'RepositoryMining_ASAResults_pos.csv'
    DICT_NAME = 'ASA_dict.csv'


    HEADER = '''severity\tupdateDate\tcomments\tline\tauthor\trule\tproject\teffort\tmessage\tcreationDate\ttype\ttags\tcomponent\tflows\torganization\ttextRange\tdebt\tkey\thash\tstatus'''

    DATA = HEADER + '''MINOR\t2020-07-03T17:57:05+0200\t\t71.0\t\tjava:S2386\tProva_Mining_Second_Part\t15min\t"Make this member ""protected""."\t2020-07-03T17:57:05+0200\tVULNERABILITY\t\tProva_Mining_Second_Part:src/RepositoryMining19/866/17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\tdefault-organization\t{startLine=71.0, endLine=71.0, startOffset=33.0, endOffset=59.0}\t15min\tAXMVa5NrkLspzIj1dA_E\tcef48bca33fc27fd295ef071f478584d\tOPEN
    MINOR\t2020-07-03T17:57:05+0200\t\t564.0\t\tjava:S1148\tProva_Mining_Second_Part\t10min\tUse a logger to log this exception.\t2020-07-03T17:57:05+0200\tVULNERABILITY\t\tProva_Mining_Second_Part:src/RepositoryMining19/866/17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\tdefault-organization\t{startLine=564.0, endLine=564.0, startOffset=14.0, endOffset=29.0}\t10min\tAXMVa5NrkLspzIj1dA_D\t2dc1665d31b37f9aa7408939a0365027\tOPEN'''

    DATA_WITH_NO_WULN = HEADER + '''MINOR\t2020-07-03T17:57:05+0200\t\t71.0\t\tjava:S2386\tProva_Mining_Second_Part\t15min\t"Make this member ""protected""."\t2020-07-03T17:57:05+0200\tBUG\t\tProva_Mining_Second_Part:src/RepositoryMining19/866/17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\tdefault-organization\t{startLine=71.0, endLine=71.0, startOffset=33.0, endOffset=59.0}\t15min\tAXMVa5NrkLspzIj1dA_E\tcef48bca33fc27fd295ef071f478584d\tOPEN'''

    @patch('os.listdir', return_value=['RepositoryMining_ASAResults_pos.csv'])
    @pytest.mark.parametrize('mock_files', [
        {RES_NEG_NAME: '', RES_POS_NAME: DATA, 'ASA_dict.csv': None}
    ], indirect=True)
    def test_case_1_vuln(self, mock_lisdir, mock_files):
        dicts = []

        lines = self.DATA.split('\n')

        for line in lines[1:]:
            dict_app = {}
            value_list = line.split("\t")
            dict_app["type"] = value_list[10]
            dict_app["rule"] = value_list[5]
            list_app = value_list[12].split("/")
            dict_app["component"] = list_app[3] + "/" + list_app[4]
            dict_app["class"] = 'pos'
            dicts.append(dict_app.copy())

        main()

        expected_pos_call = call('RepositoryMining_ASAResults_pos.csv', 'r')

        # Create the expected list of calls for dict_mock.write
        expected_calls = [call('[')]  # Initial opening bracket

        for i in range(0, len(dicts)):
            if i > 0:
                expected_calls.append(call(','))
            expected_calls.append(call(str(dicts[i])))

        expected_calls.append(call(']'))

        mock_files[self.RES_NEG_NAME].assert_not_called()
        mock_files[self.RES_POS_NAME].assert_has_calls([expected_pos_call])
        mock_files[self.DICT_NAME]().write.assert_has_calls(expected_calls)



    @patch('os.listdir', return_value=['RepositoryMining_ASAResults_neg.csv'])
    @pytest.mark.parametrize('mock_files', [
        {RES_NEG_NAME: DATA, RES_POS_NAME: '', DICT_NAME: None}
    ], indirect=True)
    def test_case_2_vuln(self, mock_lisdir, mock_files):
        dicts = []

        lines = self.DATA.split('\n')

        for line in lines[1:]:
            dict_app = {}
            value_list = line.split("\t")
            dict_app["type"] = value_list[10]
            dict_app["rule"] = value_list[5]
            list_app = value_list[12].split("/")
            dict_app["component"] = list_app[3] + "/" + list_app[4]
            dict_app["class"] = 'neg'
            dicts.append(dict_app.copy())

        main()

        expected_neg_call = call('RepositoryMining_ASAResults_neg.csv', 'r')

        # Create the expected list of calls for dict_mock.write
        expected_calls = [call('[')]  # Initial opening bracket

        for i in range(0, len(dicts)):
            if i > 0:
                expected_calls.append(call(','))
            expected_calls.append(call(str(dicts[i])))

        expected_calls.append(call(']'))

        mock_files[self.RES_POS_NAME].assert_not_called()
        mock_files[self.RES_NEG_NAME].assert_has_calls([expected_neg_call])
        mock_files[self.DICT_NAME]().write.assert_has_calls(expected_calls)

    @pytest.mark.parametrize('mock_op_permission_err', [DICT_NAME], indirect=True)
    def test_case_3_vuln(self, mock_op_permission_err):

        with pytest.raises(PermissionError):
            main()


    @pytest.mark.parametrize('invalidate_format', ['RepositoryMining_ASAResults_neg.csv'], indirect=True)
    @pytest.mark.parametrize('mock_files', [
        {RES_NEG_NAME: '', RES_POS_NAME: DATA, DICT_NAME: None}
    ], indirect=True)
    @patch('os.listdir', return_value=['RepositoryMining_ASAResults_neg.csv', 'RepositoryMining_ASAResults_pos.csv'])
    def test_case_4_vuln(self, mock_listdir, invalidate_format, mock_files):

        # The test function logic
        with pytest.raises(IndexError):
            main()

    @pytest.mark.parametrize('invalidate_format', ['RepositoryMining_ASAResults_pos.csv'], indirect=True)
    @pytest.mark.parametrize('mock_files', [
        {RES_NEG_NAME: DATA, RES_POS_NAME: '', DICT_NAME: None}
    ], indirect=True)
    @patch('os.listdir', return_value=['RepositoryMining_ASAResults_neg.csv', 'RepositoryMining_ASAResults_pos.csv'])
    def test_case_5_vuln(self, mock_listdir, invalidate_format, mock_files):

        # The test function logic
        with pytest.raises(IndexError):
            main()


    @pytest.mark.parametrize('mock_files', [
        {RES_NEG_NAME: DATA_WITH_NO_WULN, RES_POS_NAME: DATA_WITH_NO_WULN, DICT_NAME: None}
    ], indirect=True)
    @patch('os.listdir', return_value=['RepositoryMining_ASAResults_neg.csv', 'RepositoryMining_ASAResults_pos.csv'])
    def test_case_6_vuln(self, mock_listdir, mock_files):
        dict_mock = mock_files[self.DICT_NAME]()

        main()

        dict_mock.write.assert_has_calls([
            call('[')
        ])


    @pytest.mark.parametrize('mock_files', [
        {RES_NEG_NAME:DATA, RES_POS_NAME: DATA, DICT_NAME: None}
    ], indirect=True)
    @patch('os.listdir', return_value=['RepositoryMining_ASAResults_neg.csv', 'RepositoryMining_ASAResults_pos.csv'])
    def test_case_7_vuln(self, mock_listdir, mock_files):
        dicts = []

        lines = self.DATA.split('\n')

        for vuln_class in ['neg', 'pos']:
            for line in lines[1:]:
                dict_app = {}
                value_list = line.split("\t")
                dict_app["type"] = value_list[10]
                dict_app["rule"] = value_list[5]
                list_app = value_list[12].split("/")
                dict_app["component"] = list_app[3] + "/" + list_app[4]

                dict_app["class"] = vuln_class
                dicts.append(dict_app.copy())
        main()

        expected_neg_call = call('RepositoryMining_ASAResults_neg.csv', 'r')
        expected_pos_call = call('RepositoryMining_ASAResults_pos.csv', 'r')

        # Create the expected list of calls for dict_mock.write
        expected_calls = [call('[')]  # Initial opening bracket

        for i in range(0, len(dicts)):
            if i > 0:
                expected_calls.append(call(','))
            expected_calls.append(call(str(dicts[i])))

        expected_calls.append(call(']'))


        mock_files[self.RES_NEG_NAME].assert_has_calls([expected_neg_call])
        mock_files[self.RES_POS_NAME].assert_has_calls([expected_pos_call])
        mock_files[self.DICT_NAME]().write.assert_has_calls(expected_calls)

    @pytest.mark.parametrize('mock_files', [
        {RES_NEG_NAME: HEADER, RES_POS_NAME: HEADER, DICT_NAME: None}
    ], indirect=True)
    @patch('os.listdir', return_value=['RepositoryMining_ASAResults_neg.csv', 'RepositoryMining_ASAResults_pos.csv'])
    def test_case_8_vuln(self, mock_listdir, mock_files):
        dict_mock = mock_files[self.DICT_NAME]()

        main()

        dict_mock.write.assert_has_calls([
            call('[')
        ])















