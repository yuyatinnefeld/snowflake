# Terraform + Snowflake

## Info
- https://quickstarts.snowflake.com/guide/terraforming_snowflake/index.html?index=..%2F..index#0

## Create a service user for terraform

### create an RSA key for Authentication

```bash
cd ~/.ssh
openssl genrsa -out snowflake_tf_snow_key 4096
openssl rsa -in snowflake_tf_snow_key -pubout -out snowflake_tf_snow_key.pub

# copy the public key
cat ~/.ssh/snowflake_tf_snow_key.pub
```

### Create the user in Snowflake
1. Role change: ACCOUNTADMIN 
2. Copy the public key (starting after the PUBLIC KEY header, and stopping just before the PUBLIC KEY footer.)

Execute both of the following SQL statements to create the User and grant it access to the SYSADMIN and SECURITYADMIN roles needed for account management.

```sql
USE ROLE accountadmin; 

CREATE USER "tf-snow" RSA_PUBLIC_KEY='xxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Kxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Zxxxxxxxxxxxxxxxxx==' DEFAULT_ROLE=PUBLIC MUST_CHANGE_PASSWORD=FALSE;

GRANT ROLE SYSADMIN TO USER "tf-snow";
GRANT ROLE SECURITYADMIN TO USER "tf-snow";
```

## Setup Terraform Authentication

### Check the YOUR_ACCOUNT_LOCATOR and YOUR_SNOWFLAKE_REGION_ID
```sql
SELECT current_account() as YOUR_ACCOUNT_LOCATOR, current_region() as YOUR_SNOWFLAKE_REGION_ID;
```
ACCOUNT_LOCATOR: ex. HH66057
SNOWFLAKE_REGION_ID: GCP_EUROPE_WEST4

### Add Account Information to Environment

```bash
YOUR_ACCOUNT_LOCATOR="HH66057"
YOUR_REGION="EUROPE-WEST4.GCP" #REGION.CLOUDPROVIDER
export SNOWFLAKE_USER="tf-snow"
export SNOWFLAKE_PRIVATE_KEY_PATH="~/.ssh/snowflake_tf_snow_key"
export SNOWFLAKE_ACCOUNT=${YOUR_ACCOUNT_LOCATOR}
export SNOWFLAKE_REGION=${YOUR_REGION}
```

## Create a terraform main.tf
```bash
cd terraform/your-project
vi main.tf
```

```bash
terraform {
  required_providers {
    snowflake = {
      source  = "chanzuckerberg/snowflake"
      version = "0.22.0"
    }
  }
}

provider "snowflake" {
  role     = "SYSADMIN"
}

resource "snowflake_database" "db" {
  name = "TF_DEMO"
}

resource "snowflake_warehouse" "warehouse" {
  name           = "TF_DEMO"
  warehouse_size = "xsmall"

  auto_suspend = 60
}
```
### run terraform project
```bash
terraform init
terraform plan
terraform apply
```

### add resources
```bash
....

resource "snowflake_schema" "schema" {
   database = snowflake_database.db.name
   name     = "TF_DEMO"
   is_managed = false
}

```

### run terraform project
```bash
terraform init
terraform plan
terraform apply
```

### remove the project
```bash
terraform destroy
```