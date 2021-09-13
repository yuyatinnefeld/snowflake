# ML + Snowflake

## Downaload the query file
https://snowflake-workshop-lab.s3.amazonaws.com/Snowflake_Datarobot_VHOL_guides.sql

## execute the queries to setup dataset

## run docker container to use jupyter notebook
```bash
docker run -p 8888:8888 --name jupyter-notebook jupyter/datascience-notebook
```
## Install the snowflake-connector
```bash
pip install --upgrade snowflake-connector-python
```
```python
import snowflake.connector
```

## Verify the connection
```python
user = 'YUYA'
password = 'xxxxx'
account = 'hh66057.europe-west4.gcp'

conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        session_parameters={
        'QUERY_TAG': 'jupyter:yt'}
)

cs = conn.cursor()
result = cs.execute("SELECT DATABASE_ID, DATABASE_NAME, CREATED FROM snowflake.account_usage.databases;")

for row in result:
    print("#####################")
    print(row[0], row[1], row[2])

cs.close()
conn.close()
```

## Transform the SQL result to the dataframe
```python
import pandas as pd

cs = conn.cursor()
result = cs.execute("SELECT CUST_ID, CHURN, STATE, ACCOUNT_LENGTH, AREA_CODE, INTERNATIONAL,VOICEMAIL_PLAN, NUM_VM_MESSAGES, TOTAL_DAY_MINS, TOTAL_DAY_CALLS FROM CUSTOMER_DATA.PUBLIC.SCORING_DATA")


col = ['CUST_ID', 'CHURN', 'STATE', 'ACCOUNT_LENGTH', 'AREA_CODE', 'INTERNATIONAL', 'VOICEMAIL_PLAN'. 'NUM_VM_MESSAGES', 'TOTAL_DAY_MINS', 'TOTAL_DAY_CALLS']

df = pd.DataFrame(query, columns=col)
print(df)

cs.close()
conn.close()
```