from util_connection import create_connection, create_cursor, close_cursor
from util_account_usage import account_usage, get_account_usage_views
from util_store_df import store_df_to_csv, store_df_to_json, store_df_to_xlsx
import snowflake.connector.cursor as cursor


def df_extract_store(cs:cursor.SnowflakeCursor, file_name:str):
    df = account_usage(cs, file_name)
    store_df_to_csv(df, file_name)

if __name__ == '__main__':
    conn = create_connection()
    cs = create_cursor(conn)
    account_usage_kpis= get_account_usage_views(cs)
    
    #[df_extract_store(cs, file_name) for file_name in account_usage_kpis]

    close_cursor(conn)
    conn.close()