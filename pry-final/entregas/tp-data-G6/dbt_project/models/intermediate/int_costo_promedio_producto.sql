-- Costo unitario promedio ponderado de las compras de cada producto.
-- Si un producto no tuvo compras, se usa el costo del catálogo.
with compras as (
    select
        producto_id,
        sum(importe_compra) / nullif(sum(cantidad), 0) as costo_promedio_compras
    from {{ ref('stg_compras') }}
    group by producto_id
)
select
    p.producto_id,
    coalesce(c.costo_promedio_compras, p.costo_unitario) as costo_unitario_ponderado
from {{ ref('stg_productos') }} as p
left join compras as c using (producto_id)
