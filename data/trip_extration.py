import json
import unittest
from datetime import datetime

from geopy.distance import geodesic


def get_time_difference(s1, s2):
    """
    This method gets the time difference between two string timestamps
    :param s1: timestamp in ISO 8601 format
    :param s2: timestamp in ISO 8601 format
    :return: seconds
    """

    return (datetime.strptime(s2['timestamp'], "%Y-%m-%dT%H:%M:%SZ") - datetime.strptime(s1['timestamp'],
                                                                                         "%Y-%m-%dT%H:%M:%SZ")).seconds


def get_distance(p1, p2):
    """
    This methods gets the distance btw two points using geodesic for geopy
    :param p1:  {'lat' : double, 'lng; :double, 'timestamp' : timestamp}
    :param p2:  {'lat' : double, 'lng; :double', timestamp' : timestamp}
    :return:  distance in meters and time difference
    """
    distance = geodesic((p1['lat'], p1['lng']), (p2['lat'], p2['lng']))
    # distance = haversine((p1['lat'], p1['lng']), (p2['lat'], p2['lng']))
    return int(distance.meters)


def get_speed(distance_covered, time_difference):
    """
    This method is used to get the speed
    :param distance_covered:
    :param time_difference:
    :return: speed in meters per second (m/s) as a float 2 decimal places
    """
    speed = distance_covered / time_difference
    return float(f'{speed:.2f}')


def get_trip_information(points):
    """
    this method is used to remove invalid coordinates, these are waypoints with a speed greater than 167 m/s
    10km in a minute
    :param filename:
    :return: list of clean coordinates
    """
    location_points = []
    i, distance_total, start, stopped_time = 0, 0, False, 0
    while i < len(points) - 1:
        distance = get_distance(points[i], points[i + 1])
        time_difference = get_time_difference(points[i], points[i + 1])
        speed = distance / time_difference
        distance_total += distance
        data = {'total_distance': distance_total,
                'speed': speed,
                'time_difference': time_difference,
                'start_point': points[i],
                'end_point': points[i + 1]}
        if speed < 167.67:
            location_points.append(data)
        i += 1
    i, started, start_location, stopped_location, stopped_time = 0, False, None, None, 0
    trips = []
    while i < len(location_points) - 1:
        if started is False:
            if location_points[i + 1]['total_distance'] - location_points[i]['total_distance'] >= 20 and \
                    location_points[i + 1]['speed'] - location_points[i]['speed'] > 1.0:
                start_location = location_points[i + 1]
                started = True
            stopped_location = None
            stopped_time = 0
        else:
            if int(location_points[i]['speed']) == 0 and int(location_points[i + 1]['speed']) == 0:
                if location_points[i + 1]['total_distance'] - location_points[i + 1]['total_distance'] <= 20:
                    stopped_time += location_points[i]['time_difference']
                    if stopped_location is None:
                        stopped_location = location_points[i]
                    else:
                        if stopped_time > 5 * 60:
                            started = False
                            trips.append({
                                'start': start_location['start_point'],
                                'end': stopped_location['start_point'],
                                'distance': stopped_location['total_distance'] - start_location['total_distance']
                            })
                            start_location = None
                            stopped_location = None
                            stopped_time = 0
            else:
                stopped_location = None
                stopped_time = 0
        i += 1

    if int(location_points[i]['speed']) == 0:
        stopped_time += location_points[i]['time_difference']
        if stopped_time > 5 * 60:
            trips.append({
                'start': start_location['start_point'],
                'end': stopped_location['start_point'],
                'distance': stopped_location['total_distance'] - start_location['total_distance']
            })

    return trips


def process_trips(filename):
    with open(filename, 'r') as file:
        location_points = json.load(file)
        return get_trip_information(location_points)


print('trips', process_trips('waypoints.json'))


class TestExtractTrips(unittest.TestCase):
    def test_get_time_difference(self):
        self.assertEqual(24,
                         get_time_difference({"lat": 51.54987, "timestamp": "2018-08-10T20:04:22Z", "lng": 12.41039},
                                             {"lat": 51.54987, "timestamp": "2018-08-10T20:04:46Z", "lng": 12.41031}))

    def test_get_distance(self):
        self.assertEqual(5,
                         get_distance(
                             {"lat": 51.54987, "timestamp": "2018-08-10T20:04:22Z", "lng": 12.41039},
                             {"lat": 51.54987, "timestamp": "2018-08-10T20:04:46Z", "lng": 12.41031}))

    def test_get_speed(self):
        self.assertEqual(10, get_speed(100, 10))


if __name__ == '__main__':
    unittest.main()
