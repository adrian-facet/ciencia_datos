-- En generar_datos.py el descuento es un monto por unidad (5 % o 10 % del
-- precio), no una proporción: importe_neto = cantidad x (precio - descuento).
with base as (
    select
        cast(id as integer)                     as venta_id,
        cast(fecha as date)                     as fecha,
        cast(producto_id as integer)            as producto_id,
        cast(vendedor_id as integer)            as vendedor_id,
        cast(cantidad as integer)               as cantidad,
        cast(precio_unitario as decimal(14, 2)) as precio_unitario,
        coalesce(cast(nullif(trim(descuento), '') as decimal(14, 2)), 0) as descuento_unitario
    from {{ source('minimercado', 'ventas') }}
)
select
    *,
    cantidad * precio_unitario                        as importe_bruto,
    cantidad * descuento_unitario                     as descuento_total,
    cantidad * (precio_unitario - descuento_unitario) as importe_neto
from base
