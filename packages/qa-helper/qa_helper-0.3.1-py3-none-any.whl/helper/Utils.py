import string
import os
from pathlib import Path
import random
import numpy
import pygeodesy.ellipsoidalVincenty as geo
from Variables.configs import qe
from Variables.main_vars import okd_token
from requests import get


def turn_off_animations(udid):
    commands = ['adb -s {} shell settings put global window_animation_scale 0'.format(udid),
                'adb -s {} shell settings put global transition_animation_scale 0'.format(udid),
                'adb -s {} shell settings put global animator_duration_scale 0'.format(udid)]

    for command in commands:
        os.system(command)


def connect_to_okd(qe_number=qe):
    os.system("oc login https://okd.private.teh-1.snappcloud.io --token={}".format(okd_token))
    os.system("oc project snapp-ode-{}".format(qe_number))


def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent.parent.parent


def generate_random_geo_points_of_tehran(zone="regular_west"):
    zone_start_lat_dic = {'regular_west': 35.718085, 'pollution': 35.722632, 'main': 35.667826, 'regular_east': 35.727956}
    zone_end_lat_dic = {'regular_west': 35.760165, 'pollution': 35.740312, 'main': 35.680865, 'regular_east': 35.746676}
    zone_start_lng_dic = {'regular_west': 51.288815, 'pollution': 51.392298, 'main': 51.397347, 'regular_east': 51.517625}
    zone_end_lng_dic = {'regular_west': 51.369495, 'pollution': 51.408447, 'main': 51.415801, 'regular_east': 51.555203}
    geo_point = {}
    lat_random_list = numpy.arange(zone_start_lat_dic[zone], zone_end_lat_dic[zone], 0.000001)
    lng_random_list = numpy.arange(zone_start_lng_dic[zone], zone_end_lng_dic[zone], 0.000001)
    random.shuffle(lat_random_list)
    random.shuffle(lng_random_list)
    geo_point.update(lat=str(lat_random_list[0])[:9], lng=str(lng_random_list[0])[:9])
    return geo_point


def calculate_geo_distance(origin_lat, origin_lng, destination_lat, destination_lng):
    origin_latlon = geo.LatLon(origin_lat, origin_lng)
    dest_latlon = geo.LatLon(destination_lat, destination_lng)
    distance_per_meter = origin_latlon.distanceTo(dest_latlon)
    distance_per_km = distance_per_meter / 1000
    return distance_per_km


def calculate_geo_distance_from_api(origin_lat, origin_lng, dest_lat, dest_lng):
    headers = {'overview': 'false', 'geometries': 'polyline', 'steps': 'false', 'generate_hints': 'false'}
    request = "https://routing.apps.public.teh-1.snappcloud.io/route/v1/driving/{},{};{},{}".format(origin_lng,
                                                                                                    origin_lat,
                                                                                                    dest_lng, dest_lat)
    resp = get(url=request, headers=headers)
    distance_per_meter = resp.json()['routes'][0]['distance']
    distance_per_km = distance_per_meter / 1000
    return distance_per_km


def generate_geo_with_distance(lat, lng, distance, direction='east'):
    # distance in KM
    geo = {}
    constant = 0.143597
    factor = (float(distance) * 0.001) / constant
    if direction == 'east':
        geo.update(lat=str(float(lat) + factor)[:9], lng=str(float(lng) + factor)[:9])
    elif direction == 'west':
        geo.update(lat=str(float(lat) - factor)[:9], lng=str(float(lng) - factor)[:9])
    return geo


def generate_two_points_from_origin(origin_lat, origin_lng, distance, zone="regular_west"):
    """ This method gets origin lat&lng and produce two different geo points which have
    distance equals to 'distance' argument with each other.
    Returns 'close' which closer to origin and 'far' from origin."""
    geo = {}
    first_geo = generate_random_geo_points_of_tehran(zone=zone)
    second_geo = generate_geo_with_distance(lat=first_geo['lat'], lng=first_geo['lng'],distance=distance)
    first_from_origin = calculate_geo_distance_from_api(origin_lat, origin_lng, first_geo['lat'], first_geo['lng'])
    second_from_origin = calculate_geo_distance_from_api(origin_lat, origin_lng, second_geo['lat'], second_geo['lng'])
    if first_from_origin < second_from_origin:
        close_geo = first_geo
        far_geo = second_geo
    else:
        close_geo = second_geo
        far_geo = first_geo
    geo.update({'close_geo': close_geo, 'far_geo': far_geo})
    return geo


def compare_two_routes_length(origin_lat, origin_lng, lat1, lng1, lat2, lng2):
    geo1 = {'lat': lat1, 'lng': lng1}
    geo2 = {'lat': lat2, 'lng': lng2}
    result = {}
    first_from_origin = calculate_geo_distance_from_api(origin_lat, origin_lng, lat1, lng1)
    second_from_origin = calculate_geo_distance_from_api(origin_lat, origin_lng, lat2, lng2)
    if first_from_origin < second_from_origin:
        result.update({'shorter_points': geo1, 'longer_points': geo2})
    else:
        result.update({'shorter_points': geo2, 'longer_points': geo1})
    return result


def generate_random_string(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

