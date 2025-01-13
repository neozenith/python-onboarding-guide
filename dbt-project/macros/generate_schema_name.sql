{% macro generate_schema_name(custom_schema_name, node) -%}

    {%- set default_schema = target.schema -%}
    {%- set data_env = data_environment() | trim | upper -%}
    {%- set cleaned_slice = clean_slice() | trim | upper -%}

    {#- Enfore a slice gets defined as part of the schema in non-PROD environments. -#}

    {%- if cleaned_slice is not none and cleaned_slice | length > 0 -%}
        {%- set cleaned_slice = cleaned_slice ~ "__" -%}
    {%- else -%}
        {%- if  data_env != 'PROD' -%}
            {{ exceptions.raise_compiler_error("Error: Data Environment is non-PROD and no slice is defined for " ~ node.name ~". Please set environment variable DBT_CLOUD_GIT_BRANCH, or DBT_GIT_BRANCH or project variable git_branch using the --vars \"git_branch: $(git rev-parse --abbrev-ref HEAD)\" commandline option." ) }}    
        {%- endif -%}
    {%- endif -%}


    {#- https://docs.getdbt.com/guides/customize-schema-alias?step=5#always-enforce-custom-schemas -#}
    {%- if custom_schema_name is none and node.resource_type == 'model' -%}
        
        {{ exceptions.raise_compiler_error("Error: No Custom Schema Defined for the model " ~ node.name ) }}
    
    {%- endif -%}


    {%- if  data_env == 'PROD' -%}
    
        {%- if custom_schema_name is not none -%}

            {{ custom_schema_name | trim | upper }}

        {%- else -%}

            {#- Should never get to this code path due to the guard exception above, but sane defaults should prevail. -#}
            {{ default_schema | trim | upper }}

        {%- endif -%}
        
    {%- else -%}

        {{ cleaned_slice | upper }}{{ custom_schema_name | trim | upper }}

    {%- endif -%}

{%- endmacro %}
