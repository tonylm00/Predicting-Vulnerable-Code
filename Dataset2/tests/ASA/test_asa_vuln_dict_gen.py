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

    DATA_NEG = HEADER + '''\nMINOR\t2020-07-03T17:57:05+0200\t\t71.0\t\tjava:S2386\tProva_Mining_Second_Part\t15min\t"Make this member ""protected""."\t2020-07-03T17:57:05+0200\tVULNERABILITY\t\tProva_Mining_Second_Part:src/RepositoryMining19/866/17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\tdefault-organization\t{startLine=71.0, endLine=71.0, startOffset=33.0, endOffset=59.0}\t15min\tAXMVa5NrkLspzIj1dA_E\tcef48bca33fc27fd295ef071f478584d\tOPEN
        MINOR\t2020-07-03T17:57:05+0200\t\t564.0\t\tjava:S1148\tProva_Mining_Second_Part\t10min\tUse a logger to log this exception.\t2020-07-03T17:57:05+0200\tVULNERABILITY\t\tProva_Mining_Second_Part:src/RepositoryMining19/866/17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\tdefault-organization\t{startLine=564.0, endLine=564.0, startOffset=14.0, endOffset=29.0}\t10min\tAXMVa5NrkLspzIj1dA_D\t2dc1665d31b37f9aa7408939a0365027\tOPEN'''

    DATA_POS = HEADER + '''\nMINOR\t2020-07-03T17:57:05+0200\t\t71.0\t\tjava:S2385\tProva_Mining_Second_Part\t15min\t"Make this member ""protected""."\t2020-07-03T17:57:05+0200\tVULNERABILITY\t\tProva_Mining_Second_Part:src/RepositoryMining19/866/17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\tdefault-organization\t{startLine=71.0, endLine=71.0, startOffset=33.0, endOffset=59.0}\t15min\tAXMVa5NrkLspzIj1dA_E\tcef48bca33fc27fd295ef071f478584d\tOPEN
            MINOR\t2020-07-03T17:57:05+0200\t\t564.0\t\tjava:S1149\tProva_Mining_Second_Part\t10min\tUse a logger to log this exception.\t2020-07-03T17:57:05+0200\tVULNERABILITY\t\tProva_Mining_Second_Part:src/RepositoryMining19/866/17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\tdefault-organization\t{startLine=564.0, endLine=564.0, startOffset=14.0, endOffset=29.0}\t10min\tAXMVa5NrkLspzIj1dA_D\t2dc1665d31b37f9aa7408939a0365027\tOPEN'''

    DATA_NEG_WITH_NO_VULN = HEADER + '''\nMINOR\t2020-07-03T17:57:05+0200\t\t71.0\t\tjava:S2385\tProva_Mining_Second_Part\t15min\t"Make this member ""protected""."\t2020-07-03T17:57:05+0200\tBUG\t\tProva_Mining_Second_Part:src/RepositoryMining19/866/17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\tdefault-organization\t{startLine=71.0, endLine=71.0, startOffset=33.0, endOffset=59.0}\t15min\tAXMVa5NrkLspzIj1dA_E\tcef48bca33fc27fd295ef071f478584d\tOPEN'''

    DATA_POS_WITH_NO_VULN = HEADER + '''\nMINOR\t2020-07-03T17:57:05+0200\t\t71.0\t\tjava:S2386\tProva_Mining_Second_Part\t15min\t"Make this member ""protected""."\t2020-07-03T17:57:05+0200\tBUG\t\tProva_Mining_Second_Part:src/RepositoryMining19/866/17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\tdefault-organization\t{startLine=71.0, endLine=71.0, startOffset=33.0, endOffset=59.0}\t15min\tAXMVa5NrkLspzIj1dA_E\tcef48bca33fc27fd295ef071f478584d\tOPEN'''


    @patch('os.listdir', return_value=[RES_POS_NAME])
    @pytest.mark.parametrize('mock_files', [
        {RES_NEG_NAME: '', RES_POS_NAME: DATA_POS, DICT_NAME: None}
    ], indirect=True)
    def test_case_1_vuln(self, mock_lisdir, mock_files):

        main()

        oracle = [
            '{\'type\': \'VULNERABILITY\', \'rule\': \'java:S2385\', ' \
              '\'component\': \'17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\', \'class\': \'pos\'}',
            '{\'type\': \'VULNERABILITY\', \'rule\': \'java:S1149\', ' \
            '\'component\': \'17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\', \'class\': \'pos\'}'
        ]

        expected_pos_call = call(self.RES_POS_NAME, 'r')

        expected_calls = [call('[')]

        for i in range(len(oracle)):
            if i>0:
                expected_calls.append(call(','))
            expected_calls.append(call(oracle[i]))

        expected_calls.append(call(']'))

        mock_files[self.RES_NEG_NAME].assert_not_called()
        mock_files[self.RES_POS_NAME].assert_has_calls([expected_pos_call])
        mock_files[self.DICT_NAME]().write.assert_has_calls(expected_calls)



    @patch('os.listdir', return_value=[RES_NEG_NAME])
    @pytest.mark.parametrize('mock_files', [
        {RES_NEG_NAME: DATA_NEG, RES_POS_NAME: '', DICT_NAME: None}
    ], indirect=True)
    def test_case_2_vuln(self, mock_lisdir, mock_files):

        main()

        oracle = [
            '{\'type\': \'VULNERABILITY\', \'rule\': \'java:S2386\', ' \
            '\'component\': \'17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\', \'class\': \'neg\'}',
            '{\'type\': \'VULNERABILITY\', \'rule\': \'java:S1148\', ' \
            '\'component\': \'17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\', \'class\': \'neg\'}'
        ]

        expected_neg_call = call(self.RES_NEG_NAME, 'r')

        expected_calls = [call('[')]

        for i in range(len(oracle)):
            if i > 0:
                expected_calls.append(call(','))
            expected_calls.append(call(oracle[i]))

        expected_calls.append(call(']'))

        mock_files[self.RES_POS_NAME].assert_not_called()
        mock_files[self.RES_NEG_NAME].assert_has_calls([expected_neg_call])
        mock_files[self.DICT_NAME]().write.assert_has_calls(expected_calls)

    @pytest.mark.parametrize('mock_op_permission_err', [DICT_NAME], indirect=True)
    def test_case_3_vuln(self, mock_op_permission_err):

        with pytest.raises(PermissionError):
            main()


    @pytest.mark.parametrize('invalidate_format', [RES_NEG_NAME], indirect=True)
    @pytest.mark.parametrize('mock_files', [
        {RES_NEG_NAME: '', RES_POS_NAME: DATA_POS, DICT_NAME: None}
    ], indirect=True)
    @patch('os.listdir', return_value=[RES_NEG_NAME, RES_POS_NAME])
    def test_case_4_vuln(self, mock_listdir, invalidate_format, mock_files):

        with pytest.raises(IndexError):
            main()

    @pytest.mark.parametrize('invalidate_format', [RES_POS_NAME], indirect=True)
    @pytest.mark.parametrize('mock_files', [
        {RES_NEG_NAME: DATA_NEG, RES_POS_NAME: '', DICT_NAME: None}
    ], indirect=True)
    @patch('os.listdir', return_value=[RES_NEG_NAME, RES_POS_NAME])
    def test_case_5_vuln(self, mock_listdir, invalidate_format, mock_files):

        with pytest.raises(IndexError):
            main()


    @pytest.mark.parametrize('mock_files', [
        {RES_NEG_NAME: DATA_NEG_WITH_NO_VULN, RES_POS_NAME: DATA_POS_WITH_NO_VULN, DICT_NAME: None}
    ], indirect=True)
    @patch('os.listdir', return_value=[RES_NEG_NAME, RES_POS_NAME])
    def test_case_6_vuln(self, mock_listdir, mock_files):
        dict_mock = mock_files[self.DICT_NAME]()

        main()

        expected_neg_call = call(self.RES_NEG_NAME, 'r')
        expected_pos_call = call(self.RES_POS_NAME, 'r')

        mock_files[self.RES_NEG_NAME].assert_has_calls([expected_neg_call])
        mock_files[self.RES_POS_NAME].assert_has_calls([expected_pos_call])

        dict_mock.write.assert_has_calls([
            call('['),
            call(']')
        ])


    @pytest.mark.parametrize('mock_files', [
        {RES_NEG_NAME:DATA_NEG, RES_POS_NAME: DATA_POS, DICT_NAME: None}
    ], indirect=True)
    @patch('os.listdir', return_value=[RES_NEG_NAME, RES_POS_NAME])
    def test_case_7_vuln(self, mock_listdir, mock_files):

        main()

        oracle = [
            '{\'type\': \'VULNERABILITY\', \'rule\': \'java:S2386\', ' \
            '\'component\': \'17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\', \'class\': \'neg\'}',
            '{\'type\': \'VULNERABILITY\', \'rule\': \'java:S1148\', ' \
            '\'component\': \'17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\', \'class\': \'neg\'}',
            '{\'type\': \'VULNERABILITY\', \'rule\': \'java:S2385\', ' \
            '\'component\': \'17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\', \'class\': \'pos\'}',
            '{\'type\': \'VULNERABILITY\', \'rule\': \'java:S1149\', ' \
            '\'component\': \'17ce298b98df08e413e81a61f209912ea7fe36ef/Runner.java\', \'class\': \'pos\'}'
        ]

        expected_neg_call = call(self.RES_NEG_NAME, 'r')
        expected_pos_call = call(self.RES_POS_NAME, 'r')

        # Create the expected list of calls for dict_mock.write
        expected_calls = [call('[')]  # Initial opening bracket

        for i in range(len(oracle)):
            if i > 0:
                expected_calls.append(call(','))
            expected_calls.append(call(oracle[i]))

        expected_calls.append(call(']'))


        mock_files[self.RES_NEG_NAME].assert_has_calls([expected_neg_call])
        mock_files[self.RES_POS_NAME].assert_has_calls([expected_pos_call])
        mock_files[self.DICT_NAME]().write.assert_has_calls(expected_calls)

    @pytest.mark.parametrize('mock_files', [
        {RES_NEG_NAME: '', RES_POS_NAME: '', DICT_NAME: None}
    ], indirect=True)
    @patch('os.listdir', return_value=[RES_NEG_NAME, RES_POS_NAME])
    def test_case_8_vuln(self, mock_listdir, mock_files):
        dict_mock = mock_files[self.DICT_NAME]()

        main()

        expected_neg_call = call(self.RES_NEG_NAME, 'r')
        expected_pos_call = call(self.RES_POS_NAME, 'r')

        mock_files[self.RES_NEG_NAME].assert_has_calls([expected_neg_call])
        mock_files[self.RES_POS_NAME].assert_has_calls([expected_pos_call])

        dict_mock.write.assert_has_calls([
            call('['),
            call(']')
        ])















