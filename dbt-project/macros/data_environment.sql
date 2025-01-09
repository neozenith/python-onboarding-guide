{% macro data_environment(node=none, debug_logging=false) -%}

    {% set data_env = env_var('DBT_ENV_TYPE','DEV') | upper %}

    {%- if data_env not in ['DEV', 'TEST', 'PROD'] -%}
        {{ exceptions.raise_compiler_error("Error: Invalid DBT_ENV_TYPE value: " ~ data_env) }}
    {%- endif -%}

    {% do log("data_environment: DBT_ENV_TYPE: " ~ data_env, info=debug_logging) %}
    {{ data_env }}

{%- endmacro %}
