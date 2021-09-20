# dbt + Gitlab + Snowflake

## Details
https://gitlab.com/yuyatinnefeld/snowflake-dbt-cicd


## Local Setup
1. create a dbt project
```bash
dbt init <project-name>
```
2. setup profiles.yml
3. adjust the dbt_project.yml
4. dbt debug
5. pip freeze > requirements.txt
6. git push

## Gitlab Setup

1. create 4 gitlab variables
- SF_ACCOUNT
- SF_PASSWORD
- SF_ROLE
- SF_USER
2. create a directory "profile"
3. create a profile/profiles.yml

```yml
dbt_sf_monitoring:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: "{{ env_var('SF_ACCOUNT') }}"
      user: "{{ env_var('SF_USER') }}"
      password: "{{ env_var('SF_PASSWORD') }}"
      role: "{{ env_var('SF_ROLE') }}"
      database: dbt_sf_dev
      warehouse: dbt_dev_wh
      schema: public
      threads: 200

    prod:
      type: snowflake
      account: "{{ env_var('SF_ACCOUNT') }}"
      user: "{{ env_var('SF_USER') }}"
      password: "{{ env_var('SF_PASSWORD') }}"
      role: "{{ env_var('SF_ROLE') }}"
      database: dbt_sf_prod
      warehouse: dbt_prod_wh
      schema: public
      threads: 200
```
4. create GitLab CIfile

```yml
image: registry.gitlab.com/gitlab-data/data-image/dbt-image:v0.0.15

before_script:
  - export SF_PASSWORD=$SF_PASSWORD
  - export SF_USER=$SF_USER
  - export CI_PROFILE_TARGET="--profiles-dir profile --target dev"
  - echo $CI_PROFILE_TARGET

after_script:
  - echo "❄️OK❄️"

build1 ⚙️:
  stage: build
  script:
    - echo "❄️install all packages❄️"
    - pip install -r requirements.txt

test1 🦖:
  stage: test
  script:
    - echo "❄️connection test❄️"
    - dbt debug $CI_PROFILE_TARGET

test2 🐭:
  stage: test
  script:
    - echo "❄️config test❄️"
    - dbt test $CI_PROFILE_TARGET

deploy1 🚀:
  stage: deploy
  script:
    - echo "❄️ deploy ❄️"
    - dbt run $CI_PROFILE_TARGET
  when: manual
```

5. test the CI/CD