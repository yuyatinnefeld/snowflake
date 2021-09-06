# SnowSQL Function

## Output

### CSV output
```bash
snowsql -c my_test_connection -d sf_tuts -s public -q 'select * from emp_basic limit 10' -o output_format=csv -o header=false -o timing=false -o friendly=false  > data/output_file.csv
```

### List Query Jobs
```sql

# show all queries
YUYA#SF_TUTS_WH@SF_TUTS.PUBLIC>!queries
+--------------------------------------+---------------------------------------------------------------------------------------------------+---------------+-------------+
| QUERY ID                             | SQL TEXT                                                                                          | STATUS        | DURATION_MS |
|--------------------------------------+---------------------------------------------------------------------------------------------------+---------------+-------------|
| 019ec4a2-0000-2499-0000-00005ce1d839 | select email from emp_basic where city = 'Miami';                                                 | SUCCEEDED     |         602 |
| 019ec4a2-0000-2499-0000-00005ce1d835 | select email from emp_basic where city = Miami;                                                   | FAILED_NORMAL |          24 |
| 019ec49c-0000-249a-0000-00005ce1e84d | select email from emp_basic;                                                                      | SUCCEEDED     |         307 |
| 019ec49b-0000-249b-0000-00005ce1f7dd | SELECT * FROM identifier('"SF_TUTS"."PUBLIC"."EMP_BASIC"') LIMIT 100;                             | SUCCEEDED     |         568 |
| 019ec493-0000-249a-0000-00005ce1e839 | select * from emp_basic limit 10                                                                  | SUCCEEDED     |          29 |
| 019ec493-0000-249a-0000-00005ce1e835 | select * from emp_basic limit 10                                                                  | SUCCEEDED     |          60 |
| 019ec490-0000-249a-0000-00005ce1e831 | select * from $mytablename limit 10                                                               | FAILED_NORMAL |          67 |
| 019ec48e-0000-249a-0000-00005ce1e82d | select * from emp_basic limit 10                                                                  | SUCCEEDED     |         753 |
| 019ec48d-0000-2499-0000-00005ce1d825 | select * from mytablename limit 10                                                                | FAILED_NORMAL |          16 |


# show only the queries from this session
YUYA#SF_TUTS_WH@SF_TUTS.PUBLIC>!queries session
+--------------------------------------+---------------------------------------------------+---------------+-------------+
| QUERY ID                             | SQL TEXT                                          | STATUS        | DURATION_MS |
|--------------------------------------+---------------------------------------------------+---------------+-------------|
| 019ec4a2-0000-2499-0000-00005ce1d839 | select email from emp_basic where city = 'Miami'; | SUCCEEDED     |         602 |
| 019ec4a2-0000-2499-0000-00005ce1d835 | select email from emp_basic where city = Miami;   | FAILED_NORMAL |          24 |
| 019ec49c-0000-249a-0000-00005ce1e84d | select email from emp_basic;                      | SUCCEEDED     |         307 |
+--------------------------------------+---------------------------------------------------+---------------+-------------+


# list only the last 20 queries
!queries amount=20

# list the queries from the warehouse
!queries warehouse=COMPUTE_WH;
!queries warehouse=SF_TUTS_WH;

```

## Executes SQL from a file
```bash
vi example.sql

select 1223 as number, 'heloo' as name;
```

```sql
!source example.sql
```