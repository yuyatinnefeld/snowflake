import snowflake.connector
from decouple import config
from util_ddl import (create_cursor, close_cursor, create, create_table, drop)
from util_dml import (insert, insert_csv, select)


user = config('SF_USER')
password = config('SF_PASSWORD')
account = config('SF_ACCOUNT')

if __name__ == '__main__':
    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        session_parameters={
        'QUERY_TAG': 'python:yt:local',
        }
    )

    cs = create_cursor(conn)
    cs.execute("USE ROLE ACCOUNTADMIN")
    cs.execute("USE DATABASE DEMO_DB")

    ### CREATE WAREHOUSE / DB / SCHEMA / TABLE###
    #object_type = WAREHOUSE, DATABASE
    #create(cs, "WAREHOUSE", "demo_warehouse_python") 
    #drop(cs, "WAREHOUSE", "demo_warehouse_python")
    #create(cs, "SCHEMA", "demo_schema_python") 
    #drop(cs, "SCHEMA", "demo_schema_python") 
    #create_table(cs, "TABLE", "demo_table_python")
    #drop(cs, "TABLE", "demo_table_python") 

    ### MANUEL INSERT ###
    #val = "VALUES(123, 'test string1'),(456, 'test string2')" 
    #insert(cs, "demo_table_python", val)
    
    ### CSV INSERT ###
    #input_file="data/input_data2021*"
    #insert_csv(cs, "demo_table_python", input_file)
    
    ### SELECT ###
    #select(cs, "demo_table_python")
    close_cursor(conn)
    conn.close()