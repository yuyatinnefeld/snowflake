# dbt + Snwoflake
![GitHub Logo](/images/dbt-dag-final.png)

dbt is a data transformation tool that enables data analysts and engineers to transform, test and document data in the cloud data warehouse.

## Info
- https://docs.getdbt.com/docs/available-adapters
- https://quickstarts.snowflake.com/guide/data_engineering_with_dbt/#0

## install dbt (pip)

```bash
python -m venv dbt-env
source dbt-env/bin/activate
pip install wheel
pip install dbt
pip install --upgrade dbt
```

More Info: https://docs.getdbt.com/dbt-cli/installation#pip

## configure dbt project
1. initialize a dbt project (project name = "dbt_hol")
```bash
dbt init dbt_hol
cd dbt_hol
```

2. create role / DB / warehouse for dbt project
```sql
create warehouse dbt_dev_wh
create warehouse dbt_prod_wh

create database dbt_hol_dev
create database dbt_hol_prod

create role dbt_dev_role
create role dbt_prod_role

grant role dbt_dev_role to role ACCOUNTADMIND;
grant role dbt_prod_role to role ACCOUNTADMIND;

grant role dbt_dev_role to user yuya;
grant role dbt_prod_role to user yuya;

grant usage on database dbt_hol_dev to role dbt_dev_role;
grant usage on database dbt_hol_prod to role dbt_prod_role;
```

3. update ~/.dbt/profiles.yml
```bash
vi ~/.dbt/profiles.yml
```

update the variables
```yml
dbt_hol:
  target: dev
  outputs:
    dev:
      type: snowflake
      ######## Please replace with your Snowflake account name
      account: hh66057.europe-west4.gcp
      
      user: YUYA
      ######## Please replace with your Snowflake dbt user password
      password: xxxx
      
      role: ACCOUNTADMIN
      database: dbt_hol_dev
      warehouse: dbt_dev_wh
      schema: public
      threads: 200
    prod:
      type: snowflake
      ######## Please replace with your Snowflake account name
      account: hh66057.europe-west4.gcp
      
      user: YUYA
      ######## Please replace with your Snowflake dbt user password
      password: xxxx
      
      role: ACCOUNTADMIN
      database: dbt_hol_prod
      warehouse: dbt_prod_wh
      schema: public
      threads: 200
```

4. update the dbt_project.yml

- project nema: dbt_hol
- replace "name", "profile", "models" fro my_new_project to dbt_hol

```yml

######## Please replace with your project name > dbt_hol
name: 'dbt_hol'
version: '1.0.0'
config-version: 2

######## Please replace with your project name > dbt_hol
profile: 'dbt_hol'


source-paths: ["models"]
analysis-paths: ["analysis"]
test-paths: ["tests"]
data-paths: ["data"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
    - "target"
    - "dbt_modules"


models:
######## Please replace with your project name > dbt_hol
  dbt_hol:
      example:
          materialized: view
```

5. run the debug command  

```bash
cd /dbt/dbt_hol
dbt debug
```

6. test run
```bash
dbt run
```

7. verify the result
open Snowflake
```sql
use database dbt_hol_dev
use schema public
select * from my_first_dbt_model
```

## get the source data

1. open the snowflake market place
- Change role to ACCOUTNADMIN
- Preview App > Data > Market place

2. search "Knoema Economy Atlas" / "Economy Data Atlas"

3. get the data
- DB Name: KNOEMA_ECONOMY_DATA_ATLAS

4. verify the DB
- DB Name: KNOEMA_ECONOMY_DATA_ATLAS
- Schema: ECONOMY

```sql
SELECT * 
  FROM "KNOEMA_ECONOMY_DATA_ATLAS"."ECONOMY"."DATASETS"
 WHERE "DatasetName" ILIKE 'US Stock%'
    OR "DatasetName" ILIKE 'Exchange%Rates%';

SELECT * 
  FROM KNOEMA_ECONOMY_DATA_ATLAS.ECONOMY.USINDSSP2020 LIMIT 10

```
## Build the dbt pipeline

