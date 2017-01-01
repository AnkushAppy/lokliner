from googlemaps.client import Client
import googlemaps.exceptions


class Snapper:

    def __init__(self,
                 key=None,
                 map_serive='GOOGLE'
                 ):
        if not key:
            raise ValueError("Must provide API key or enterprise credentials "
                             "when creating client.")
        if map_serive == 'GOOGLE':
            self.client = Client(key=key)
        elif map_serive == 'OSM':
            pass
        else:
            self.client = Client(key=key)

    def snap_using_google_api(self,
                        locations,
                        time_array,
                        per_call=100,
                        interpolate=True
                        ):

        if len(locations) < 1:
            return locations, time_array

        if per_call > 100:
            per_call = 100

        new_location_array = []
        new_time_array = []

        i = 0
        number_of_locations = len(locations)

        while i*per_call < number_of_locations:

            current_n_locations = locations[i*per_call: (i+1)*per_call]
            snapped_locations = self.client.snap_to_roads(current_n_locations, interpolate=interpolate)
            i = i + 1

            if len(snapped_locations) <= 0:
                continue

            last_index_checked = -1
            for other_index, loc in enumerate(snapped_locations):

                index = loc.get('originalIndex', None)

                if index is None:
                    new_location_array.append(self.fetch_coordinates(loc))
                    new_time_array.append(time_array[last_index_checked])
                else:
                    new_location_array.append(self.fetch_coordinates(loc))
                    new_time_array.append(time_array[index])
                    last_index_checked = index

        return new_location_array, new_time_array

    def fetch_coordinates(self, loc):
        snapped_points = loc.get('location')
        return [snapped_points.get('latitude'), snapped_points.get('longitude')]





