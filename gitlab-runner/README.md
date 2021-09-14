# Gitlab CICD + Snowflake

customized github-actions + schemachange for gitlab runner
Details: https://github.com/yuyatinnefeld/snowflake/tree/master/github-actions

## Setup

1. create a gitlab project

2. create a migrations folder and sql file

3. create .gitlab-ci.yml

4. setup the variables by pipeline run
- SF_ACCOUNT
- SF_USERNAME
- SF_ROLE
- SF_WAREHOUSE
- SF_DATABASE
- SF_PASSWORD

5. run the cicd pipeline 
