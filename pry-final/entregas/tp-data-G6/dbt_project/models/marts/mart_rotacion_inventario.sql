-- Stock actual, rotación y días de stock disponibles por producto.
-- Punto de reposición = demanda diaria promedio x var('dias_reposicion').
with periodo as (
    select datediff('day', min(fecha), max(fecha)) + 1 as dias from {{ ref('stg_ventas') }}
),
ventas as (
    select producto_id, sum(cantidad) as unidades_vendidas
    from {{ ref('stg_ventas') }}
    group by producto_id
),
stock as (
    select
        producto_id,
        arg_max(stock_despues, (fecha, movimiento_id)) as stock_actual,
        avg(stock_despues)                             as stock_promedio
    from {{ ref('int_movimientos_stock') }}
    group by producto_id
),
base as (
    select
        p.producto_id,
        p.nombre_producto,
        p.categoria,
        p.stock_inicial,
        coalesce(s.stock_actual, p.stock_inicial)   as stock_actual,
        coalesce(s.stock_promedio, p.stock_inicial) as stock_promedio,
        coalesce(v.unidades_vendidas, 0)            as unidades_vendidas,
        coalesce(v.unidades_vendidas, 0) / periodo.dias as demanda_diaria
    from {{ ref('stg_productos') }} as p
    cross join periodo
    left join stock as s using (producto_id)
    left join ventas as v using (producto_id)
)
select
    *,
    round(unidades_vendidas / nullif(stock_promedio, 0), 2) as rotacion,
    round(stock_actual / nullif(demanda_diaria, 0), 1)      as dias_stock,
    round(demanda_diaria * {{ var('dias_reposicion') }}, 1) as punto_reposicion,
    stock_actual < demanda_diaria * {{ var('dias_reposicion') }} as bajo_punto_reposicion
from base
order by dias_stock
