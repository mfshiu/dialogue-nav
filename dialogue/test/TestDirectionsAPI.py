import googlemaps
from dialogue import NavHelper

nearest = NavHelper.get_nearest_place("便利商店")

gmaps = googlemaps.Client(key='AIzaSyCINyXxM17YsQbc-AozygwX9japfzZi0DQ')

# 25.0012688,121.4771506
loc = gmaps.geolocate()
# coords_0 = "我的位置"
coords_0 = str(loc['location']['lat']) + "," + str(loc['location']['lng'])
# coords_0 = '43.70721,-79.3955999'
# coords_1 = '43.7077599,-79.39294'
coords_1 = '全家便利商店 三峽福容店'
# directions_result = gmaps.directions(coords_0, coords_1, mode="driving", departure_time=now, avoid='tolls')
result = gmaps.directions(coords_0, coords_1, mode="walking")

print(result)
