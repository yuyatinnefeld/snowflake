# SnowSQL
SnowSQL is the Snowflake command line client

## SnowSQL Install
1. download snowsql installer (Linux)
```sql
 curl -O https://sfc-repo.snowflakecomputing.com/snowsql/bootstrap/1.2/linux_x86_64/snowsql-1.2.17-linux_x86_64.bash

```
run the installer
```sql
bash snowsql-1.2.17-linux_x86_64.bash
```

2. login
```sql
snowsql -a <account_identifier> -u <user_name>
snowsql -a hh66057.europe-west4.gcp -u YUYA
```
When prompted by SnowSQL, enter the password for your Snowflake user.

## Create Snowflake objects

### Create a database
```sql
* SnowSQL * v1.2.17
Type SQL statements or !help
YUYA#COMPUTE_WH@(no database).(no schema)> CREATE OR REPLACE DATABASE sf_tuts;
```

### Create a table
```sql
CREATE OR REPLACE TABLE emp_basic (
  first_name STRING ,
  last_name STRING ,
  email STRING ,
  streetaddress STRING ,
  city STRING ,
  start_date DATE
  );
```

### Create a WH
```sql
CREATE OR REPLACE WAREHOUSE sf_tuts_wh WITH
  WAREHOUSE_SIZE='X-SMALL'
  AUTO_SUSPEND = 180
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED=TRUE;

SELECT CURRENT_WAREHOUSE();
```

## Stage the data files

1. open the linkt to download the simple files
https://docs.snowflake.com/en/_downloads/34f4a66f56d00340f8f7a92acaccd977/getting-started.zip

2. unzip the files
```bash
mv getting-started.zip snowsql/data
cd data
unzip getting-started.zip
```

3. Execute PUT to upload data to the table
```sql
YUYA#SF_TUTS_WH@SF_TUTS.PUBLIC> PUT file://data/employees0*.csv @sf_tuts.public.%emp_basic;
YUYA#SF_TUTS_WH@SF_TUTS.PUBLIC> LIST @sf_tuts.public.%emp_basic;
```

## Copy data into the target table
```sql
COPY INTO emp_basic
  FROM @%emp_basic
  FILE_FORMAT = (type = csv field_optionally_enclosed_by='"')
  PATTERN = '.*employees0[1-5].csv.gz'
  ON_ERROR = 'skip_file';
```

## Query data from the table
```sql
-- Select all columns
SELECT * FROM emp_basic;

-- Insert records
INSERT INTO emp_basic VALUES
  ('Clementine','Adamou','cadamou@sf_tuts.com','10510 Sachs Road','Klenak','2017-9-22') ,
  ('Marlowe','De Anesy','madamouc@sf_tuts.co.uk','36768 Northfield Plaza','Fangshan','2017-1-26');

-- Query to show new employees
SELECT first_name, last_name, DATEADD('day',90,start_date) FROM emp_basic WHERE start_date <= '2017-01-01';
```

## Delete table, database, warehouse

```sql
DROP TABLE IF EXISTS emp_basic;
DROP DATABASE IF EXISTS sf_tuts;
DROP WAREHOUSE IF EXISTS sf_tuts_wh;
```

## Exit Snowsql
```sql
!exit
```

## Create a connection file

1. create config file
```sql
cd ~/.snowsql/
```

2. update config file

```bash
vi config

[connections.my_test_connection]
accountname = hh66057.europe-west4.gcp
username = YUYA
password = xxxxxxxxxxxxxxxxxxxx
dbname = sf_tuts
schemaname = public
warehousename = sf_tuts_wh
```

3. create a connection
```bash
snowsql -c my_test_connection
```