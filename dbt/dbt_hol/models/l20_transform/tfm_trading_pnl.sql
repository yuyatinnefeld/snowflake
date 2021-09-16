SELECT t.instrument, t.stock_exchange_name, 
       t.date, trader, t.volume,cost, cost_per_share,currency,
       SUM(cost) OVER(partition BY t.instrument, t.stock_exchange_name, trader ORDER BY t.date rows UNBOUNDED PRECEDING ) cash_cumulative,
       CASE WHEN t.currency = 'GBP' THEN gbp_close
            WHEN t.currency = 'EUR' THEN eur_close
            ELSE close
       END                                                        AS close_price_matching_ccy,     
       total_shares  * close_price_matching_ccy                   AS market_value, 
       total_shares  * close_price_matching_ccy + cash_cumulative AS PnL
   FROM       {{ref('tfm_daily_position_with_trades')}}    t
   INNER JOIN {{ref('tfm_stock_history_major_currency')}}  s 
      ON t.instrument = s.company_symbol 
     AND s.date = t.date 
     AND t.stock_exchange_name = s.stock_exchange_name