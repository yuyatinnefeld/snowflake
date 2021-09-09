# Snowflake + Terraform + Github Actions
- Snowflake as DWH
- Terraform as Database Change Management
- Github Actions as CI/CD
This guide shows how to build a simple CI/CD pipeline for Snowflake with GitHub Actions and Terraform

## Setup a new Terraform workspace
1. Login / Register
https://app.terraform.io/app

2. click "New workspace"

3. select "API driven workflow"

4. define the name "YT-Snowflake"

5. Setup Environment Variables

Variable key
- SNOWFLAKE_ACCOUNT     (ex. hh66057)           Sensitive NO
- SNOWFLAKE_REGION      (ex. europe-west4.gcp)  Sensitive NO
- SNOWFLAKE_USER        (ex. yuya)              Sensitive NO
- SNOWFLAKE_PASSWORD    (ex. xxxxx)             Sensitive YES

6. Create an API Token

- Click on the user icon > click on "User settings"
- Click on the user settings page click on the "Tokens"
- Click "Create API token"
- Description: GitHub Actions
- You need to save the API token


 tL3P1fVu1OrkuQ.atlasv1.IyshlhDQgcFyrL8DMoCCDYx8g6CdtzFNTZoARe2ptzPYvUHiidOwUqtq3h6zqzoyqsg

## Create the Actions Workflow

### Create a Actions Secrets
1. Create Github Repo
 
2. Create Actions Secrets
- Click Settings > Secrets > Click on the "New repository secret"
- Name = TF_API_TOKEN 
- Value = Terraform Token

## Define the Action Workflows
In this step we will create a deployment workflow which will run Terraform and deploy changes to our Snowflake account

- Select the Github Repo > click on the "Actions" > click on the "Set up this workflow"

- Name the workflow = snowflake-terraform-demo.yml
- In the "Edit new file" box, replace the contents with the the following:
- check if the main branch name "main"

Please note that if you are re-using an existing GitHub repository it might retain the old master branch naming. If so, please update the YAML bottom

```yml
name: "Snowflake Terraform Demo Workflow"

on:
  push:
    branches:
      - main

jobs:
  snowflake-terraform-demo:
    name: "Snowflake Terraform Demo Job"
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v1
        with:
          cli_config_credentials_token: ${{ secrets.TF_API_TOKEN }}

      - name: Terraform Format
        id: fmt
        run: terraform fmt -check

      - name: Terraform Init
        id: init
        run: terraform init

      - name: Terraform Validate
        id: validate
        run: terraform validate -no-color

      - name: Terraform Apply
        id: apply
        run: terraform apply -auto-approve
```

- Click on the "Start commit"

## Create Your First Database Migration
1. git clone your github repo
```bash
git clone git@github.com:<YOURNAME>/snowflake-terraform.git
```


2. add a main.tf 
```bash
vi main.tf
```

replace the organization name with your Terraform Cloud organization name
```bash
terraform {
  required_providers {
    snowflake = {
      source  = "chanzuckerberg/snowflake"
      version = "0.25.17"
    }
  }

  backend "remote" {
    organization = "yuyatinnefeld"

    workspaces {
      name = "YT-Snowflake"
    }
  }
}

provider "snowflake" {
}

resource "snowflake_database" "tf_db" {
  name    = "TERRAFORM_DB"
  comment = "Database for Snowflake Terraform demo"
}

3. test local
```bash
terraform init
terraform plan
```

4. commit and push the change
```bash
git add .
git commit -m "add main.tf"
git push origin main
```
the first database migration should have been successfully deployed

## Confirm changes deployed to snowflake

1. check Snowflake Objects
2. check Terraform Cloud Log
3. check GitHub Actions Log


## Update main.tf to create the second database migration

1. add this lines to end of the file
```bash
resource "snowflake_schema" "tf_schema" {
  database = snowflake_database.tf_db.name
  name     = "TERRAFORM_SCHEMA"
  comment  = "Schema for Snowflake Terraform demo"
}
```
2. commit and push the change
```bash
git add .
git commit -m "updates main.tf"
git push origin main
```

## Setup Advanced github Actions

1. update the github actions file
```yml
name: "Snowflake Terraform Demo Workflow"

on:
  push:
    branches:
      - main

jobs:
  snowflake-terraform-demo:
    name: "Snowflake Terraform Demo Job"
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v1
        with:
          cli_config_credentials_token: ${{ secrets.TF_API_TOKEN }}

      - name: Terraform Format
        id: fmt
        run: terraform fmt -check

      - name: Terraform Init
        id: init
        run: terraform init

      - name: Terraform Validate
        id: validate
        run: terraform validate -no-color


      - name: Terraform Plan
        id: plan
        if: github.event_name == 'pull_request'
        run: terraform plan -no-color
        continue-on-error: true

      - uses: actions/github-script@0.9.0
        if: github.event_name == 'pull_request'
        env:
          PLAN: "terraform\n${{ steps.plan.outputs.stdout }}"
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const output = `#### Terraform Format and Style 🖌\`${{ steps.fmt.outcome }}\`
            #### Terraform Initialization ⚙️\`${{ steps.init.outcome }}\`
            #### Terraform Validation 🤖\`${{ steps.validate.outcome }}\`
            #### Terraform Plan 📖\`${{ steps.plan.outcome }}\`
            
            <details><summary>Show Plan</summary>
            
            \`\`\`\n
            ${process.env.PLAN}
            \`\`\`
            
            </details>
            
            *Pusher: @${{ github.actor }}, Action: \`${{ github.event_name }}\`, Working Directory: \`${{ env.tf_actions_working_dir }}\`, Workflow: \`${{ github.workflow }}\`*`;
            
            github.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: output
            })

      - name: Terraform Plan Status
        if: steps.plan.outcome == 'failure'
        run: exit 1

      - name: Terraform Apply
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        run: terraform apply -auto-approve
```

2. commit and push the change
```bash
git add .
git commit -m "updates main.tf"
git push origin main
```

3. update the main.tf

resource "snowflake_database" "tf_db2" {
  name    = "TERRAFORM_DB2"
  comment = "Database for Snowflake Terraform demo"
}

4. commit and push the change
```bash
git add .
git commit -m "updates main.tf"
git push origin main
```