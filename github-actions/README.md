# Github Actions + Snowflake

## Setup Snowfake

```sql
USE ROLE ACCOUNTADMIN;
CREATE OR REPLACE DATABASE DEMO_DB
GRANT USAGE ON DATABASE DEMO_DB TO ROLE SYSADMIN;
```

## Setup a new github repo

0. create a github repo

1. create a repo and an initial object
```bash
# create a local repo
mkdir snowflake-cicd
mkdir snowflake-cicd/migrations
vi snowflake-cicd/migrations/V1.1.1__initial_objects.sql
```

V1.1.1__initial_objects.sql
```sql
CREATE SCHEMA DEMO;
CREATE TABLE HELLO_WORLD
(
   FIRST_NAME VARCHAR
  ,LAST_NAME VARCHAR
);
```
2. git commit and push
```bash
git init
git add .
git commit -m "initial setup"
git remote add origin https://github.com/<USER_NAME>/snowflake-cicd.git
git push origin main
```

## Create Action Secrets
1. github repo > settings > secrets > New repository secret

- SF_ACCOUNT = hh66057.europe-west4.gcp
- SF_USERNAME = YUYA
- SF_ROLE = SYSADMIN
- SF_WAREHOUSE = COMPUTE_WH
- SF_DATABASE = DEMO_DB
- SF_PASSWORD = Fxxxxxx


![GitHub Logo](/images/actions-secrets.png)

## Create Action Workflow

1. github repo > click on the "Actions" 
2. click on the "Set up this workflow"

- Name the workflow = snowflake-devops-demo.yml
- In the "Edit new file" box, replace the contents with the the following:
- check if the main branch name "main"
```yml
name: snowflake-devops-demo

# Controls when the action will run. 
on:
  push:
    branches:
      - main
    paths:
      - 'migrations/**'

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

jobs:
  deploy-snowflake-changes-job:
    runs-on: ubuntu-latest

    steps:
      # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Use Python 3.8.x
        uses: actions/setup-python@v2.2.1
        with:
          python-version: 3.8.x

      - name: Run schemachange
        env:
          SF_ACCOUNT: ${{ secrets.SF_ACCOUNT }}
          SF_USERNAME: ${{ secrets.SF_USERNAME }}
          SF_ROLE: ${{ secrets.SF_ROLE }}
          SF_WAREHOUSE: ${{ secrets.SF_WAREHOUSE }}
          SF_DATABASE: ${{ secrets.SF_DATABASE }}
          SNOWFLAKE_PASSWORD: ${{ secrets.SF_PASSWORD }}
        run: |
          echo "GITHUB_WORKSPACE: $GITHUB_WORKSPACE"
          python --version
          echo "Step 1: Installing schemachange"
          pip install schemachange
          
          echo "Step 2: Running schemachange"
          schemachange -f $GITHUB_WORKSPACE/migrations -a $SF_ACCOUNT -u $SF_USERNAME -r $SF_ROLE -w $SF_WAREHOUSE -d $SF_DATABASE -c $SF_DATABASE.SCHEMACHANGE.CHANGE_HISTORY --create-change-history-table
```

Please note that if you are re-using an existing GitHub repository it might retain the old master branch naming. If so, please update the YAML bottom

3. click on Start commit

## Manually Run the Actions Workflow
Actions > snowflake-devops-demo > Run Workflow


## Confirm the changes in Snowflake

## Create the second db change
```bash
vi snowflake-cicd/migrations/V1.1.2__updated_objects.sql
```

```sql
USE SCHEMA DEMO;
ALTER TABLE HELLO_WORLD ADD COLUMN AGE NUMBER;
```

```bash
git add .
git commit -m "updates db migration 2"
git push origin main
