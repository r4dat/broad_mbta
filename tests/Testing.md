# TODO Testing for Classes/Methods
## API Pull
* Test response code error handling - slow down if rate-limited, etc. 
* Confirm non-200 response code isn't getting cached in LRU. 
* resource_str (API Endpoint) is a free string e.g. stops, routes. This should be validated against Swagger doc endpoints and tested for. 
* What is req and test for no API key? If it's missing/malformed it drops back to the public rate-limit. 

## Graph
* Confirm graph fails gracefully with an empty update. 
* Test seq to adj. E.g. [a,b,c] => a : [b], b:[a,c], c: [b]...
* Detect non-unique vertices

## Pathfinding
* Test source != target. 
* Test source and target exist in graph. 
* Test Dijkstra's on disconnected graphs. 
* Station strings currently case-sensitive, fix and test. 

## Stops
* Should have a test confirming the generation of intersection stops is working. 
* Test case for min/max stops. 