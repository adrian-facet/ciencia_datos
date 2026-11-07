-- Una fila por día del período, incluidos los días sin ventas (con ceros),
-- para que promedio, mediana y desviación estándar no queden sesgados.
with rango as (
    select min(fecha) as desde, max(fecha) as hasta from {{ ref('int_ventas_enriquecidas') }}
),
calendario as (
    select cast(d as date) as fecha
    from rango, generate_series(rango.desde, rango.hasta, interval 1 day) as t(d)
),
diario as (
    select
        fecha,
        count(*)            as transacciones,
        sum(cantidad)       as unidades,
        sum(importe_bruto)  as facturacion_bruta,
        sum(descuento_total) as descuentos,
        sum(importe_neto)   as facturacion_neta,
        sum(costo_venta)    as costo_ventas,
        sum(ganancia_bruta) as ganancia_bruta
    from {{ ref('int_ventas_enriquecidas') }}
    group by fecha
)
select
    c.fecha,
    dayname(c.fecha)                      as dia_semana,
    coalesce(d.transacciones, 0)          as transacciones,
    coalesce(d.unidades, 0)               as unidades,
    coalesce(d.facturacion_bruta, 0)      as facturacion_bruta,
    coalesce(d.descuentos, 0)             as descuentos,
    coalesce(d.facturacion_neta, 0)       as facturacion_neta,
    coalesce(d.costo_ventas, 0)           as costo_ventas,
    coalesce(d.ganancia_bruta, 0)         as ganancia_bruta
from calendario as c
left join diario as d using (fecha)
order by c.fecha
