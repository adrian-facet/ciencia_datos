-- Cada venta con su producto, vendedor y costo, lista para los marts.
select
    v.venta_id,
    v.fecha,
    v.producto_id,
    p.nombre_producto,
    p.categoria,
    v.vendedor_id,
    vd.nombre_vendedor,
    vd.sucursal,
    v.cantidad,
    v.precio_unitario,
    v.descuento_unitario,
    v.descuento_total,
    v.importe_bruto,
    v.importe_neto,
    round(v.cantidad * c.costo_unitario_ponderado, 2)                  as costo_venta,
    round(v.importe_neto - v.cantidad * c.costo_unitario_ponderado, 2) as ganancia_bruta
from {{ ref('stg_ventas') }} as v
join {{ ref('stg_productos') }} as p using (producto_id)
join {{ ref('stg_vendedores') }} as vd using (vendedor_id)
join {{ ref('int_costo_promedio_producto') }} as c using (producto_id)
