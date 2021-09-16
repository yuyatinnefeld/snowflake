SELECT
  company_symbol, company_name, stock_exchange_name, date, data_source_name,
  {{ dbt_utils.pivot(
      column = 'indicator_name',
      values = dbt_utils.get_column_values(ref('base_knoema_stock_history'), 'indicator_name'),
      then_value = 'value'
  ) }}
FROM {{ ref('base_knoema_stock_history') }}
GROUP BY company_symbol, company_name, stock_exchange_name, date, data_source_name