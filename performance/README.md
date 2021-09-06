# Snowflake Performance Management 

In this project we will use GCS bucket

## Upload the job.csv file in the GCS bucket

```bash
cat job.csv
first_name,last_name,email,gender,birthday,job
Rhys,Napleton,rnapleton0@economist.com,Female,1982-04-19 23:08:40,Financial Advisor
Klarika,Stot,kstot1@vinaora.com,Non-binary,1982-04-20 21:16:18,Geologist IV
....

gsutil cp ${LOCAL_FILE_PATH}/* gs://${BUCKET_NAME}
```

## Use the Env which is created in the getting-started session

If you do not create the dwh and db
[Visit here:](https://github.com/yuyatinnefeld/snowflake/tree/main/getting-started)


If you do not make the Cloud storage snowflake integration
[Visit here:](https://github.com/yuyatinnefeld/snowflake/tree/master/gcp-snowflake)



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
  
## copy the stage data into the table
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

show tables like 'job_tb';
```

## Partitioning 


### Micro Partitioning for small/middle tables

In contrast to a data warehouse, the Snowflake Data Platform implements a powerful and unique form of partitioning, called micro-partitioning, that delivers all the advantages of static partitioning without the known limitations, as well as providing additional significant benefits.

Snowflake stores metadata about all rows stored in a micro-partition, including:

- The range of values for each of the columns in the micro-partition.
- The number of distinct values.
- Additional properties used for both optimization and efficient query processing.

Micro-partitioning is automatically performed on all Snowflake tables. Tables are transparently partitioned using the ordering of the data as it is inserted/loaded.

## Clustering
```sql

-- create a clustered table
CREATE OR REPLACE TABLE job_clustering_tb (
    first_name VARCHAR(50), 
    last_name VARCHAR(50),
    email VARCHAR(100),
    gender VARCHAR(50), 
    ts TIMESTAMP,
    job VARCHAR(100)
) 
CLUSTER BY (job);

SHOW TABLE LIKE 'job_clustering_tb';


-- update a table with the clutering
CREATE OR REPLACE TABLE emp_basic (
  first_name STRING ,
  last_name STRING ,
  email STRING ,
  streetaddress STRING ,
  city STRING ,
  start_date DATE
  );

ALTER TABLE emp_basic CLUSTER BY (TO_DATE(start_date));
```

### Automatic clustering
Automatic Clustering is the Snowflake service that seamlessly and continually manages all reclustering, as needed, of clustered tables.

```sql
ALTER TABLE job_clustering_tb SUSPEND RECLUSTER;
ALTER TABLE job_clustering_tb RESUME RECLUSTER;

show tables like 'job_clustering_tb';
```

## Clustering Keys for very large tables
Clustering keys are not intended for all tables. The size of a table, as well as the query performance for the table, should dictate whether to define a clustering key for the table

- In general, tables in the multi-terabyte (TB) range will experience the most benefit from clustering
- Also, before explicitly choosing to cluster a table, Snowflake strongly recommends that you test a representative set of queries on the table to establish some performance baselines.