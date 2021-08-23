# Roll back a table

```sql
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
```
