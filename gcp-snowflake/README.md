# GCP + Snowflake Integration

- Info:
https://docs.snowflake.com/en/user-guide/data-load-gcs-config.html

## Create a GCP bucket and update a test csv file in the Cloud Storage

```bash
cat stackoverflow.csv

num age, webframeworkedwith
1, 20, Django
2, 40, Kafka
3, 30, React
4, 10, Hadoop


gsutil mb -p $DEVSHELL_PROJECT_ID \
    -c ${STORAGE_CLASS} \
    -l ${REGION} \
    gs://${BUCKET_NAME}/

gsutil cp ${LOCAL_FILE_PATH}/* gs://${BUCKET_NAME}
```

## Setting Up the Snowflake Environment
```sql

-- create a dwh server / db / schema
create or replace warehouse analytics_wh with warehouse_size = 'small' warehouse_type = 'standard' 
  auto_suspend = 600 auto_resume = true;
create or replace database yt_db;
create or replace schema yt_schema;

-- connect the dwh / db / schema
use role accountadmin;
use warehouse analytics_wh;
use schema public;
```
## Create a snowflake service account by Snowflake

```sql
-- create gcp storage integration (USER ROLE has to be ACCOUNTADMIN)

create storage integration gcp_int
type = external_stage
storage_provider = gcs
enabled = true
storage_allowed_locations = ('gcs://yygcplearning-snowflake/')

-- retrieve the cloud storage service account for your Snowflake Account
desc storage integration gcp_int
```
(ex. xxx@gcpeuropewest4-1-88d1.iam.gserviceaccount.com)

## Grant the Service Account Permissions to Access Bucket Objects

- GCP > IAM > ROLE > Create Role
- Title: Snowflake Bucket Role
- Add Permissions > Filter:
  - storage.buckets.get
  - storage.buckets.delete
  - storage.buckets.create
  - storage.buckets.list

## Assigning the Custom Role to the Cloud Storage Service Account

1. Cloud Storage
2. Select a bucket
3. Click SHOW INFO PANEL
4. Click Add Member

- Service Account: xxx@gcpeuropewest4-1-88d1.iam.gserviceaccount.com
- Role: Storage Object Admin + Snowflake Bucket Role (custom)

## Granting the Cloud Storage Service Account Permissions on the Cloud Key Management Service Cryptographic Keys
This step is required only if your GCS bucket is encrypted using a key stored in the Google Cloud Key Management Service (Cloud KMS).

- GCP > Security > Enable Key Management API 
- KEy ring name: snowflakekey
- location: europe
- key name: snowflakekey

### Add Snowflake Service Accoujnt in the Key Management 
- Select the created key
- Click SHOW INFO PANEL in the upper-right corner
- Add member: xxx@gcpeuropewest4-1-88d1.iam.gserviceaccount.com
- Role:
  - Cloud KMS CrytoKey Encryptor
  - Cloud KMS CrytoKey Decryptor

## Create an External Stage

grant create stage on schema public TO ROLE accountadmin;
grant usage on integration gcp_yt_private_int TO ROLE accountadmin;

```sql
use schema yt_db.public;

-- create a format for bucket gs file
create or replace file format stackoverflow_csv_format
  TYPE = 'CSV'
  FIELD_DELIMITER = ','
  SKIP_HEADER = 1;

-- create a stackoverflow stage 
create stage stackoverflow_gcp_stage
  url = 'gcs://yygcplearning-snowflake/stackoverflow.csv '
  storage_integration  = gcp_int
  file_format  = stackoverflow_csv_format
  
list @stackoverflow_gcp_stage;
```
  
## Stage data into the table
```sql
-- create a new table
create or replace table stackoverflow_tb (num integer, age integer, framework string);

-- data transport
copy into stackoverflow_tb from @stackoverflow_gcp_stage
file_format=stackoverflow_csv_format
force=true;

-- check the values
select * from stackoverflow_tb
```
