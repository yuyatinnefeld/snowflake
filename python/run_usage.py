from util_connection import create_connection, create_cursor, close_cursor
from util_account_usage import account_usage


if __name__ == '__main__':
    conn = create_connection()
    cs = create_cursor(conn)
    cs.execute("USE ROLE ACCOUNTADMIN")
    cs.execute("USE DATABASE DEMO_DB")

    account_usage_kpis= ["DATABASES", "QUERY_HISTORY", "DATABASE_STORAGE_USAGE_HISTORY", "TASK_HISTORY", "WAREHOUSE_LOAD_HISTORY","DATA_TRANSFER_HISTORY", 
    "LOAD_HISTORY", "STAGE_STORAGE_USAGE_HISTORY", "STORAGE_USAGE", "TABLE_STORAGE_METRICS", "WAREHOUSE_EVENTS_HISTORY", "WAREHOUSE_METERING_HISTORY"]

    #TODO: 2. save the df as json
    # [save_df_as_json(usage_category) for usage_category in account_usage_kpis]


    df = account_usage(cs, "WAREHOUSE_LOAD_HISTORY")
    #TODO: 1. create a save_df_as_json(usage_category)

    print(df.head())

    close_cursor(conn)
    conn.close()