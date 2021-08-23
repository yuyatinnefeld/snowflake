# Unstructured / Semi-Structure Data in Snowflake

```sql
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

```
