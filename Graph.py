# There is probably a library for this but let's go from first principles I guess.

class Graph:

    adj_dict = {}
    # Create an adjacency dictionary of the form StopName : {Stop1, Stop2...}
    def update_adj_dict(self,line_stops):
        """Update adjacency dict from sequential list.
           We have assumed that adjacency is connection.
           E.g. [a,b,c] => a : [b], b:[a,c], c: [b]...
           Turns out: this is true when you send in a single Line
           like Red, or Blue, but is NOT true if you send in multiple lines. """
        for i in range(0, len(line_stops)):
            prev_val = i-1
            next_val = i+1
            curr_stop = line_stops[i].get('attributes').get('name')
            if curr_stop not in self.adj_dict:
                self.adj_dict[curr_stop] = set()
            if prev_val >= 0:
                self.adj_dict[curr_stop].add(line_stops[prev_val].get('attributes').get('name'))
            if next_val < len(line_stops):
                self.adj_dict[curr_stop].add(line_stops[next_val].get('attributes').get('name'))
        """ Test for disconnected graphs
            E.g. neither harvard nor davis may enter porter.
            Results in default cost (1000) for dest node."""
        # for v in self.adj_dict.values():
        #     v.discard('Porter')




    def print_adj_dict(self):
        """ Print adjacency dictionary.
            Should've done an override but less
            syntax sugar than Java."""
        print(self.adj_dict)
        return

    def get_adj_dict(self):
        return self.adj_dict
