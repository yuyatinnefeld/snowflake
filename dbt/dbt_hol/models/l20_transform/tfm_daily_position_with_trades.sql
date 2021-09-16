SELECT book
     , date
     , trader
     , instrument
     , action
     , cost
     , currency
     , volume
     , cost_per_share
     , stock_exchange_name
     , SUM(t.volume) OVER(partition BY t.instrument, t.stock_exchange_name, trader ORDER BY t.date rows UNBOUNDED PRECEDING ) total_shares
  FROM {{ref('tfm_book')}}  t
UNION ALL   
SELECT book
     , date
     , trader
     , instrument
     , 'HOLD' as action
     , 0 AS cost
     , currency
     , 0      as volume
     , 0      as cost_per_share
     , stock_exchange_name
     , total_shares
FROM {{ref('tfm_daily_position')}} 
WHERE (date,trader,instrument,book,stock_exchange_name) 
      NOT IN 
      (SELECT date,trader,instrument,book,stock_exchange_name
         FROM {{ref('tfm_book')}}
      )