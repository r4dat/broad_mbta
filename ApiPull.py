import requests
from os import getenv
from functools import lru_cache
import time
from abc import abstractmethod


def __reqerrorhandler(response):
    """A rough and ready exception class, grab anything not 200 OK."""
    raise ValueError(f"{response.status_code}, {response.reason}")


class ApiPull:
    """API Interaction Class"""

    @staticmethod
    def get_ttl_hash(seconds=3600):
        """Return the same value within `seconds` time period"""
        # Depends on system clock, if this is a problem look at monotonic time.
        return round(time.time() / seconds)

    # There are some API elements that can handle "modified since"
    # And let the server handle unchanged with an HTTP code.
    # For now just adding a TTL hash to the lru call.
    # https://stackoverflow.com/questions/31771286/python-in-memory-cache-with-time-to-live

    @staticmethod
    @lru_cache(maxsize=24)
    def get_raw_resource(self, resource_str='routes', ttl_hash=None, filter_function=None):
        """ Get MBTA resource specified by 'resource_str', default to 'routes'.
            TTL hash is used to cache at 1h intervals.
            Filter_fucnction: a function returing a filter string.
            Returns: List of dictionaries in API response."""
        __BASE_URL = 'https://api-v3.mbta.com'
        __API_KEY = getenv('MBTAKEY')  # Normally we'd keep this in a secrets vault but for now into the env it goes.
        __header_data = {'X-API-Key': __API_KEY}
        __URL = ''
        if filter_function is None:
            __URL = f"{__BASE_URL}/{resource_str}"
        else:
            __URL = f"{__BASE_URL}/{resource_str}{filter_function}"
        response = requests.get(__URL, headers=__header_data)
        if response.status_code != 200:
            self.__reqerrorhandler(response)
        return response.json().get('data')  # return data list.

    @abstractmethod
    def __filter_func(self):
        """Function generating filter string(s).
           Expected subclass implementation."""
        pass

    def get_long_name(route_dict):
        """Return human readable names (str) from a single route entry (JSON/DICT)."""
        long_name = route_dict.get('attributes').get('long_name')
        return long_name

    def print_rail_names():
        """For utility, print all human readable strings in an iterable list."""
        for route in get_filtered_routes(ttl_hash=get_ttl_hash()):
            print(get_long_name(route))
        return

    def get_rail_names_ls():
        """Return list of human readable route strings."""
        out = []
        for route in get_filtered_routes(ttl_hash=get_ttl_hash()):
            out.append(get_long_name(route))
        return out

    def raw_get_stops_from_lines():
        """For all stops, keep only stops matching subway IDs.
           This is deprecated because there is no easy way to
           get only 1 per station, stops set contains multiple
           fare collection points per station. Easier to just filter
           via API call.
           """
        subway_lines = get_rail_names_ls()
        # ID is Red, Orange, Blue, Mattapan, Green-B etc.
        stops_list = __get_raw_resource(resource_str='stops')
        s_list = []
        for item in stops_list:
            if item.get('attributes').get('description') is None:
                continue
            if any(s in item.get('attributes').get('description') for s in subway_lines):
                s_list.append(item)
        return s_list

