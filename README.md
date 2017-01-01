# location_manipulation

GPS tracks are collection of latitude, longitude, elevation, accuracy, timestamp etc. But some low-end
  devices can not provide accurate and reliable GPS tracks. Because of noisy and error prone GPS points, plotting these
  location tuples or analyzing them can be hard.<br><br>
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
