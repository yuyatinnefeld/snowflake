# Access Control

```sql
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
```
