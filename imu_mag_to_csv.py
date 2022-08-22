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

topic = "/imu/mag"
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
    imu_data_file = open(os.path.join(output_path, "imu_mag_data.csv"), "w", newline='')
    imu_data_csv = csv.writer(imu_data_file)
    imu_data_csv.writerow(["seconds", "nanoseconds", "magnetic field x", "mag field y", "mag field z"])

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


            # sensor_msgs__msg__MagneticField(header=std_msgs__msg__Header(stamp=builtin_interfaces__msg__Time(sec=1657738033, nanosec=263924420, __msgtype__='builtin_interfaces/msg/Time'), frame_id='imu_link', __msgtype__='std_msgs/msg/Header'), magnetic_field=geometry_msgs__msg__Vector3(x=-0.5371105670928955, y=0.5926845073699951, z=-1.7204811573028564, __msgtype__='geometry_msgs/msg/Vector3'), magnetic_field_covariance=array([0., 0., 0., 0., 0., 0., 0., 0., 0.]), __msgtype__='sensor_msgs/msg/MagneticField')
            # print(data)
            # print("\n")

            tsecond = data.header.stamp.sec
            tnanosecond = data.header.stamp.nanosec
            
            mf_x = data.magnetic_field.x
            mf_y = data.magnetic_field.y
            mf_z = data.magnetic_field.z


            imu_data_csv.writerow([tsecond, tnanosecond, mf_x, mf_y, mf_z])

    imu_data_file.close()
