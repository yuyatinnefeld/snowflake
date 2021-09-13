import snowflake.connector.connection as conn
import snowflake.connector.cursor as cursor

def listing_users(cs:cursor.SnowflakeCursor):
    print("USER LIST:")
    rows = cs.execute("SHOW USERS ")
    for row in rows:
        print(row[0])

def create_user(cs:cursor.SnowflakeCursor, user_name:str, password:str="password"):
    query = f"CREATE USER {user_name} PASSWORD={password} DEFAULT_ROLE = employee MUST_CHANGE_PASSWORD = TRUE;"
    cs.execute(query)

def create_role(cs:cursor.SnowflakeCursor, role:str="employee"):
    query = f"CREATE ROLE {role};"
    cs.execute(query)

def drop_role(cs:cursor.SnowflakeCursor, role:str):
    query = f"DROP ROLE {role};"
    cs.execute(query)

def grant_user(cs:cursor.SnowflakeCursor, role:str, user_name:str):
    query = f"GRANT ROLE {role} to user {user_name};"
    cs.execute(query)


def drop_user(cs:cursor.SnowflakeCursor, user_name:str):
    query = f"DROP USER {user_name};"
    cs.execute(query)
