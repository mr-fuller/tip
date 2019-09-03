select gid,
project_na, 
--assuming web mercator(SRID:3857) which has units of meters
--can I use a case statement here to get the srid unit?
st_buffer(geom,
        case 
		  when st_srid(geom) = '3857' then 1609.344
		  when st_srid(geom) = '3734' then 5280
		  else 0
		end)
--select st_srid(geom) 
from apps2019
where funding_ty = 'TA';

--get the area of each block/tract that intersects each buffer,
--then sum the population*area_ratio