1. create the dirs
```bash
cd dbt_hol
mkdir models/l10_staging
mkdir models/l20_transform
mkdir models/l30_mart
mkdir models/tests
```

2. update the dbt_project.yml

```yml

name: 'dbt_hol'
version: '1.0.0'
config-version: 2
....

models:
  dbt_hol:
      # Applies to all files under models/example/
      example:
          materialized: view
          +enabled: false
      l10_staging:
          schema: l10_staging
          materialized: view
      l20_transform:
          schema: l20_transform
          materialized: view
      l30_mart:
          schema: l30_mart
          materialized: view

```

3. create customize schema naming macros

```bash
vi macros/call_me_anything_you_want.sql
```

```sql
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}
        {{ default_schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}


{% macro set_query_tag() -%}
  {% set new_query_tag = model.name %} {# always use model name #}
  {% if new_query_tag %}
    {% set original_query_tag = get_current_query_tag() %}
    {{ log("Setting query_tag to '" ~ new_query_tag ~ "'. Will reset to '" ~ original_query_tag ~ "' after materialization.") }}
    {% do run_query("alter session set query_tag = '{}'".format(new_query_tag)) %}
    {{ return(original_query_tag)}}
  {% endif %}
  {{ return(none)}}
{% endmacro %}
```

4. create a packages.yml

```bash
cd dbt_hol
vi packages.yml
```

use the pacakge from dbt hub
https://hub.getdbt.com/fishtown-analytics/dbt_utils/latest/

```bash
packages:
  - package: fishtown-analytics/dbt_utils
    version: 0.6.4
```

5. install the dbt plugins
```bash
dbt deps
```

## Build dbt pipelines - Stock trading history

1. create a models/l10_staging/sources.yml file

```yml
version: 2

sources:
  - name: knoema_economy_data_atlas
    database: knoema_economy_data_atlas
    schema: economy
    tables:
      - name: exratescc2018
      - name: usindssp2020

```
2. create models/l10_staging/base_knoema_fx_rates.sql file to transform the exratescc2018 table data
```sql
SELECT "Currency"        currency
     , "Currency Unit"   currency_unit
     , "Frequency"       frequency
     , "Date"            date
     , "Value"           value
     , 'Knoema.FX Rates' data_source_name
     , src.*
  FROM {{source('knoema_economy_data_atlas','exratescc2018')}}  src
```

3. create models/l10_staging/base_knoema_fx_rates.sql file to transform the usindssp2020 table data


```sql
SELECT "Company"                    Company
     , "Company Name"               Company_Name
     , "Company Symbol"             Company_Symbol
     , "Stock Exchange"             Stock_Exchange
     , "Stock Exchange Name"        Stock_Exchange_Name
     , "Indicator"                  Indicator
     , "Indicator Name"             Indicator_Name
     , "Units"                      Units
     , "Scale"                      Scale
     , "Frequency"                  Frequency
     , "Date"                       Date
     , "Value"                      Value
     , 'Knoema.Stock History' data_source_name
  FROM {{source('knoema_economy_data_atlas','usindssp2020')}}  src 
```

4. run all models tha are located in models/l10_staging
```bash
dbt run --model l10_staging --no-version-check
```


5. verify the result
the staging view is created

```sql
SELECT * 
  FROM dbt_hol_dev.l10_staging.base_knoema_stock_history 
 WHERE Company_Symbol ='AAPL' 
   AND date ='2021-03-01'
```

6. create the transform pipeline
- create a models/l20_transform/tfm_knoema_stock_history.sql file
- create a models/l20_transform/tfm_knoema_stock_history_alt.sql file
- create a models/l20_transform/tfm_stock_history.sql file

