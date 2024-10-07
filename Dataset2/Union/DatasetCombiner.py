import pandas as pd


class DatasetCombiner:
    def __init__(self, output_file_name):
        self.output = output_file_name

    def merge(self, *csv_files):
        if len(csv_files) < 2:
            raise ValueError("Devi passare almeno due file CSV per il merge.")

        dfs = [pd.read_csv(csv, delimiter=',', encoding="utf-8") for csv in csv_files]

        # Rimozione degli spazi
        dfs = [df.map(lambda x: x.strip() if isinstance(x, str) else x) for df in dfs]

        for df in dfs:
            if 'NameClass' in df.columns:
                df.rename(columns={'NameClass': 'Name'}, inplace=True)

        merged_df = dfs[0]
        for df in dfs[1:]:
            try:
                merged_df = pd.merge(merged_df, df, on=["Name"], how="outer")
            except ValueError as e:
                print(f"Errore durante il merge: {e}")
                return

        merged_df.fillna(int(0), inplace=True)
        merged_df.to_csv(self.output, index=False)



