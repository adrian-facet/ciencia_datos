-- Indicadores descriptivos del período (una sola fila).
select
    count(*)                                   as dias_periodo,
    sum(facturacion_neta)                      as facturacion_total,
    sum(unidades)                              as unidades_vendidas,
    sum(ganancia_bruta)                        as ganancia_bruta_total,
    round(avg(facturacion_neta), 2)            as promedio_venta_diaria,
    round(median(facturacion_neta), 2)         as mediana_venta_diaria,
    round(stddev_samp(facturacion_neta), 2)    as desvio_venta_diaria,
    round(min(facturacion_neta), 2)            as minimo_venta_diaria,
    round(max(facturacion_neta), 2)            as maximo_venta_diaria
from {{ ref('mart_ventas_diarias') }}
