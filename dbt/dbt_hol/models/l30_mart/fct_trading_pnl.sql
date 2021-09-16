{{ 
config(
	  materialized='incremental'
	  , tags=["Fact Data"]
	  ) 
}}
SELECT src.*
  FROM {{ref('tfm_trading_pnl')}} src

{% if is_incremental() %}
  -- this filter will only be applied on an incremental run
 WHERE (trader, instrument, date, stock_exchange_name) NOT IN (select trader, instrument, date, stock_exchange_name from {{ this }})

{% endif %}