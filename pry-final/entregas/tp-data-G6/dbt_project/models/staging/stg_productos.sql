select
    cast(id as integer)              as producto_id,
    trim(nombre)                     as nombre_producto,
    trim(categoria)                  as categoria,
    cast(costo_unitario as decimal(14, 2)) as costo_unitario,
    cast(precio_venta as decimal(14, 2))   as precio_venta,
    cast(stock_inicial as integer)   as stock_inicial
from {{ source('minimercado', 'productos') }}
