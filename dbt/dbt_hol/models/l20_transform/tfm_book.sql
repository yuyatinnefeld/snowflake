{{ dbt_utils.union_relations(
    relations=[ref('manual_book1'), ref('manual_book2')]
) }}