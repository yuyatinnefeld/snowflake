SELECT "Currency"        currency
     , "Currency Unit"   currency_unit
     , "Frequency"       frequency
     , "Date"            date
     , "Value"           value
     , 'Knoema.FX Rates' data_source_name
     , src.*
  FROM {{source('knoema_economy_data_atlas','exratescc2018')}}  src 