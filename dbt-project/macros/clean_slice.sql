{% macro clean_slice(debug_logging=false) -%}

  {#- we replace characters not allowed in the schema names by "_" -#}
  {%- set re = modules.re -%}
        
  {#- https://docs.getdbt.com/docs/build/environment-variables#special-environment-variables -#} 
  {%- set pr_id = re.sub("\W", "_", env_var('DBT_CLOUD_PR_ID', '')) | trim | upper -%}
  {%- set job_id = re.sub("\W", "_", env_var('DBT_CLOUD_JOB_ID', '')) | trim | upper -%}
  {%- set run_id = re.sub("\W", "_", env_var('DBT_CLOUD_RUN_ID', '')) | trim | upper -%}

  {#- DEV environment uses branch -#}
  {%- set branch_slice = re.sub("\W", "_", 
      env_var('DBT_CLOUD_GIT_BRANCH', 
        env_var('DBT_GIT_BRANCH', 
          env_var('GIT_BRANCH', 
            var('git_branch')
          )
        )
      )
    )
   -%}
        
  {#- TEST Environment uses CI values -#}
  {%- set ci_slice = "PR" ~ pr_id ~ "_JOB" ~ job_id ~ "_RUN" ~ run_id -%}

  {%- set cleaned_slice = "" -%}        

  {% if branch_slice is not none and branch_slice | length > 0 %}
    {%- set cleaned_slice = branch_slice -%}
  {% elif ci_slice is not none and ci_slice | length > 10 %}
    {%- set cleaned_slice = ci_slice -%}        
  {% endif %}

  {% do log("Clean slice: " ~ cleaned_slice, info=debug_logging) %}
  {{- cleaned_slice | trim -}}       

{% endmacro %}
