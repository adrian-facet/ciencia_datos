-- La facturación total debe ser la misma en ventas diarias, productos y vendedores.
with totales as (
    select
        (select sum(facturacion_neta) from {{ ref('mart_ventas_diarias') }})        as diaria,
        (select sum(facturacion_neta) from {{ ref('mart_rentabilidad_productos') }}) as productos,
        (select sum(facturacion_neta) from {{ ref('mart_desempeno_vendedores') }})   as vendedores
)
select * from totales
where abs(diaria - productos) > 0.01 or abs(diaria - vendedores) > 0.01
