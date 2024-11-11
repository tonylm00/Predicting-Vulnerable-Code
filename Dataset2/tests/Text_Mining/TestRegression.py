import pandas as pd

class TestRegression:
    def test_regression(self):
        # Carica i due CSV in due DataFrame
        df1 = pd.read_csv("csv_mining_final_old.csv")
        df2 = pd.read_csv("csv_mining_final.csv")

        # Rimuove il carattere "_" finale dai valori della colonna "Name" nel primo DataFrame
        df1["Name"] = df1["Name"].str.rstrip('_')

        # Ordina entrambi i DataFrame in base alla colonna "Name"
        df1 = df1.sort_values(by="Name").reset_index(drop=True)
        df2 = df2.sort_values(by="Name").reset_index(drop=True)

        # Confronta i due DataFrame
        assert df1.equals(df2)