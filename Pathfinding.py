from queue import PriorityQueue


class Pathfinding():
    """Pathfinding class that accepts a graph G for instantiation,
       and finds a path between two named graph nodes."""
    cost = {}
    parent = {}
    graph = []
    src_station, dest_station = '',''

    def __init__(self, graph):
        self.visited = []
        self.graph = graph
        for k in graph.get_adj_dict().keys():
            self.cost[k] = 1000
            self.parent[k] = None

    def PathErrors(self):
        """Internal error handling function.
           Currently checking for invalid graph nodes:
           No such named node, and src=destination."""
        graph = self.graph.get_adj_dict()
        if (self.src_station not in graph) or (self.dest_station not in graph):
            raise ValueError('Invalid Stop Name')
        if (self.src_station == self.dest_station):
            raise ValueError('Same Start and Destination Stops')
        return

    def dijkstra(self, src, target):
        """An implementation of Djikstra's algorithm.
           Returns a cost dictionary (distance from source nodes),
           and the first (lowest cost because PQ) Station Path between
           nodes."""
        self.src_station = src
        self.dest_station = target
        graph = self.graph.get_adj_dict()
        self.PathErrors()
        cost = self.cost
        parent = self.parent


        dist_min = 1000
        seen = set()
        cost[src] = 0

        pq = PriorityQueue()
        pq.put((0, src))

        AllPaths = []

        while not pq.empty():
            (dist, current_vertex) = pq.get()
            self.visited.append(current_vertex)
            for neighbor in graph.keys():
                if neighbor in graph.get(current_vertex):
                    distance = 1
                    if neighbor not in self.visited:
                        prev_cost = cost[neighbor]
                        new_cost = cost[current_vertex] + distance
                        if new_cost < prev_cost:
                            pq.put((new_cost, neighbor))
                            cost[neighbor] = new_cost
                            parent[neighbor] = current_vertex
            s = []
            u = current_vertex
            while parent[u] is not None:
                s.insert(0, u)
                u = parent[u]

            s.insert(0, src)
            AllPaths.append(s)

        FirstPath = []
        for p in AllPaths:
            if all(x in p for x in [src,target]):
                FirstPath=p

        return cost, FirstPath
