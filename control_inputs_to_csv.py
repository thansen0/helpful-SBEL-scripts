from rosbags.rosbag2 import Reader as ROS2Reader
import sqlite3

from rosbags.serde import deserialize_cdr
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
# import cv2
import os
import collections
import argparse

import csv

# from std_msgs.msg import String

parser = argparse.ArgumentParser(description='Extract images from rosbag.')
# input will be the folder containing the .db3 and metadata.yml file
parser.add_argument('--input','-i',type=str, help='rosbag input location')
parser.add_argument('--output','-o',type=str, help='image output directory')

args = parser.parse_args()

rosbag_dir = args.input

from rosbags.typesys import get_types_from_msg, register_types

# path to message example, can copy into this directory
VehicleInput_msg_path = Path('./msgs/VehicleInput.msg')
vh_def = VehicleInput_msg_path.read_text(encoding='utf-8')
register_types(get_types_from_msg(
        vh_def, 'art_msgs/msg/VehicleInput2'))

from rosbags.typesys.types import art_msgs__msg__VehicleInput2 as VehicleInput2
vh_msg_type = VehicleInput2.__msgtype__


topic = "/control/vehicle_inputs"
frame_counter = 0
output_path = args.output

if(not os.path.exists(output_path)):
    os.mkdir(output_path)

with ROS2Reader(rosbag_dir) as ros2_reader:

    # ros2_conns = [x for x in ros2_reader.connections.values() if x.topic in []]
    ros2_conns = [x for x in ros2_reader.connections] # if x.topic in topic_list]
    # print(ros2_conns)
    # print("\n\n")
    print([x.topic for x in ros2_conns])
    ros2_messages = ros2_reader.messages(connections=ros2_conns)

    # create a file for each topic being written
    control_input_file = open(os.path.join(output_path, "control_vehicle_input.csv"), "w", newline='')
    control_vehicle_inputs_csv = csv.writer(control_input_file)
    control_vehicle_inputs_csv.writerow(["second", "nanosecond", "steering", "throttle", "braking"])

    # print("\nros2_messages:")
    # print(ros2_messages)
    for m, msg in enumerate(ros2_messages):
        (connection, timestamp, rawdata) = msg
        

        if (connection.topic  == topic):
            data = deserialize_cdr(rawdata, vh_msg_type)
            # Early versions didn't have a header, more recent ones do. Be sure to check 
            # Whether you need the header or not

            tsecond = data.header.stamp.sec
            tnanosecond = data.header.stamp.nanosec

            steering = data.steering
            throttle = data.throttle
            braking = data.braking

            control_vehicle_inputs_csv.writerow([tsecond, tnanosecond, steering, throttle, braking])


    control_input_file.close()
