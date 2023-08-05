
-- cette requête rend deux IRIS : Ambroise et Père-Lachaise alors que l'intersection semble être plus Ambroise.
select iris
  , nom_com
  , nom_iris
  , typ_iris
  , dcomiris
  , st_asGeoJSON(geom)
from geoiris
-- where geom && st_setSRID(st_makepoint(2.3837, 48.8661), 4326);
where st_within(st_setSRID(st_makepoint(2.3837, 48.8661), 4326), geom);

-- NOTE: overlap && fait une bounding box 2D sur polygon avant de voir si le point il est dedans.

-- dcomiris:
-- ambroise: 751114201
-- lachaise: 751207907

-- lachaise
select nom_iris
  , dcomiris
  , st_distance(geom, st_setSRID(st_makepoint(2.3837, 48.8661), 4326)) as dist
from geoiris
where dcomiris='751207907';

-- saint-ambroise
select nom_iris
  , dcomiris
  , st_distance(geom, st_setSRID(st_makepoint(2.3837, 48.8661), 4326)) as dist
from geoiris
where dcomiris='751114201';
