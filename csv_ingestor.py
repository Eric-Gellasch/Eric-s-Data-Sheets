import pandas as pd

def load_csv(file_path):
    df = pd.read_csv(file_path)
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    print(df.head())  
    return df