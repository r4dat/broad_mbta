from ApiPull import ApiPull
from Routes import Routes

class Stops():

    stop_to_line_dict = {}
    def get_stops_to_line(self):
        """ Return dict of Stops : Line.
            Assumes default filters are used. """
        line_ids = Routes.get_rail_ids_dict()
        # Dict of StopName : Set (Rail Line 1... Rail Line N)

        # k,v id : long_name
        for k, v in line_ids.items():
            current_id_dict = {k: v}
            line_stops = self.get_filtered_stops(filt_func=self.filter_func(current_id_dict))
            for s in line_stops:
                stop_name = s.get('attributes').get('name')
                if stop_name not in self.stop_to_line_dict:
                    self.stop_to_line_dict[stop_name] = {v}
                else:
                    self.stop_to_line_dict[stop_name].add(v)
        return self.stop_to_line_dict

    def filter_func(self, id_dict):
        """ Generate filter strings for stops.
            From a dict whose keys are line IDs."""
        base_str = f"?filter[route]="
        route_str = ','.join(id_dict.keys())
        filter_str = f"{base_str}{route_str}"
        return filter_str

    def filter_func_route_str(self, route_string):
        """ Generate filter strings for stops.
            By custom string. E.g. "Red", "Red, Orange" etc."""
        base_str = f"?filter[route]="
        route_str = route_string
        filter_str = f"{base_str}{route_str}"
        return filter_str

    def filter_func_route_ls(self, rt_lst):
        """ Generate filter strings for stops.
            From iterable."""
        base_str = f"?filter[route]="
        ln_lst = []
        for ln in rt_lst:
            ln_lst.append(ln.get('id'))
        route_str = ','.join(ln_lst)
        filter_str = f"{base_str}{route_str}"
        return filter_str

    def get_filtered_stops(self, ttl_hash=None, filt_func=None):
        """ Return filtered list of stop dicts (JSON).
            Default filter is for Light and Heavy Rail (0,1)
            """

        stops_list = ApiPull.get_raw_resource(self, resource_str='stops', ttl_hash=ApiPull.get_ttl_hash(),
                                               filter_function=filt_func)
        return stops_list

    def print_min_max_stops(self):
        """ Print Lines with most and fewest stops.
            Default to subway filters, all lines."""
        line_ids = Routes.get_rail_ids_dict()
        min_stop,max_stop = 1000,0
        min_id,max_id = '',''
        for k,v in line_ids.items():
            current_id_dict = {k:v}
            line_stops = self.get_filtered_stops(filt_func=self.filter_func(current_id_dict))
            if len(line_stops) < min_stop:
                min_id = v
                min_stop = len(line_stops)
            if len(line_stops) > max_stop:
                max_id = v
                max_stop = len(line_stops)

        print(f"Most stops: {max_id}, Count: {max_stop}")
        print(f"Fewest stops: {min_id}, Count: {min_stop}")
        return

    def print_intersect_stops(self):
        """ Print all stations that have multiple lines passing through.
            Default filters to subway, all lines."""
       # Dict of StopName : Set (Rail Line 1... Rail Line N)
        possible_intersect_dict = self.get_stops_to_line()
        only_intersect_dict = {}
        for k, v in possible_intersect_dict.items():
            if len(v)>1:
                only_intersect_dict[k] = v

        for k,v in only_intersect_dict.items():
            print(f"Stop: {k}, Connecting Routes: {', '.join(v)}")
        return



