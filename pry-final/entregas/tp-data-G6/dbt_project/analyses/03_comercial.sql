-- 3a. Top de vendedores.
select ranking, nombre_vendedor, sucursal, facturacion_neta, participacion_pct
from {{ ref('mart_desempeno_vendedores') }}
order by ranking;

-- 3b. Distribución ABC de las ventas.
select
    clase_abc,
    count(*)                         as productos,
    round(sum(facturacion_neta), 2)  as facturacion,
    round(sum(participacion_pct), 2) as participacion_pct
from {{ ref('mart_clasificacion_abc') }}
group by clase_abc
order by clase_abc;
