select
    cast(id as integer)      as vendedor_id,
    trim(nombre)             as nombre_vendedor,
    trim(sucursal)           as sucursal,
    cast(fecha_alta as date) as fecha_alta
from {{ source('minimercado', 'vendedores') }}
