from util_connection import create_connection, create_cursor, close_cursor
from util_ddl import (create, create_table, drop)
from util_dml import (insert, insert_csv, select)
from user_management import (create_user, create_role, grant_user, listing_users, drop_user, drop_role)
from usage_warehouse import warehouse_metering_history, warehouse_events_history, warehouse_load_history


if __name__ == '__main__':
    conn = create_connection()
    cs = create_cursor(conn)


    #create_role(cs, "data_scientist")
    #grant_user(cs, "data_scientist", "yuya")
    #drop_role(cs, "data_scientist")

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