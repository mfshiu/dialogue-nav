import googlemaps
import json

gmaps = googlemaps.Client(key='AIzaSyCINyXxM17YsQbc-AozygwX9japfzZi0DQ')

loc = gmaps.geolocate()
print(loc)

# places_result = gmaps.places(query='便利商店', radius='500', location=('24.9671999', '121.1876454'), language='zh-TW')
# places_result = gmaps.places(query='便利商店', radius='300', location=(loc['location']['lat'], loc['location']['lng']), language='zh-TW')
places = gmaps.places(query='7-ELEVEN', radius='300', language='zh-TW')
print(places)
first = places['results'][0]

print(first['name'])
print(first['geometry']['location']['lat'])
print(first['geometry']['location']['lng'])
