-- Movimientos de almacén con signo (+ entrada, - salida) y stock corrido por
-- producto. El stock inicial ya llega como movimiento STOCK_INICIAL.
with movimientos as (
    select
        movimiento_id,
        fecha,
        producto_id,
        tipo_movimiento,
        sentido,
        cantidad,
        referencia_id,
        case when sentido = 'entrada' then cantidad else -cantidad end as cantidad_neta
    from {{ ref('stg_movimientos_stock') }}
)
select
    *,
    sum(cantidad_neta) over (
        partition by producto_id
        order by fecha, movimiento_id
        rows between unbounded preceding and current row
    ) as stock_despues
from movimientos
