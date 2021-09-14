import snowflake.connector.connection as conn
import snowflake.connector.cursor as cursor
import pandas as pd

def account_usage(cs:cursor.SnowflakeCursor, db_object:str) -> pd.DataFrame:
    show_col_query = f"SHOW COLUMNS IN TABLE SNOWFLAKE.ACCOUNT_USAGE.{db_object}"
    columns_schema = cs.execute(show_col_query)
    all_columns = [col[2] for col in columns_schema]
    query = f"SELECT * FROM  SNOWFLAKE.ACCOUNT_USAGE.{db_object}"
    result = cs.execute(query)
    df = pd.DataFrame(result, columns=all_columns)
    return df