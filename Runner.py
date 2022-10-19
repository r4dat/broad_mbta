from Graph import Graph
from Pathfinding import Pathfinding
from Routes import Routes
from Stops import Stops

if __name__ == '__main__':
    # Q 1 Long Name of Rail Lines
    R = Routes()
    subways = R.get_filtered_routes()
    R.print_rail_names(routes_list=subways)

    # Q 2
    # Name of routes with most/fewest stops.
    #
    S = Stops()
    S.print_min_max_stops()

    # Q2 List of Connecting Stops
    S.print_intersect_stops()

    # Q3 List a route from one stop to another.
    G = Graph()
    """Assumption of sequences being adjacent is no longer true for a multi-line pull.
    Sorting order or something else would probably solve it but since we know a single line
    works without issue we'll just update the adjac graph sequentially."""
    # G.update_adj_dict(S.get_filtered_stops(filt_func=S.filter_func_route_ls(subways)))
    for rail_id in Routes.get_rail_ids_ls():
        G.update_adj_dict(S.get_filtered_stops(filt_func=S.filter_func_route_str(rail_id)))
    PathInstance = Pathfinding(G)
    Src_Node = 'State'
    Dst_Node = 'Porter'
    c, station_path = PathInstance.dijkstra(Src_Node,Dst_Node)
    if c[Dst_Node]==1000:
        print(f"No path exists between {Src_Node} and {Dst_Node}.")
    else:
        LinePath = []
        for station in station_path:
            next_line = S.get_stops_to_line().get(station).copy().pop()
            if len(LinePath)==0:
                LinePath.append(next_line)
            if LinePath[len(LinePath)-1] != next_line:
                LinePath.append(next_line)
        print(f"{','.join(LinePath)}")