```bash
dbt run --model +tfm_stock_history --no-version-check
```
```sql
SELECT * 
  FROM dbt_hol_dev.l20_transform.tfm_stock_history
 WHERE company_symbol = 'AAPL'
   AND date = '2021-03-01'
```

## Build dbt pipelines - Currency exchange rates

1. create a models/l20_transform/tfm_fx_rates.sql file
2. create a models/l20_transform/tfm_stock_history_major_currency.sql file

3. dbt run
```bash
dbt run --model +tfm_stock_history_major_currency --no-version-check
```
### See the dbt documentation (DAG)

![GitHub Logo](/images/dbt-dag.png)
1. create a documentation 
```bash
dbt docs generate --no-version-check
dbt docs serve
```

2. open: http://localhost:8080

3. verify the result by snowflake
```sql
SELECT * 
  FROM dbt_hol_dev.l20_transform.tfm_stock_history_major_currency
 WHERE company_symbol = 'AAPL'
   AND date = '2021-03-01'
```

## Build dbt pipelines - Trading books

### upload small datasets
1. create a data/manual_book1.csv file
2. create a data/manual_book2.csv file
3. load the data into Snowflake
```bash
dbt seed --no-version-check
```

### create a new model to union the manual insert data
1. create a models/l20_transform/tfm_book.sql
2. deploy the model
```bash
dbt run -m tfm_book --no-version-check
```
3. create a model models/l20_transform/tfm_daily_position.sql
4. create a model models/l20_transform/tfm_daily_position_with_trades.sql
5. deploy the models
```bash
dbt run -m tfm_book+ --no-version-check
```

5. verify the result
```sql
SELECT * 
  FROM dbt_hol_dev.l20_transform.tfm_daily_position_with_trades
 WHERE trader = 'Jeff A.'
 ORDER BY date
```

## Build dbt pipelines - PnL calculation

1. creata a model models/l20_transform/tfm_trading_pnl.sql
2. create a model models/l30_mart/fct_trading_pnl.sql

### Create datamarts for the treasury, risk and finance departments
1. create a datamart models/l30_mart/fct_trading_pnl_finance_view.sql
2. create a datamart models/l30_mart/fct_trading_pnl_risk_view.sql
3. create a datamart models/l30_mart/fct_trading_pnl_treasury_view.sql

4. deploy the models
```bash
dbt run --no-version-check
```

5. check the dag
```bash
dbt docs serve
```

6. verify the result
```sql
SELECT * 
  FROM dbt_hol_dev.l30_mart.fct_trading_pnl
 WHERE trader = 'Jeff A.'
 ORDER by date
```

 ## create a simple visualization

1. Preview App > Worksheet enable > Worksheet + 
2. Role Switch to ACCOUNTADMIN
3. Paste the query

```sql
SELECT * 
  FROM dbt_hol_dev.l30_mart.fct_trading_pnl
 WHERE trader = 'Jeff A.'
 ORDER by date
```
4. Click on the play button

5. Change the column to PNL
![GitHub Logo](/images/sf-visualize.png)

## Testing, Deployment, Materializations

1. createa a test model

models/tests/data_quality_tests.yml

2. run test
```bash
dbt test --no-version-check
```
3. error will be displayed
```bash
17:30:15 | 6 of 6 FAIL 891295 unique_tfm_stock_history_company_symbol_date...... [FAIL 891295 in 110.76s]
```
4. update the data_quality_tests.yml
- reason: there are more than one stock exchanges
```yaml
version: 2

models:
  - name: tfm_fx_rates
    columns:
      - name: currency||date
        tests:
          - unique
          - not_null

  - name: tfm_book
    columns:
      - name: instrument
        tests:
          - not_null
          - relationships:
              to: ref('tfm_stock_history')
              field: company_symbol

  - name: tfm_stock_history
    columns:
      - name: company_symbol||date||stock_exchange_name
        tests:
          - not_null
          - unique
```

## Deploy into the prod
```bash
dbt seed --target=prod --no-version-check
dbt run  --target=prod --no-version-check
```
