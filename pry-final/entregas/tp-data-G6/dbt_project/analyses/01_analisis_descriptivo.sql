-- 1. Facturación total, unidades vendidas, promedio, mediana y desviación
--    estándar de las ventas diarias.
select * from {{ ref('mart_estadisticas_ventas') }}
