# Jenkins + Snowflake CI/CD
- This guide shows you the automated release management for Snowflake by leveraging the open-source Jenkins
- In order to manage the database objects/changes in Snowflake the schemachange is used for a Database Change Management (DCM) tool.

schemachange: https://github.com/Snowflake-Labs/schemachange

## Setup

### Setup a new github repo

0. create a github repo

1. create a repo and an initial object
```bash
# create a local repo
mkdir jenkins-snowflake
mkdir jenkins-snowflake/migrations
vi jenkins-snowflake/migrations/V1.1.1__initial_objects.sql
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
git remote add origin https://github.com/<USER_NAME>/jenkins-snowflake.git
git push origin master
```

## Deploying Jenkins
1. create a Dockerfile

2. build the image
```bash
# create a image
docker build -t jenkins .

# create and run container
docker run -p 8080:8080 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name jenkins \
  jenkins

# copy the jenkins password
Jenkins initial setup is required. An admin user has been created and a password generated.
Please use the following password to proceed to installation:

xxxxxxxxxxxxxxx


# give jenkins access to docker engine
docker exec -it -u root jenkins bash -c 'chmod 666 /var/run/docker.sock'
```

3. configure the jenkins
- open localhost:8080
- click on the Install suggested plugins
- define name, password, etc.
- Sign in
- click "Manage Plugins" under Manage Jenkins
- click "Available" tab and enter "docker pipeline"
- check the box under docker pipeline
- click on the Install
- restart

## Create a jenkins pipeline (Github)
1. create a Jenkinsfile

```bash
vi Jenkinsfile
```

```bash
pipeline {
    agent { 
        docker { 
            image "python:3.8"
            args '--user 0:0'
        } 

    }
    stages {
        stage('Run schemachange') {
            steps {
                sh "pip install schemachange --upgrade"
                sh "schemachange -f migrations -a ${SF_ACCOUNT} -u ${SF_USERNAME} -r ${SF_ROLE} -w ${SF_WAREHOUSE} -d ${SF_DATABASE} -c ${SF_DATABASE}.SCHEMACHANGE.CHANGE_HISTORY --create-change-history-table"
            }
        }
    }
}
```
2. commit and push the change
```bash
git add .
git commit -m "add Jenkinsfile"
git push origin master
```

3. copy the URL of github repo
ex. https://github.com/<USER_NAME>/jenkins-snowflake.git

## Create the jenkins pipeline (Jenkins)

- click new item
- name = snowflake-devops-demo
- click Pipeline
- Definition = Pipeline script from SCM
- SCM > Git
- define the Repo URL
- click on the advanced btn enter these values for the below parameters:

    Name: origin
    Refspec: +refs/pull/*:refs/remotes/origin/pr/*
    Branches to build: leave blank
    Repository browser: (Auto)
    Additional Behaviours: Add > Wipe out repository & force clone
    Script Path: Jenkinsfile
    Uncheck "Lightweight checkout"

- save the setup

## Add pipeline parameters
1. open up your snowflake-devops-demo job
2. click on Configure > click the checkbox "this project is parameterised" option
3. click on the "Add Parameter"

- SF_ACCOUNT = hh66057.europe-west4.gcp (String Parameter)
- SF_USERNAME = YUYA (String Parameter)
- SF_ROLE = SYSADMIN (String Parameter)
- SF_WAREHOUSE = COMPUTE_WH (String Parameter)
- SF_DATABASE = DEMO_DB (String Parameter)
- SNOWFLAKE_PASSWORD = xxxxxxx (Password Parameter)
- ROOT_FOLDER = migrations (String Parameter)
4. save the configuration

## Manually Run the Pipeline

1. click on the "Build with Paramters" > Build
2. Stage view will be displayed
Now that your first database migration has been deployed to Snowflake, log into your Snowflake account and confirm
3. confirm the DEMO_DB in the Snowflake
- A new schema DEMO and table HELLO_WORLD
- A new schema SCHEMACHANGE and table CHAGE_HISTORY (created by schemachange to track deployed changes)

## Create Your Second Database Migration

1. open up your cloned repo
2. create a script named V1.1.2__updated_objects.sql
```sql
USE SCHEMA DEMO;
ALTER TABLE HELLO_WORLD ADD COLUMN AGE NUMBER;
```
3. commit and push the change
```bash
git add .
git commit -m "add v2 db migration"
git push origin master
```
4. confirm the changing in the JENKINS + Snowflake