-- Ningún producto puede quedar con stock negativo (vender más de lo que había).
select producto_id, fecha, stock_despues
from {{ ref('int_movimientos_stock') }}
where stock_despues < 0
