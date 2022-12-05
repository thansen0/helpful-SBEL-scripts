# /chrono_ros_bridge/output/gps/data
# type: sensor_msgs/msg/NavSatFix

from rosbags.rosbag2 import Reader as ROS2Reader
import sqlite3

from rosbags.serde import deserialize_cdr
import matplotlib.pyplot as plt
import numpy as np
# import cv2
import os
import collections
import argparse

import csv

parser = argparse.ArgumentParser(description='Extract images from rosbag.')
# input will be the folder containing the .db3 and metadata.yml file
parser.add_argument('--input','-i',type=str, help='rosbag input location')
parser.add_argument('--output','-o',type=str, help='image output directory')

args = parser.parse_args()

rosbag_dir = args.input

topic = "/chrono_ros_bridge/output/gps/data"
frame_counter = 0
output_path = args.output

if(not os.path.exists(output_path)):
    os.mkdir(output_path)

with ROS2Reader(rosbag_dir) as ros2_reader:

    ros2_conns = [x for x in ros2_reader.connections] # if x.topic in topic_list]
    # print(ros2_conns)
    # print("\n\n")
    print([x.topic for x in ros2_conns])
    ros2_messages = ros2_reader.messages(connections=ros2_conns)

    # create a file for each topic being written
    gnss_file = open(os.path.join(output_path, "chrono-gps.csv"), "w", newline='')
    gnss_csv = csv.writer(gnss_file)
    gnss_csv.writerow(["seconds", "nanoseconds", "latitude", "longitude", "altitude"])

    # print("\nros2_messages:")
    # print(ros2_messages)
    for m, msg in enumerate(ros2_messages):
        (connection, timestamp, rawdata) = msg
        # print(connection.topic)
        
        if (connection.topic == topic):
            data = deserialize_cdr(rawdata, connection.msgtype)

            # print(data)
            # print("\n\n")
            # print(data.latitude)

            tsecond = data.header.stamp.sec
            tnanosecond = data.header.stamp.nanosec
            
            latitude = data.latitude
            longitude = data.longitude
            altitude = data.altitude

            gnss_csv.writerow([tsecond, tnanosecond, latitude, longitude, altitude])

    gnss_file.close()


"""
sensor_msgs__msg__NavSatFix(header=std_msgs__msg__Header(stamp=builtin_interfaces__msg__Time(sec=0, nanosec=0, __msgtype__='builtin_interfaces/msg/Time'), frame_id='', __msgtype__='std_msgs/msg/Header'), status=sensor_msgs__msg__NavSatStatus(status=0, service=0, STATUS_NO_FIX=-1, STATUS_FIX=0, STATUS_SBAS_FIX=1, STATUS_GBAS_FIX=2, SERVICE_GPS=1, SERVICE_GLONASS=2, SERVICE_COMPASS=4, SERVICE_GALILEO=8, __msgtype__='sensor_msgs/msg/NavSatStatus'), latitude=43.07000758904729, longitude=-89.40002807693236, altitude=259.85730131871566, position_covariance=array([0., 0., 0., 0., 0., 0., 0., 0., 0.]), position_covariance_type=0, COVARIANCE_TYPE_UNKNOWN=0, COVARIANCE_TYPE_APPROXIMATED=1, COVARIANCE_TYPE_DIAGONAL_KNOWN=2, COVARIANCE_TYPE_KNOWN=3, __msgtype__='sensor_msgs/msg/NavSatFix')

"""
