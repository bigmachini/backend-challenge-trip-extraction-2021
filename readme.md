# Vimcar Coding Challenge: Trip Extraction

One of Vimcar's successful products is the digital logbook. The purpose
of a logbook is to maintain a complete, consistent list of all trips a 
vehicle has made over time. 

There are many different use-cases for this, one of them is taxation. 
Our customers e.g. maintain a logbook, to keep track of how many trips were 
made privately and how many kilometers were driven in a business context.


## The trip extraction

The central piece of the logbook is the trip extraction. Trip extraction is the process of 
determining when a vehicle starts and stops moving based on data collected by gps trackers.


When driving from A to B, a user will probably have interruptions like stopping at red lights, 
traffic jams, tunnels. The expected behavior is to have one trip accounting for the whole 
journey, and not broken trips like from A to first red light etc.


GPS technology has some limitations which the trip extraction should account for. 
Within cities the GPS precision may be poorer than 15 meters and the GPS position might even "jump", 
due to bad reception caused by reflections on building. There are places without gps signal
like tunnels and underground parking lots.


## The task

Your challenge is to write a simplified version of the trip extraction.

The input is supplied in a file and contains a list of Waypoints, this is the gps information 
collected for one vehicle. A waypoint has the following structure. 

- `timestamp` – string, a timestamp in ISO 8601 format
- `lat` – float, Latitude of the GPS coordinate (WGS84)
- `lng` – float, Longitude of the GPS coordinate (WGS84)

The output is a list of Trips. A trip contains the start and end locations and the distance driven.
A trip has the following structure. 

- `start` – object, the start of the trip in Waypoint schema (see above)
- `end` – object, the end of the trip in Waypoint schema (see above)
- `distance` – int, the distance of the trip in meters

The distance is the the sum of all distances between the individual waypoints of the trip and has to be 
calculated.
 

The trip extraction uses the following logic:

- A trip is considered ended when a moving vehicle remains within a circle of 20 meters radius for longer than 5 minutes.

- A trip is considered started when the vehicle moves outside the circle of 20 meters radius around its rest position.

- If the change in distance is more than 10 km per minute, the waypoint "jumps" and should be ignored.


The `data` folder contains a sample of input and output data.


## Evaluation

The focus of the evaluation will be clean, readable and tested code which follows best practices.


##
Remarks: I was not able to get the same distance as the trip json file
I tried three libraries and the math function on calculating distance but
none ws able to give the same distance

For the last trip the time constraint doesnt meet the 5 min window within a 20m radius
the difference in time is less that 300 secods
