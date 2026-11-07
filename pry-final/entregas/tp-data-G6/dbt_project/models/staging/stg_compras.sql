select
    cast(id as integer)                    as compra_id,
    cast(fecha as date)                    as fecha,
    cast(producto_id as integer)           as producto_id,
    cast(cantidad as integer)              as cantidad,
    cast(costo_unitario as decimal(14, 2)) as costo_unitario,
    cast(cantidad as integer) * cast(costo_unitario as decimal(14, 2)) as importe_compra,
    trim(proveedor)                        as proveedor
from {{ source('minimercado', 'compras') }}
