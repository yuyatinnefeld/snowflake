# Snowflake Getting Started

## Create a DWH server and DB
```sql
-- create a dwh server / db / schema
create or replace warehouse analytics_wh with warehouse_size = 'small' warehouse_type = 'standard' 
  auto_suspend = 600 auto_resume = true;
create or replace database yt_db;
create or replace schema yt_schema;
```

## Connect to the server / db

```sql
use role accountadmin;
use warehouse analytics_wh;
use schema yt_schema;
```

## Create tables with the structured data
[More Info](https://github.com/yuyatinnefeld/snowflake/tree/main/getting-started/structured-data)

## Create tables with the unstructured data
[More Info](https://github.com/yuyatinnefeld/snowflake/tree/main/getting-started/unstructured-data)

## Rollback a table
[More Info](https://github.com/yuyatinnefeld/snowflake/tree/main/getting-started/rollback-table)

## Access Control
[More Info](https://github.com/yuyatinnefeld/snowflake/tree/main/getting-started/access-control)
