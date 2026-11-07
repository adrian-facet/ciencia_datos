-- 2. Rotación de inventario y productos por debajo del punto de reposición.
select
    producto_id, nombre_producto, stock_actual, punto_reposicion,
    dias_stock, rotacion, bajo_punto_reposicion
from {{ ref('mart_rotacion_inventario') }}
order by bajo_punto_reposicion desc, dias_stock
