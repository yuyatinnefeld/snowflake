# GCP + Snowflake

- Info:
https://docs.snowflake.com/en/user-guide/data-load-gcs-config.html

## Initial Snowflake Setup
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
desc storage integration gcp_yt_private_int
```

## Grant the Service Account Permissions to Access Bucket Objects
copy the created STORAGE_GCP_SERVICE_ACCOUNT 
(ex. euppnhvuuo@gcpeuropewest4-1-88d1.iam.gserviceaccount.com)

GCP > IAM > ROLE > Create Role
Title: Snowflake Bucket Role
Add Permissions > Filter:
    -- storage.buckets.get
    -- storage.buckets.delete
    -- storage.buckets.create
    -- storage.buckets.list

## Assigning the Custom Role to the Cloud Storage Service Account

1. Cloud Storage
2. Select a bucket
3. Click SHOW INFO PANEL
4. Click Add Member

- Service Account: euppnhvuuo@gcpeuropewest4-1-88d1.iam.gserviceaccount.com
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
- Add member: euppnhvuuo@gcpeuropewest4-1-88d1.iam.gserviceaccount.com
- Role:
  - Cloud KMS CrytoKey Encryptor
  - Cloud KMS CrytoKey Decryptor

## Create an External Stage

GRANT CREATE STAGE ON SCHEMA yt_schema TO ROLE accountadmin;
GRANT USAGE ON INTEGRATION gcp_yt_private_int TO ROLE accountadmin;

```sql
USE SCHEMA yt_db.public;

CREATE STAGE my_gcs_stage
  URL = 'gcs://yygcplearning-snowflake/'
  STORAGE_INTEGRATION = gcp_int
  FILE_FORMAT = my_csv_format;
```
  
