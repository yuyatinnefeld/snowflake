import snowflake.connector.connection as conn
import snowflake.connector.cursor as cursor


def create(cs:cursor.SnowflakeCursor, object_type:str, object_name:str):
    query = f"CREATE {object_type} IF NOT EXISTS {object_name}"
    cs.execute(query)
    
def create_table(cs:cursor.SnowflakeCursor, object_type:str, object_name:str):
    query = f"CREATE OR REPLACE {object_type} {object_name}(col1 integer, col2 string)"
    cs.execute(query)
    
def drop(cs:cursor.SnowflakeCursor, object_type:str, object_name:str):
    query = f"DROP {object_type} {object_name}"
    cs.execute(query)

