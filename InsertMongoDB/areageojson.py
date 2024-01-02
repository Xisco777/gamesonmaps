
# core modules
from functools import partial

# 3rd pary modules
import pyproj
from shapely.geometry import Polygon
import shapely.ops as ops

l = [[13.65374516425911, 52.38533382814119, 0],
     [13.65239769133293, 52.38675829106993, 0],
     [13.64970274383571, 52.38675829106993, 0],
     [13.64835527090953, 52.38533382814119, 0],
     [13.64970274383571, 52.38390931824483, 0],
     [13.65239769133293, 52.38390931824483, 0],
     [13.65374516425911, 52.38533382814119, 0]]
polygon = Polygon(l)

print(polygon.area)
geom_area = ops.transform(
    partial(
        pyproj.transform,
        pyproj.Proj(init='EPSG:4326'),
        pyproj.Proj(
            proj='aea',
            lat1=polygon.bounds[1],
            lat2=polygon.bounds[3])),
    polygon)
print(geom_area.area)