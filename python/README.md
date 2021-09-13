# Python + Snowflake

## create a python env

```bash
python -m venv venv
source ./venv/bin/activate #Mac
venv\Scripts\activate #Windows

# install snowflake connector
pip install --upgrade snowflake-connector-python

# install decouple
pip install python-decouple
```

## create a .env text file on your repo
```bash
vi .env

SF_USER="<Your UserName>"
SF_ACCOUNT="Account ID.Region.Cloud Provider" # ex. hh00897.europe-west4.gcp
SF_PASSWORD="<Your Snowflake Password>"
```

## create a conn_validate.py file
```python
#!/usr/bin/env python
import snowflake.connector
from decouple import config


user = config('SF_USER')
password = config('SF_PASSWORD')
account = config('SF_ACCOUNT')

conn = snowflake.connector.connect(
    user=user,
    password=password,
    account=account
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
```
## track the query history with the query tag

1. add a session parameter
```bash
conn = snowflake.connector.connect(
    user=user,
    password=password,
    account=account,
    session_parameters={
        'QUERY_TAG': 'python yt local query',
    }
)
```

2. check the query history by snowflake

## create a main.py, util_ddl.py and util_dml.py


