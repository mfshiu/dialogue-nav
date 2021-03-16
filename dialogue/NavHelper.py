import googlemaps
import dialogue.Information as info

gmaps = googlemaps.Client(key='AIzaSyCINyXxM17YsQbc-AozygwX9japfzZi0DQ')
MAX_DISTANCE = 99999


def get_user_location():
    # loc = gmaps.geolocate()
    # return 25.0230239, 121.2210628
    # return loc['location']['lat'], loc['location']['lng']
    loc = info.get_location()
    if loc is None:
        geo = gmaps.geolocate()
        loc = geo['location']['lat'], geo['location']['lng']
    return loc[0], loc[1]


def get_nearest_place(place):
    nearest = None, None, MAX_DISTANCE
    loc0 = get_user_location()

    places = gmaps.places(location=loc0, query=place, radius='300', language='zh-TW')

    test = 0
    for p in places['results']:
        if test > 2:
            break
        loc1 = p['geometry']['location']['lat'], p['geometry']['location']['lng']
        dist = get_walking_distance(loc0, loc1)
        if dist < nearest[2]:
            nearest = p['name'], \
                      (p['geometry']['location']['lat'],
                       p['geometry']['location']['lng']), \
                      dist
        test += 1

    return nearest


def get_walking_distance(coords_0, coords_1=None):
    if not coords_1:
        coords_1 = get_user_location()
    distance = MAX_DISTANCE
    try:
        result = gmaps.directions(coords_0, coords_1, mode="walking")
        if len(result) and len(result[0]['legs']):
            distance = result[0]['legs'][0]['distance']['value']
    except:
        distance = MAX_DISTANCE

    return distance


def parse_destination_type(dest_name):
    if '捷運' in dest_name:
        return 'mrt'
    elif '全家' in dest_name:
        return 'family'
    elif '7-ELEVEN' in dest_name:
        return 'seven'
    elif 'OK' in dest_name:
        return 'okmart'
    elif '萊爾富' in dest_name:
        return 'hilife'
    else:
        return None
