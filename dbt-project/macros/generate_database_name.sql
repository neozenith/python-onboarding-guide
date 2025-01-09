{% macro generate_database_name(custom_database_name=none, node=none) -%}

    {%- set default_database = target.database -%}

    {#- https://docs.getdbt.com/guides/customize-schema-alias?step=5#always-enforce-custom-schemas -#}
    {%- if custom_database_name is none and node.resource_type == 'model' -%}
        
        {{ exceptions.raise_compiler_error("Error: No Custom Database Defined for the model " ~ node.name ) }}
    
    {%- endif -%}

    {%- if custom_database_name is none -%}

        {{ default_database }}

    {%- else -%}

        {{ data_environment(node=node) | trim | upper }}__{{ custom_database_name | trim | upper }}

    {%- endif -%}

{%- endmacro %}
