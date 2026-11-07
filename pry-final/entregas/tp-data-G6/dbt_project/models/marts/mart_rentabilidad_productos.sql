-- Ganancia bruta por producto = facturación neta - costo (costo promedio
-- ponderado de compras x unidades vendidas).
select
    p.producto_id,
    p.nombre_producto,
    p.categoria,
    coalesce(sum(v.cantidad), 0)       as unidades_vendidas,
    coalesce(sum(v.importe_neto), 0)   as facturacion_neta,
    coalesce(sum(v.costo_venta), 0)    as costo_ventas,
    coalesce(sum(v.ganancia_bruta), 0) as ganancia_bruta,
    round(100.0 * sum(v.ganancia_bruta) / nullif(sum(v.importe_neto), 0), 2) as margen_bruto_pct
from {{ ref('stg_productos') }} as p
left join {{ ref('int_ventas_enriquecidas') }} as v using (producto_id)
group by 1, 2, 3
order by ganancia_bruta desc
