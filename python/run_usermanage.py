from user_management import (create_user, create_role, grant_user, listing_users, drop_user, drop_role)
from util_connection import create_connection, create_cursor, close_cursor


if __name__ == '__main__':
    conn = create_connection()

    cs = create_cursor(conn)
    cs.execute("USE ROLE ACCOUNTADMIN")
    cs.execute("USE DATABASE DEMO_DB")

    listing_users(cs)
    users = ["user1", "user2", "user3", "user4", "user5", "user6"]

    #[create_user(cs, user) for user in users]
    #[drop_user(cs, user) for user in users]

    listing_users(cs)
    
    #create_role(cs, "data_scientist")
    #grant_user(cs, "data_scientist", "yuya")
    #drop_role(cs, "data_scientist")



    close_cursor(conn)
    conn.close()