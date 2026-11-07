-- Usa el nombre de esquema tal cual (staging, intermediate, marts) en lugar de
-- anteponerle el esquema por defecto (main_staging...). Así las consultas finales
-- y Dagster leen siempre marts.<tabla>.
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- if custom_schema_name is none -%}{{ target.schema }}{%- else -%}{{ custom_schema_name | trim }}{%- endif -%}
{%- endmacro %}
