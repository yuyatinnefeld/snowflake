import snowflake.connector.connection as conn
import snowflake.connector.cursor as cursor

def insert(cs:cursor.SnowflakeCursor, object_name:str, val:str):
    query = f"INSERT INTO {object_name}(col1, col2) {val}"
    cs.execute(query)

def insert_csv(cs:cursor.SnowflakeCursor, object_name:str, input_file:str):
    query = f"PUT file://{input_file}* @%{object_name}"
    cs.execute(query)
    cs.execute(f"COPY INTO {object_name}")

def select(cs:cursor.SnowflakeCursor, object_name:str):
    query = f"SELECT col1, col2 FROM {object_name} LIMIT 10"
    rows = cs.execute(query)
    for row in rows:
        print("col1 = ",row[0], "| col2 = ",row[1])

def close_cursor(cs):
    cs.close()

