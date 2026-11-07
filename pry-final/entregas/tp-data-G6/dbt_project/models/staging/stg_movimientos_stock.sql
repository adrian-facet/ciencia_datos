-- STOCK_INICIAL y ENTRADA_COMPRA suman stock; SALIDA_VENTA lo resta.
select
    cast(id as integer)            as movimiento_id,
    cast(fecha as date)            as fecha,
    cast(producto_id as integer)   as producto_id,
    upper(trim(tipo_movimiento))   as tipo_movimiento,
    case
        when upper(trim(tipo_movimiento)) = 'SALIDA_VENTA' then 'salida'
        else 'entrada'
    end                            as sentido,
    cast(cantidad as integer)      as cantidad,
    cast(referencia_id as integer) as referencia_id
from {{ source('minimercado', 'movimientos_stock') }}
