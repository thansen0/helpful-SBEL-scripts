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

frame_counter = 0
output_path = args.output

if(not os.path.exists(output_path)):
    os.mkdir(output_path)

with ROS2Reader(rosbag_dir) as ros2_reader:

    # ros2_conns = [x for x in ros2_reader.connections.values() if x.topic in []]
    ros2_conns = [x for x in ros2_reader.connections] # if x.topic in topic_list]
    # print(ros2_conns)
    # print("\n\n")
    # print([x.topic for x in ros2_conns])
    ros2_messages = ros2_reader.messages(connections=ros2_conns)

    # create a file for each topic being written
    ART1_pose_file = open(os.path.join(output_path, "ART1_pose.csv"), "w", newline='')
    ART1_pose_csv = csv.writer(ART1_pose_file)
    ART1_pose_csv.writerow(["Seconds", "Nanoseconds", "x position", "y position", "z position", "x orientation", "y orientation", "z orientation", "w orientation"])

    # print("\nros2_messages:")
    # print(ros2_messages)
    for m, msg in enumerate(ros2_messages):
        (connection, timestamp, rawdata) = msg
        # print(connection.topic)

        # This will be position data
        if (connection.topic == "/ART1/pose" or connection.topic == "/ART2/pose"):
            data = deserialize_cdr(rawdata, connection.msgtype)

            # print(data)
            # print("")

            tsecond = data.header.stamp.sec
            tnanosecond = data.header.stamp.nanosec
            xx = data.pose.position.x
            yy = data.pose.position.y
            zz = data.pose.position.z
            ox = data.pose.orientation.x
            oy = data.pose.orientation.y
            oz = data.pose.orientation.z
            ow = data.pose.orientation.w

            ART1_pose_csv.writerow([tsecond, tnanosecond, xx, yy, zz, ox, oy, oz, ow])

    ART1_pose_file.close()
