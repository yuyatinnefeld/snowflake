#!/usr/bin/env python
import snowflake.connector
from decouple import config


user = config('SF_USER')
password = config('SF_PASSWORD')
account = config('SF_ACCOUNT')

conn = snowflake.connector.connect(
    user=user,
    password=password,
    account=account,
    session_parameters={
        'QUERY_TAG': 'python yt local query',
    }
)

cs = conn.cursor()
try:
    cs.execute("SELECT current_version()")
    one_row = cs.fetchone()
    print("✨ connection successfully ✨")
    print(one_row[0])
finally:
    cs.close()

conn.close()