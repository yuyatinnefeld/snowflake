
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

/* *********************************************************************************** */
/* *** SEMI-STRUCTURED DATA (WATHER) ************************************************* */
/* *********************************************************************************** */

-- create a new db
create database weather;

-- select the new db
use role sysadmin;
use warehouse compute_wh;
use database weather;
use schema public;

-- create a table with the semi-structured data 
-- semi-structured data => using the special column type called VARIANT
create table json_weather_data (v variant);

-- create a stage
create stage nyc_weather url = 's3://snowflake-workshop-lab/weather-nyc';

-- check the records
list @nyc_weather;

-- import the stage data into the table
copy into json_weather_data 
from @nyc_weather 
file_format = (type=json);

-- check the json data
select * from json_weather_data limit 10;

-- create a view
-- you can use SQL dot notation (v.city.coord.lat) to pull out

values at lower levels in the JSON hierarchy 
create view json_weather_data_view as
select
  v:time::timestamp as observation_time,
  v:city.id::int as city_id,
  v:city.name::string as city_name,
  v:city.country::string as country,
  v:city.coord.lat::float as city_lat,
  v:city.coord.lon::float as city_lon,
  v:clouds.all::int as clouds,
  (v:main.temp::float)-273.15 as temp_avg,
  (v:main.temp_min::float)-273.15 as temp_min,
  (v:main.temp_max::float)-273.15 as temp_max,
  v:weather[0].main::string as weather,
  v:weather[0].description::string as weather_desc,
  v:weather[0].icon::string as weather_icon,
  v:wind.deg::float as wind_dir,
  v:wind.speed::float as wind_speed
from json_weather_data
where city_id = 5128638;

-- see the view
select * from json_weather_data_view
where date_trunc('month',observation_time) = '2018-01-01' 
limit 20;

-- join the weater table and citibike table
select 
    weather as conditions
    ,count(*) as num_trips
from 
    citibike.public.trips_test 
left outer join json_weather_data_view
    on date_trunc('hour', observation_time) = date_trunc('hour', starttime)
where conditions is not null
group by 1 order by 2 desc;

-- delete the table
drop table json_weather_data;

-- show the 10 records of the deleted table
select * from json_weather_data limit 10;

-- restore the table = time travel
undrop table json_weather_data;

/* *********************************************************************************** */
/* *** ROLL BACK A TABLE **************************************************** */
/* *********************************************************************************** */

-- change the db
use database citibike;
use schema public;

-- update a column with the error value
update trips set start_station_name = 'oops';

-- show the result
select start_station_name as station
    ,count(*) as rides
from trips
group by 1
order by 2 desc
limit 20;


-- run query to find the query ID of the last UPDATE command
set query_id = 
(select query_id from 
table(information_schema.query_history_by_session (result_limit=>5)) 
where query_text like 'update%' order by start_time limit 1);

-- roll back the table status
create or replace table trips as
(select * from trips before (statement => $query_id));
        
-- see the result
select start_station_name as "station"
    ,count(*) as "rides"
from trips
group by 1
order by 2 desc
limit 20;


/* *********************************************************************************** */
/* *** Access Controls, account usage, and  Account Admin **************************** */
/* *********************************************************************************** */

-- change the role
use role accountadmin; 

-- create a role
create role junior_dataengineer;
grant role junior_dataengineer to user yuya;--YOUR_USER_NAME_GOES HERE;

-- change the role
use role junior_dataengineer;

-- change the role
use role accountadmin;

-- grant the junior_dataengineer db accesses
grant usage on database citibike to role junior_dataengineer;
grant usage on database weather to role junior_dataengineer;

-- change the role
use role junior_dba;

