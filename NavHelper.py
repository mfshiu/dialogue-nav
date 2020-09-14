import googlemaps

gmaps = googlemaps.Client(key='AIzaSyCINyXxM17YsQbc-AozygwX9japfzZi0DQ')
MAX_DISTANCE = 99999


def get_current_location():
    loc = gmaps.geolocate()
    return 25.0230239, 121.2210628
    # return loc['location']['lat'], loc['location']['lng']


def get_nearest_place(place):
    nearest = None, None, MAX_DISTANCE
    loc0 = get_current_location()

    places = gmaps.places(location=loc0, query=place, radius='300', language='zh-TW')

    test = 0
    for p in places['results']:
        if test > 2:
            break
        loc1 = p['geometry']['location']['lat'], p['geometry']['location']['lng']
        dist = get_walking_dustance(loc0, loc1)
        if dist < nearest[2]:
            nearest = p['name'], \
                      (p['geometry']['location']['lat'],
                       p['geometry']['location']['lng']), \
                      dist
        test += 1

    return nearest


def get_walking_dustance(coords_0, coords_1):
    result = gmaps.directions(coords_0, coords_1, mode="walking")
    if len(result) == 0 or len(result[0]['legs']) == 0:
        return MAX_DISTANCE
    return result[0]['legs'][0]['distance']['value']
