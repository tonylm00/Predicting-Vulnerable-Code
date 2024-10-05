from DatasetCombiner import DatasetCombiner


def combine_tm_sm():
    combiner = DatasetCombiner("Union_TM_SM.csv")
    tm_csv = "../mining_results/csv_mining_final.csv"
    sm_csv = "../Software_Metrics/mining_results_sm_final.csv"
    combiner.merge(tm_csv, sm_csv)


def combine_tm_asa():
    combiner = DatasetCombiner("Union_TM_ASA.csv")
    tm_csv = "../mining_results/csv_mining_final.csv"
    asa_csv = "../mining_results_asa/csv_ASA_final.csv"
    combiner.merge(tm_csv, asa_csv)


def combine_sm_asa():
    combiner = DatasetCombiner("Union_SM_ASA.csv")
    sm_csv = "../Software_Metrics/mining_results_sm_final.csv"
    asa_csv = "../mining_results_asa/csv_ASA_final.csv"
    combiner.merge(sm_csv, asa_csv)


def total_combination():
    combiner = DatasetCombiner("3COMBINATION.csv")
    tm_csv = "../mining_results/csv_mining_final.csv"
    sm_csv = "../Software_Metrics/mining_results_sm_final.csv"
    asa_csv = "../mining_results_asa/csv_ASA_final.csv"
    combiner.merge(sm_csv, tm_csv, asa_csv)
