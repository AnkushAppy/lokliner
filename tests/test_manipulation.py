from lokliner.smoother import Manipulation
import unittest
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

locations =  [
    [12.9956927,77.7296046 ],[ 12.9940198,77.7269958 ],[ 12.9902847,77.7264299 ],[ 12.9901569,77.7242155 ],\
    [ 12.992211,77.7190483 ],[ 12.9921783,77.719092 ],[ 12.9871973,77.7090469 ],[ 12.985359,77.7081672 ],\
    [ 12.9888217,77.7022373 ],[ 12.9891085,77.6993243 ],[ 12.9888217,77.7022373 ],[ 12.9902847,77.7264299 ],\
    [ 12.9902847,77.7264299 ],[ 12.9888279,77.687049 ], [ 12.9885003,77.6858858 ],[ 12.9904586,77.6801263 ],\
    [ 12.9886829,77.6803986 ],[ 12.9885611,77.67955], [ 12.9885611,77.67955], [ 12.9885611,77.67955]
]

time_array = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

sm = Manipulation(key='my_google_api_key')

class TestManipulation(unittest.TestCase):

    def test_calculate_distance(self):
        distance_in_meters = sm.calculate_distance(point1=locations[0], point2=locations[1])
        self.assertTrue(distance_in_meters >= 338, msg='calculate distance failed.')

    def test_calculate_distance_using_google(self):
        distance_in_meters = sm.calculate_distance_using_google(locations[0], locations[1])
        self.assertTrue(distance_in_meters >= 420, msg='calculate distance using google failed.')

    def test_calculate_total_distance(self):
        total_distance_in_meters = sm.calculate_total_distance(locations)
        self.assertTrue(total_distance_in_meters > 12400, msg='calculate total distance failed.')

    def test_calculate_total_distance_using_google(self):
        total_distance_in_meters = sm.calculate_total_distance_using_google(locations)
        self.assertTrue(total_distance_in_meters > 19100, msg='calculate total distance using google failed.')

    def test_apply_rdp(self):
        results = sm.apply_rdp(locations,
                               time_array,
                               algo='iter')
        expected_result = ([[12.9956927, 77.7296046], [12.9940198, 77.7269958], [12.9902847, 77.7264299],
                            [12.9901569, 77.7242155], [12.992211, 77.7190483], [12.9921783, 77.719092],
                            [12.9871973, 77.7090469], [12.985359, 77.7081672], [12.9888217, 77.7022373],
                            [12.9891085, 77.6993243], [12.9888217, 77.7022373], [12.9902847, 77.7264299],
                            [12.9888279, 77.687049], [12.9885003, 77.6858858], [12.9904586, 77.6801263],
                            [12.9886829, 77.6803986], [12.9885611, 77.67955]],
                           [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 20]
                           )
        self.assertTrue(results == expected_result)


    def test_remove_consecutive_same_location(self):
        results = sm.remove_consecutive_same_location(locations,
                                            time_array,
                                            bound=2,
                                            miles=False
                                            )
        expected_result = ([[12.9956927, 77.7296046], [12.9940198, 77.7269958], [12.9902847, 77.7264299],
                            [12.9901569, 77.7242155], [12.992211, 77.7190483], [12.9921783, 77.719092],
                            [12.9871973, 77.7090469], [12.985359, 77.7081672], [12.9888217, 77.7022373],
                            [12.9891085, 77.6993243], [12.9888217, 77.7022373], [12.9902847, 77.7264299],
                            [12.9888279, 77.687049], [12.9885003, 77.6858858], [12.9904586, 77.6801263],
                            [12.9886829, 77.6803986], [12.9885611, 77.67955]],
                           [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18],
                           [[12.9902847, 77.7264299], [12.9885611, 77.67955], [12.9885611, 77.67955]],
                           [13, 19, 20])
        self.assertTrue(results == expected_result)

    def test_remove_consecutive_same_location_using_google(self):
        results = sm.remove_consecutive_same_location_using_google(locations,
                                            time_array,
                                            bound=2,
                                            miles=False
                                            )
        expected_result = ([[12.9956927, 77.7296046], [12.9940198, 77.7269958], [12.9902847, 77.7264299],
                             [12.9901569, 77.7242155], [12.992211, 77.7190483], [12.9921783, 77.719092],
                             [12.9871973, 77.7090469], [12.985359, 77.7081672], [12.9888217, 77.7022373],
                             [12.9891085, 77.6993243], [12.9888217, 77.7022373], [12.9902847, 77.7264299],
                             [12.9888279, 77.687049], [12.9885003, 77.6858858], [12.9904586, 77.6801263],
                             [12.9886829, 77.6803986], [12.9885611, 77.67955]],
                            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18],
                            [[12.9902847, 77.7264299], [12.9885611, 77.67955], [12.9885611, 77.67955]],
                            [13, 19, 20])
        self.assertTrue(results == expected_result)

    def test_get_shortest_distance_from_google_response(self):
        resp = sm.client.distance_matrix(origins=tuple(locations[0]),
                                           destinations=tuple(locations[19]),
                                           mode='driving')

        distance_in_meters = sm.get_shortest_distance_from_google_response(resp=resp)
        self.assertTrue(distance_in_meters >= 7898, msg='calculate distance failed.')
