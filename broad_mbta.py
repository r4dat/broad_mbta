import requests
from os import getenv
from functools import lru_cache

BASE_URL = 'https://api-v3.mbta.com'
API_KEY = getenv('MBTAKEY')  # Normally we'd keep this in a secrets vault but for now into the env it goes.
LIGHT_RAIL, HEAVY_RAIL = 0, 1  # Defined in V3 MBTA API


# look adding TTL key to routes call - refresh every hour or 24h is probably reasonable.
@lru_cache(maxsize=24)
def __get_raw_routes():
    """ Get routes
        Return JSON response."""
    response = requests.get(f"{BASE_URL}/routes")
    return response.json()


@lru_cache(maxsize=24)
def get_filtered_routes(filter_set=set([LIGHT_RAIL, HEAVY_RAIL])):
    """ Return filtered list of routes JSON.
        Default filter is for Light and Heavy Rail (0,1)
        """
    raw_routes_list = __get_raw_routes().get('data')
    # There's a more concise (and probably faster) list/dict comprehension way to do this.
    filt_routes = []
    for route in raw_routes_list:
        if route.get('attributes').get('type') in filter_set:
            filt_routes.append(route)

    return filt_routes


def get_long_name(route_dict):
    long_name = route_dict.get('attributes').get('long_name')
    return long_name


if __name__ == '__main__':
    for route in get_filtered_routes():
        print(get_long_name(route))
