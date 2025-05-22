from kml_exporter import *
from navPoint import NavPoint

p1 = NavPoint(1, "P1", 41.38, 2.17)
p2 = NavPoint(2, "P2", 41.40, 2.20)
export_points_to_kml([p1, p2], "points.kml")
export_path_to_kml([p1, p2], "path.kml")
