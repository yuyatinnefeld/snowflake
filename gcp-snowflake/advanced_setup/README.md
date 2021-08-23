# GCP + Snowflake Advanced Setup


## Create a GCP bucket and update a test csv file in the Cloud Storage

```bash
cat job.csv
first_name,last_name,email,gender,birthday,job
Rhys,Napleton,rnapleton0@economist.com,Female,1982-04-19 23:08:40,Financial Advisor
Klarika,Stot,kstot1@vinaora.com,Non-binary,1982-04-20 21:16:18,Geologist IV
....

gsutil cp ${LOCAL_FILE_PATH}/* gs://${BUCKET_NAME}
```

## Use the Env which is created in the getting-started session

If you do not create the dwh and create the gcp integration
[Visit here:](https://github.com/yuyatinnefeld/snowflake/tree/main/getting-started)


```sql
-- use the data warehouse
use warehouse analytics_wh

-- use the database ans schema
use schema yt_db.public

-- use the stage integration "gcp_int"
desc storage integration gcp_int
```

```sql
-- create a format for bucket gs file
create or replace file format csv_format
  TYPE = 'CSV'
  FIELD_DELIMITER = ','
  SKIP_HEADER = 1;

-- create a job stage 
create stage job_gcp_stage
  url = 'gcs://yygcplearning-snowflake/job.csv '
  storage_integration  = gcp_int
  file_format  = csv_format
  
list @job_gcp_stage;
```
  
## Stage data into the table
```sql
-- create a new table
create or replace table job_tb (
    first_name VARCHAR(50), 
    last_name VARCHAR(50),
    email VARCHAR(100),
    gender VARCHAR(50), 
    ts TIMESTAMP,
    job VARCHAR(100)
)


-- data transport
copy into job_tb from @job_gcp_stage
file_format=csv_format
force=true;

select * from job_tb
```

