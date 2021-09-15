import pandas as pd


def store_df_to_csv(df:pd.DataFrame, file_name:str):
    file_path = f"data/output/{file_name}.csv"
    df.to_csv(file_path, sep=',', encoding='utf-8')

def store_df_to_json(df:pd.DataFrame, file_name:str):
    file_path = f"data/output/{file_name}.json"
    df.to_json(file_path)

def store_df_to_xlsx(df:pd.DataFrame, file_name:str):
    file_path = f"data/output/{file_name}.xlsx"
    df.to_excel(file_path)