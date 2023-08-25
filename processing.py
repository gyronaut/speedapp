import gpxpy
import gpxpy.gpx
from datetime import timedelta
import numpy as np
import histogram as h

#conversion between m/s to miles/hour
MPS_TO_MILESPERHOUR = 2.23694

def load_gpx():
    filename = 'C:/Users/JB/Downloads/Lunch_Run.gpx'
    gpx_file = open(filename, 'r')

    gpx = gpxpy.parse(gpx_file)

    datapoints = []
    for track in gpx.tracks:
        for segment in track.segments:
            datapoints.extend(segment.points)
    return datapoints

def great_circle_distance(end_lat, end_long, start_lat, start_long):
    r = 6378100
    lat1 = start_lat*np.pi/180.0
    lat2 = end_lat*np.pi/180.0
    long1 = start_long*np.pi/180.0
    long2 = end_long*np.pi/180.0
    delta_long = np.abs(long2 - long1)
    return r*(np.arctan2(np.sqrt(np.power(np.cos(lat1)*np.sin(delta_long), 2)+np.power(np.cos(lat1)*np.sin(lat2) - np.sin(lat1)*np.cos(lat2)*np.cos(delta_long), 2)), (np.sin(lat1)*np.sin(lat2) + np.cos(lat1)*np.cos(lat2)*np.cos(delta_long))))


def gpx_to_speed(datapoints):
    speedpoints = []
    for point_end, point_start in zip(datapoints[1:], datapoints):
        dist = great_circle_distance(point_end.latitude, point_end.longitude, point_start.latitude, point_start.longitude)
        dist = np.sqrt(np.power(dist, 2) + np.power(point_end.elevation - point_start.elevation, 2))
        time = (point_end.time - point_start.time)/timedelta(seconds=1)
        speed_point = {'speed': MPS_TO_MILESPERHOUR*dist/time, 'interval': time}
        speedpoints.append(speed_point)
    return speedpoints

def process_gpx():
    datapoints = load_gpx()
    speedpoints = gpx_to_speed(datapoints) 
    speeddata = []
    histogram = h.Histogram(low=0, high=10, numbins=50, x_label="mph", y_label="seconds")
    for point in speedpoints:
        speeddata.append(point['speed'])
        histogram.fill(point['speed'], point['interval'])
    histogram = histogram.rebin(5)
    return histogram

def process_strava_stream(activity):
    time = activity['time']['data']
    strava_velocity = activity['velocity_smooth']['data']
    latlng = activity['latlng']['data']
    distance = activity['distance']['data']
    timediff = [time2-time1 for time2, time1 in zip(time[1:], time)]
    speedpoints = [{'speed': v*MPS_TO_MILESPERHOUR, 'interval': t} for v, t in zip(strava_velocity[1:], timediff)]
    distdiff = [dist2-dist1 for dist2, dist1 in zip(distance[1:], distance)]
    speedpoints2 = [{'speed':MPS_TO_MILESPERHOUR*d/t, 'interval': t} for d, t in zip(distdiff, timediff)]
    h1 = h.Histogram(low=0, high=50, numbins=10, x_label="mph", y_label="minutes")
    h2 = h.Histogram(low=0, high=50, numbins=10, x_label="mph", y_label="minutes")
    for point1, point2 in zip(speedpoints, speedpoints2):
        h1.fill(point1['speed'], point1['interval'])
        h2.fill(point2['speed'], point2['interval'])
    h1.scale(1.0/60.0)
    h2.scale(1.0/60.0)
    return [h1, h2]