import csv
import os
import shutil
import stat
from unittest.mock import patch
import pandas as pd

import json

from Dataset2.mining_results_asa.rules_dict_generator_ASA import main
import pytest

   
@pytest.mark.parametrize('manage_test_files', ['RepositoryMining_ASAResults_neg.csv'], indirect=True)
@pytest.mark.parametrize('remove_result_file', ['ASA_rules_dict.csv'], indirect=True)
def test_case_1_rules(manage_test_files, remove_result_file):
    # Run the main function
    main()

    # Path to your .tsv file
    file_path = 'RepositoryMining_ASAResults_pos.csv'

    # Read the .tsv file into a DataFrame
    df = pd.read_csv(file_path, sep='\t')

    # Extract the 'rule' column values
    rules_set = set(df['rule'].tolist())

    result_file_name = "ASA_rules_dict.csv"

    assert os.path.exists(result_file_name)

    with open(result_file_name, "r+") as result_file:
        rules_dict=json.loads(result_file.read().replace("\'","\""))
        result_rules_set = set(rules_dict.keys())

        assert rules_set == result_rules_set



   
@pytest.mark.parametrize('manage_test_files', ['RepositoryMining_ASAResults_pos.csv'], indirect=True)
@pytest.mark.parametrize('remove_result_file', ['ASA_rules_dict.csv'], indirect=True)
def test_case_2_rules(manage_test_files, remove_result_file):
    # Run the main function
    main()

    # Path to your .tsv file
    file_path = 'RepositoryMining_ASAResults_neg.csv'

    # Read the .tsv file into a DataFrame
    df = pd.read_csv(file_path, sep='\t')

    # Extract the 'rule' column values
    rules_set = set(df['rule'].tolist())

    result_file_name = "ASA_rules_dict.csv"

    assert os.path.exists(result_file_name)

    with open(result_file_name, "r+") as result_file:
        rules_dict = json.loads(result_file.read().replace("\'", "\""))
        result_rules_set = set(rules_dict.keys())

        assert rules_set == result_rules_set

   
@pytest.mark.parametrize('invalidate_format', ['RepositoryMining_ASAResults_neg.csv'], indirect=True)
@pytest.mark.parametrize('remove_result_file', ['ASA_rules_dict.csv'], indirect=True)
def test_case_3_rules(invalidate_format, remove_result_file):
    with pytest.raises(IndexError):
        main()

   
@pytest.mark.parametrize('invalidate_format', ['RepositoryMining_ASAResults_pos.csv'], indirect=True)
@pytest.mark.parametrize('remove_result_file', ['ASA_rules_dict.csv'], indirect=True)
def test_case_4_rules(invalidate_format, remove_result_file):
    with pytest.raises(IndexError):
        main()

   
@pytest.mark.parametrize('invalidate_content', [{'RepositoryMining_ASAResults_neg.csv', 'RepositoryMining_ASAResults_pos.csv'}], indirect=True)
@pytest.mark.parametrize('remove_result_file', ['ASA_rules_dict.csv'], indirect=True)
def test_case_5_rules(invalidate_content, remove_result_file):
    main()

    result_file_name = "ASA_rules_dict.csv"

    with open(result_file_name, "r+") as result_file:
        rules_dict = json.loads(result_file.read().replace("\'", "\""))
        assert len(rules_dict) == 0

   
@pytest.mark.parametrize('remove_result_file', ['ASA_rules_dict.csv'], indirect=True)
def test_case_6_rules(remove_result_file):
    # Run the main function
    main()

    # Path to your .tsv file
    file_path_neg = 'RepositoryMining_ASAResults_neg.csv'

    # Read the .tsv file into a DataFrame
    df_neg = pd.read_csv(file_path_neg, sep='\t')

    # Extract the 'rule' column values
    rules_neg = df_neg['rule'].tolist()

    # Path to your .tsv file
    file_path_pos = 'RepositoryMining_ASAResults_pos.csv'

    # Read the .tsv file into a DataFrame
    df_pos = pd.read_csv(file_path_pos, sep='\t')

    # Extract the 'rule' column values
    rules_pos = df_pos['rule'].tolist()

    rules_set = set(rules_neg + rules_pos)

    result_file_name = "ASA_rules_dict.csv"

    with open(result_file_name, "r+") as result_file:
        rules_dict = json.loads(result_file.read().replace("\'", "\""))
        result_rules_set = set(rules_dict.keys())

        assert rules_set == result_rules_set

   
@pytest.mark.parametrize('remove_content', [{'RepositoryMining_ASAResults_neg.csv', 'RepositoryMining_ASAResults_pos.csv'}], indirect=True)
@pytest.mark.parametrize('remove_result_file', ['ASA_rules_dict.csv'], indirect=True)
def test_case_7_rules(remove_content, remove_result_file):
    main()

    result_file_name = "ASA_rules_dict.csv"

    with open(result_file_name, "r+") as result_file:
        rules_dict = json.loads(result_file.read().replace("\'", "\""))

        assert len(rules_dict) == 0














