from googlemaps.client import Client
from rdp import rdp
from haversine import haversine


class Manipulation:

    def __init__(self,
                 key=None,
                 map_serivce='GOOGLE'):

        if not key:
            raise ValueError("Must provide API key or enterprise credentials "
                             "when creating client.")
        if map_serivce == 'GOOGLE':
            self.client = Client(key=key)
        elif map_serivce == 'OSM':
            pass
        else:
            self.client = Client(key=key)

    def apply_rdp(self,
                  locations,
                  time_array,
                  epsilon=0.000005,
                  algo='iter'):

        if len(locations) < 1:
            return locations, time_array

        new_locations = []
        new_time_array = []
        after_rdp = rdp(locations, epsilon=epsilon, algo=algo, return_mask=True)
        for index, loc in enumerate(after_rdp):
            if loc is True:
                new_locations.append(locations[index])
                new_time_array.append(time_array[index])
        return new_locations, new_time_array

    def remove_consecutive_same_location(self,
                                         locations,
                                         time_array,
                                         bound=1,
                                         miles=False):

        new_locations = []
        new_locations_time = []
        remove_locations = []
        remove_locations_time = []
        if not locations or len(locations) < 2:
            return locations

        prev_coords = locations[0]
        new_locations.append(prev_coords)
        new_locations_time.append(time_array[0])
        index = 1
        for curr_cords in locations[1:]:
            if curr_cords == prev_coords:
                remove_locations.append(curr_cords)
                remove_locations_time.append(time_array[index])
            else:
                distance = self.calculate_distance(prev_coords, curr_cords)
                if float(distance) < bound:
                    remove_locations.append(curr_cords)
                    remove_locations_time.append(time_array[index])
                else:
                    new_locations.append(curr_cords)
                    new_locations_time.append(time_array[index])
                    prev_coords = curr_cords
            index += 1

        return new_locations, new_locations_time, remove_locations, remove_locations_time

    def remove_consecutive_same_location_using_google(self,
                                                      locations,
                                                      time_array,
                                                      bound=1,
                                                      miles=False):

        new_locations = []
        new_locations_time = []
        remove_locations = []
        remove_locations_time = []
        if not locations or len(locations) < 2:
            return locations

        prev_coords = locations[0]
        new_locations.append(prev_coords)
        new_locations_time.append(time_array[0])
        index = 1
        for curr_cords in locations[1:]:
            if curr_cords == prev_coords:
                remove_locations.append(curr_cords)
                remove_locations_time.append(time_array[index])
            else:
                distance = self.calculate_distance_using_google(prev_coords, curr_cords)
                if float(distance) < bound:
                    remove_locations.append(curr_cords)
                    remove_locations_time.append(time_array[index])
                else:
                    new_locations.append(curr_cords)
                    new_locations_time.append(time_array[index])
                    prev_coords = curr_cords
            index += 1

        return new_locations, new_locations_time, remove_locations, remove_locations_time

    def calculate_total_distance(self,
                                 user_locations):

        if len(user_locations) < 2:
            return float(0)

        distance = 0
        point1 = user_locations[0]
        for location in user_locations[1:]:
            point2 = location
            distance += haversine(point1=point1, point2=point2, miles=False)*1000
            point1 = point2
        return distance

    def calculate_total_distance_using_google(self,
                                              user_locations):

        if len(user_locations) < 2:
            return 0

        distance_in_meters = 0
        point1 = user_locations[0]
        for location in user_locations[1:]:
            point2 = location
            distance_in_meters += self.calculate_distance_using_google(point1=point1, point2=point2)
            point1 = point2
        return distance_in_meters

    def calculate_distance(self,
                           point1,
                           point2):
        distance = haversine(point1=point1, point2=point2, miles=False)
        distance_in_meters = distance*1000
        return distance_in_meters

    def calculate_distance_using_google(self,
                                        point1,
                                        point2):
        resp = self.client.distance_matrix(origins=tuple(point1),
                                           destinations=tuple(point2),
                                           mode='driving')

        distance_in_meters = self.get_shortest_distance_from_google_response(resp)
        return distance_in_meters

    def get_shortest_distance_from_google_response(self,
                                                   resp):
        rows = resp.get('rows')
        first_row = rows[0]
        elements = first_row.get('elements')
        get_all_distance = []
        for element in elements:
            get_all_distance.append(element.get('distance').get('value'))
        get_all_distance.sort()
        return get_all_distance[0]

    def apply_kalman(self):
        pass












