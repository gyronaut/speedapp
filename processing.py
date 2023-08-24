import gpxpy
import gpxpy.gpx
from datetime import timedelta
import numpy as np
import histogram as h

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
    conversion_factor = 2.23694 #conversion between m/s to miles/hour
    speedpoints = []
    for point_end, point_start in zip(datapoints[1:], datapoints):
        dist = great_circle_distance(point_end.latitude, point_end.longitude, point_start.latitude, point_start.longitude)
        dist = np.sqrt(np.power(dist, 2) + np.power(point_end.elevation - point_start.elevation, 2))
        time = (point_end.time - point_start.time)/timedelta(seconds=1)
        speed_point = {'speed': conversion_factor*dist/time, 'interval': time}
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
    histogram.plot() 
    
def process_strava_stream(activity):
    time = activity['time']['data']
    strava_velocity = activity['velocity_smooth']['data']
    latlng = activity['latlng']['data']
    distance = activity['distance']['data']

