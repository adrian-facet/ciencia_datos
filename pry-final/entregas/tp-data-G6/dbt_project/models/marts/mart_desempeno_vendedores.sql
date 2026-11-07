-- Ventas acumuladas por vendedor y su ranking por facturación neta.
select
    vd.vendedor_id,
    vd.nombre_vendedor,
    vd.sucursal,
    count(v.venta_id)                  as transacciones,
    coalesce(sum(v.cantidad), 0)       as unidades,
    coalesce(sum(v.importe_neto), 0)   as facturacion_neta,
    coalesce(sum(v.ganancia_bruta), 0) as ganancia_bruta,
    round(sum(v.importe_neto) / nullif(count(v.venta_id), 0), 2) as ticket_promedio,
    round(100.0 * sum(v.importe_neto) / sum(sum(v.importe_neto)) over (), 2) as participacion_pct,
    rank() over (order by sum(v.importe_neto) desc nulls last) as ranking
from {{ ref('stg_vendedores') }} as vd
left join {{ ref('int_ventas_enriquecidas') }} as v using (vendedor_id)
group by 1, 2, 3
order by ranking
