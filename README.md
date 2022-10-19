# broad_mbta
Broad questions about MBTA API

## Question 1
Write a program that retrieves data representing all, what we'll call "subway" routes: "Light Rail" (type 0) and “Heavy Rail” (type 1). The program should list their “long names” on the console.
Partial example of long name output: Red Line, Blue Line, Orange Line...

There are two ways to filter results for subway-only routes. Think about the two options below and choose:
1. Download all results from https://api-v3.mbta.com/routes then filter locally
2. Rely on the server API (i.e., https://api-v3.mbta.com/routes?filter[type]=0,1) to filter before results
are received.

We rely on server-side filtering for this for two reasons: primarily for size and simplicity, but also because while filtering for subway-only routes is relatively easy, filtering for line specific stops (as in question 2) is less so. In order to reduce hard-coding and share API pull between Route and Stop endpoints we use server-side filtering for both. 


Sample output: 
> Red Line, Mattapan Trolley, Orange Line, Green Line B, Green Line C, Green Line D, Green Line E, Blue Line

## Question 2
Extend your program so it displays the following additional information.
1. The name of the subway route with the most stops as well as a count of its stops.
2. The name of the subway route with the fewest stops as well as a count of its stops.
3. A list of the stops that connect two or more subway routes along with the relevant route names for
each of those stops.

Sample output:
> Most stops: Green Line D, Count: 25
> 
> Fewest stops: Mattapan Trolley, Count: 8
> 
> Stop: Park Street, Connecting Routes: Red Line, Green Line E, Green Line B, Green Line D, Green Line C
> 
> Stop: Downtown Crossing, Connecting Routes: Orange Line, Red Line

## Question 3
Extend your program again such that the user can provide any two stops on the subway routes you listed for
question 1.
List a rail route you could travel to get from one stop to the other. 
Examples:
1. Davis to Kendall/MIT -> Red Line
2. Ashmont to Arlington -> Red Line, Green Line B

Sample output:
> Path State to Porter -> Blue Line,Red Line,Green Line B,Red Line

# General Design:
## ApiPull
The ApiPull class contains API interaction elements. In order to avoid hitting the MBTA API too often I've added a 1hr cache to the API calls. The API key is stored in the environment and retreived for use at run-time. 

## Routes and Stops classes
The Route and Stop classes make use of the ApiPull functions to retrieve their respective data - these could be subclasses of the ApiPull class but I instead decided to favor composition of the filter settings and method calls over inheritance when refactoring. 

## Graph and Pathfinding classes
The Graph class contains and constructs an adjacency dictionary of the graph. The current implementation was tested on single-lines initially, and so makes the assumption that sequential stops are adjacent. So adding all Red, then all Orange stops behaves as expected, but adding both at once (equivalent to "filter[route]=Red,Orange") creates an incorrect graph. 
The Pathfinding class accepts a graph at instatiation and performs Dijkstra's algorithm given a source station. It then returns a cost dictionary and a station based path from source to destination.

## Runner Class
This is a program runner. As a TODO we should really add argparse and create a command-line utility here. But a runner file is good enough for demonstration. For question 3 there is some functional code that should be pushed down into the Pathfinding class to return subway lines from stations. The subway-paths may look wonky because the transition from station -> line picks whichever is on top of the set, which may cause one-line dips in a station with multiple lines. E.g. Park Street is both Red Line and Green Line so a path through could have either. 

## Testing
Full testing framework was not completed though TODO tests are described in the tests folder. 

## General TODO
Need to commit to the classes holding a copy of their data with appropriate getters as needed. The two big issues are a lot of static/class methods scattered about, and right now there's a lot of calls hitting the LRU a layer or two deep, and portions where knowing the underlying representation is a dict of specific key:val design is needed. E.g. Rail ID : Long Name etc. Ideally the next person shouldn't have to know that. Also, should rewrite in Java. 

## Libraries
See environment.yaml for full environment. 
Primary installed libraries are Requests and Pytest.