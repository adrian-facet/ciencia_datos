-- Las entradas y salidas de movimientos_stock deben coincidir con compras y ventas.
with mov as (
    select
        sum(case when tipo_movimiento = 'ENTRADA_COMPRA' then cantidad else 0 end) as entradas,
        sum(case when tipo_movimiento = 'SALIDA_VENTA' then cantidad else 0 end)   as salidas
    from {{ ref('stg_movimientos_stock') }}
)
select *
from mov
where entradas <> (select sum(cantidad) from {{ ref('stg_compras') }})
   or salidas  <> (select sum(cantidad) from {{ ref('stg_ventas') }})
