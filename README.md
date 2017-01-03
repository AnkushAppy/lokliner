### Simplifying location points

GPS tracks are collection of latitude, longitude, elevation, accuracy, timestamp etc. But some low-end
  devices can not provide accurate and reliable GPS tracks. Because of noisy and error prone GPS points, plotting these
  location tuples or analyzing them can be hard. <br><br>
We need to clean and process gps tracks before plotting them . Here, we will try to create APIs useful for cleaning,
    filtering, smoothing, reducing number of points, interpolating etc. these location points.<br><br>
For now we have distance and snap-to-road api using googlemaps api. Some of approach to reduce to reduce teh number
of points can be:<br>
1) Removing every nth point<br>
2) Removes consecutive points within certain distance<br>
3) Removes consecutive points more then certain distance in lesser time (google distance or haversine library)<br>
4) RDP Algorithm
(https://pypi.python.org/pypi/rdp or https://pypi.python.org/pypi/simplification/)<br>
5) Remove points within a radius.<br>

Some useful reads:<br>
https://www.toptal.com/gis/adventures-in-gps-track-analytics-a-geospatial-primer <br>
https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm<br>
https://en.wikipedia.org/wiki/Kalman_filter<br>
https://github.com/googlemaps/google-maps-services-python<br>

### Usage

##### Installation
```
pip install lokliner
```

##### Using on waypoints

```
locations =  [
    [12.9956927,77.7296046 ], [ 12.9940198,77.7269958 ], [ 12.9902847,77.7264299 ], [ 12.9901569,77.7242155 ],\
    [ 12.992211,77.7190483 ],[ 12.9921783,77.719092 ],[ 12.9871973,77.7090469 ],[ 12.985359,77.7081672 ],\
    [ 12.9888217,77.7022373 ],[ 12.9891085,77.6993243 ],[ 12.9888217,77.7022373 ],[ 12.9902847,77.7264299 ],\
    [ 12.9902847,77.7264299 ],[ 12.9888279,77.687049 ], [ 12.9885003,77.6858858 ],[ 12.9904586,77.6801263 ],\
    [ 12.9886829,77.6803986 ],[ 12.9885611,77.67955], [ 12.9885611,77.67955], [ 12.9885611,77.67955]
]
```

<br>


```
# Items in time_array should be equal to points in location array
# time_array is supposed to be time. Here we have taken numbers in increasing order

time_array = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
```
<br>


```
# Initialize Manipulation with google api key

from lokliner.smoother import Manipulation
sm = Manipulation(key='my_google_api_key')
```

```
# Calculate distance using haversine

distance_in_meters = sm.calculate_distance(point1=locations[0], point2=locations[1])
```
338.3744749682981

```
# calculate distance using google distance matrix api

distance_in_meters = sm.calculate_distance_using_google(locations[0], locations[1])
```
428

```
# Params: location, time_array, bound In meteres, miles False
# Returns: new_locations, new_locations_time, remove_locations, remove_locations_time

results = sm.remove_consecutive_same_location_using_google(locations,
                                            time_array,
                                            bound=2,
                                            miles=False
                                            )
```
([[12.9956927, 77.7296046], [12.9940198, 77.7269958], [12.9902847, 77.7264299],
[12.9901569, 77.7242155], [12.992211, 77.7190483], [12.9921783, 77.719092],
[12.9871973, 77.7090469], [12.985359, 77.7081672], [12.9888217, 77.7022373],
[12.9891085, 77.6993243], [12.9888217, 77.7022373], [12.9902847, 77.7264299],
[12.9888279, 77.687049], [12.9885003, 77.6858858], [12.9904586, 77.6801263],
[12.9886829, 77.6803986], [12.9885611, 77.67955]],
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18],
[[12.9902847, 77.7264299], [12.9885611, 77.67955], [12.9885611, 77.67955]],
[13, 19, 20])


```
from lokliner.snapper import Snapper
sm = Snapper(key='my_google_api_key')
result = sm.snap_using_google_api(
            locations=locations,
            time_array=time_array,
            per_call=50,interpolate=True
        )

```
Result of above snap: green are four original points. Blue line is Google's snapped and interpolated points.<br>
[![snap_google.png](https://s28.postimg.org/d16dud7od/snap_google.png)](https://postimg.org/image/hn2i2pt7d/)