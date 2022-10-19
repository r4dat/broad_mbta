from ApiPull import ApiPull


class Routes():
    # Defined in business case.
    LIGHT_RAIL, HEAVY_RAIL = 0, 1  # Defined in V3 MBTA API

    def __filter_func():
        """Generate filter strings for Routes."""
        filter_str = f"?filter[type]=0,1"
        return filter_str

    def get_filtered_routes(self, ttl_hash=None, filt_func=__filter_func()):
        """ Return filtered list of route dicts (JSON).
            Default filter is for Light and Heavy Rail (0,1).
            """
        routes_list = ApiPull.get_raw_resource(self, resource_str='routes', ttl_hash=ApiPull.get_ttl_hash(),
                                               filter_function=filt_func)
        return routes_list

    def get_long_name(self, route_dict):
        """Get human readable strings from individual route dict/JSON."""
        long_name = route_dict.get('attributes').get('long_name')
        return long_name

    def print_rail_names(self, routes_list):
        """Helper function, print all human readable route str from list of routes."""
        str_list = []
        for route in routes_list:
            str_list.append(self.get_long_name(route))
        print(', '.join(str_list))
        return

    @classmethod
    def get_rail_ids_dict(cls):
        """ Return dict of line IDs : Long Names.
            Assumes default filter is used."""
        subway_list = cls.get_filtered_routes(self=cls)
        rail_id_dict = {}
        for line in subway_list:
            rail_id_dict[line.get('id')] = line.get('attributes').get('long_name')
        return rail_id_dict

    @classmethod
    def get_rail_ids_ls(cls):
        """ Return list of line IDs.
            Assumes default filtered routes is used."""
        return cls.get_rail_ids_dict().keys()
