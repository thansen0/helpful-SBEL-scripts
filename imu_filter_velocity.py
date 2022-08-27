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

topic = "/filter/velocity"
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
    imu_data_file = open(os.path.join(output_path, "imu_filter_velocity.csv"), "w", newline='')
    imu_data_csv = csv.writer(imu_data_file)
    imu_data_csv.writerow(["seconds", "nanoseconds", "velocity_x", "velocity_y", "velocity_z"])

    # print("\nros2_messages:")
    # print(ros2_messages)
    for m, msg in enumerate(ros2_messages):
        (connection, timestamp, rawdata) = msg
        # print(connection.topic)
        
        if (connection.topic == topic):
            # define custom message type of following:
            # 
            type(connection.msgtype)
            data = deserialize_cdr(rawdata, connection.msgtype)

            # print(data)
            # print("\n")

            tsecond = data.header.stamp.sec
            tnanosecond = data.header.stamp.nanosec
            
            vel_x = data.vector.x
            vel_y = data.vector.y
            vel_z = data.vector.z



            imu_data_csv.writerow([tsecond, tnanosecond, vel_x, vel_y, vel_z])

    imu_data_file.close()
