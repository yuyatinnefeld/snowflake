from decouple import config
import snowflake.connector
import snowflake.connector.connection as conn
import snowflake.connector.cursor as cursor

#TODO: this must OBJECT! to avoid call every time the conn

def create_connection():
    user = config('SF_USER')
    password = config('SF_PASSWORD')
    account = config('SF_ACCOUNT')

    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        session_parameters={
        'QUERY_TAG': 'python:yt:local',
        }
    )
    return conn
    
def create_cursor(conn: conn.SnowflakeConnection) -> cursor.SnowflakeCursor:
    try:
        cs = conn.cursor()
        print("✨ connection successful ✨")
        cs.execute("USE ROLE ACCOUNTADMIN")
        return cs
    except:
        print("connection not successful")


def close_cursor(cs):
    cs.close()

