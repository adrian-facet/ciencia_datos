-- Clasificación ABC (Pareto) por facturación neta:
-- A = productos que acumulan hasta el 80 %, B = hasta el 95 %, C = el resto.
with ventas as (
    select producto_id, nombre_producto, categoria, unidades_vendidas, facturacion_neta
    from {{ ref('mart_rentabilidad_productos') }}
),
acumulado as (
    select
        *,
        100.0 * facturacion_neta / sum(facturacion_neta) over () as participacion_pct,
        100.0 * sum(facturacion_neta) over (
            order by facturacion_neta desc, producto_id
            rows between unbounded preceding and current row
        ) / sum(facturacion_neta) over () as acumulado_pct
    from ventas
)
select
    producto_id,
    nombre_producto,
    categoria,
    unidades_vendidas,
    facturacion_neta,
    round(participacion_pct, 2) as participacion_pct,
    round(acumulado_pct, 2)     as acumulado_pct,
    case
        when acumulado_pct - participacion_pct < 80 then 'A'
        when acumulado_pct - participacion_pct < 95 then 'B'
        else 'C'
    end as clase_abc
from acumulado
order by facturacion_neta desc
