-- La participación de la clasificación ABC debe sumar 100 %.
select sum(participacion_pct) as total
from {{ ref('mart_clasificacion_abc') }}
having abs(sum(participacion_pct) - 100) > 0.1
