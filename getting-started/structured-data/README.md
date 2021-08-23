# Structured Data in Snowflake

```sql
/* *********************************************************************************** */
/* *** STRUCTURED DATA (CITIBIKE) **************************************************** */
/* *********************************************************************************** */

-- create a table
create table trips 
(tripduration integer,
  starttime timestamp,
  stoptime timestamp,
  start_station_id integer,
  start_station_name string,
  start_station_latitude float,
  start_station_longitude float,
  end_station_id integer,
  end_station_name string,
  end_station_latitude float,
  end_station_longitude float,
  bikeid integer,
  membership_type string,
  usertype string,
  birth_year integer,
  gender integer);

-- create a stage (stage = internal snowflake storage location)
create or replace stage citibike_trips url = 's3://snowflake-workshop-lab/citibike-trips';

-- show stage data
list @citibike_trips;

-- define the csv file format
create or replace file format csv type='csv'
  compression = 'auto' field_delimiter = ',' record_delimiter = '\n'
  skip_header = 0 field_optionally_enclosed_by = '\042' trim_space = false
  error_on_column_count_mismatch = false escape = 'none' escape_unenclosed_field = '\134'
  date_format = 'auto' timestamp_format = 'auto' null_if = ('');


-- import stage data into the db table
copy into trips from @citibike_trips file_format=csv;

-- create a small table
create table trips_test as (select * from trips limit 150);

-- delete the original table
truncate table trips;

-- create a dwh server "analytics_wh"
create or replace warehouse analytics_wh with warehouse_size = 'large' warehouse_type = 'standard' 
  auto_suspend = 600 auto_resume = true;

-- connect the db and the dwh server
use role sysadmin;
use warehouse analytics_wh;
use database citibike;
use schema public;


-- preview the 20 rows
select * from trips limit 20;


-- show the basic hourly statistics on Citi Bike usage
select date_trunc('hour', starttime) as "date",
count(*) as "num trips",
avg(tripduration)/60 as "avg duration (mins)", 
avg(haversine(start_station_latitude, start_station_longitude, end_station_latitude, end_station_longitude)) as "avg distance (km)" 
from trips_main
group by 1 order by 1;

-- show the monthly activity:
select monthname(starttime) as "month",
    count(*) as "num trips"
from trips_main
group by 1 order by 2 desc;
    

-- clone table 
create table trips_dev clone trips_test;
```