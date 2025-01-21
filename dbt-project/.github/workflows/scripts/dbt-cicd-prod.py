name: dbt Cloud CD - PROD Merge Deploy Job
on:
  workflow_dispatch:
    inputs:
      confirm_deployment:
        description: 'Confirm Production Deployment'
        required: true
        type: boolean
  push:
    paths:
      - dbt-project/**
    branches:
      - main
  
permissions:
  contents: read

jobs:
  ghcontext:
    runs-on: ubuntu-latest
    steps:
      - name: Dump GitHub context
        env:
          GITHUB_CONTEXT: ${{ toJSON(github) }}
        run: echo "$GITHUB_CONTEXT"

  trigger-prod-dbt-cloud-job:
    if: |
      github.ref == 'refs/heads/main' && (
        (github.event_name == 'push')  || 
        (github.event_name == 'workflow_dispatch' && github.event.inputs.confirm_deployment == 'true')
      )

    name: trigger-prod-dbt-cloud-job
    runs-on: ubuntu-latest
    
    env:
      DBT_CLOUD_HOST: ${{ vars.DBT_CLOUD_HOST }}
      DBT_ACCOUNT_ID: ${{ vars.DBT_CLOUD_ACCOUNT_ID }}
      DBT_PROJECT_ID: ${{ vars.DBT_CLOUD_PROJECT_ID }}
      DBT_CLOUD_JOB_ID: ${{ vars.DBT_CLOUD_PROD_JOB_ID }}
      DBT_CLOUD_SERVICE_TOKEN: ${{ secrets.DBT_CLOUD_PROD_SERVICE_TOKEN }}

    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4  
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Trigger dbt cloud PROD Job
        run: uv run .github/workflows/scripts/dbt_cicd.py


  
