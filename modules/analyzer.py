import duckdb


class Analyzer:
    df: duckdb.DuckDBPyRelation

    def __init__(self, df: duckdb.DuckDBPyRelation):
        self.df = df

    def describe(self):
        return self.df.describe()
