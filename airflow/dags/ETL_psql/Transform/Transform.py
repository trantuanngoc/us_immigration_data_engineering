import pandas as pd
import os
from ETL_psql.Transform.Rename_col_df import column_dict


class TransformDf:
    def __init__(self, name, filePath=""):
        self.root_dir = "/opt/airflow/Input_data"
        self.write_dir = "/opt/airflow/Transformed_data"

        try:
            path = os.path.join(self.root_dir, filePath)
            self.df = pd.read_csv(path)
        except:
            self.df = pd.DataFrame()

        self.name = name

        self.clean()
        self.extra_var()
        self.transform()
        self.rename_col_df()
        self.write_csv()

    def extra_var(self):
        pass

    def get_primary_column(self):
        for col in self.df.columns:
            if "ID" in col: return col

    def clean(self):
        self.df.drop_duplicates(subset=[self.get_primary_column()], keep='first', inplace=True)

    def transform(self):
        pass

    def rename_col_df(self):
        self.df.rename(columns=column_dict[self.name], inplace=True)

    def write_csv(self):
        write_path = os.path.join(self.write_dir, self.name + ".csv")
        self.df.to_csv(write_path, index=False)
