import geopandas as gpd
import geoplot as gplt

cities = gpd.read_file(glpt.datasets.get_path('usa_cities'))
gplt.pointplot(cities)
