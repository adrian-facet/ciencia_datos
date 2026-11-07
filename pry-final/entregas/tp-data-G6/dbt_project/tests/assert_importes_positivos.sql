-- Falla si hay ventas o compras con cantidades o precios no positivos,
-- o descuentos que superen el precio.
select 'venta' as origen, venta_id as id from {{ ref('stg_ventas') }}
where cantidad <= 0 or precio_unitario <= 0
   or descuento_unitario < 0 or descuento_unitario >= precio_unitario
union all
select 'compra', compra_id from {{ ref('stg_compras') }}
where cantidad <= 0 or costo_unitario <= 0
