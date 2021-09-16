WITH cst_market_days AS
(
    SELECT DISTINCT date
    FROM {{ref('tfm_stock_history_major_currency')}} hist
    WHERE hist.date >= ( SELECT min(date) AS min_dt FROM {{ref('tfm_book')}}  )
)
SELECT
    cst_market_days.date,
    trader,
    stock_exchange_name,
    instrument,
    book,
    currency,
    sum(volume) AS total_shares
FROM cst_market_days
   , {{ref('tfm_book')}} book
WHERE book.date <= cst_market_days.date
GROUP BY 1, 2, 3, 4, 5, 6 