from rosbags.rosbag2 import Reader as ROS2Reader
from rosbags.serde import deserialize_cdr
import sqlite3

from multiprocessing.pool import ThreadPool
#from multiprocessing import Pool
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import collections
import argparse
from PIL import Image

import csv

def write_image(data, img_time, frame_counter):
    img = data.data.reshape(720, 1280, 3)

    pil_img = Image.fromarray(img)
    pil_img.save(os.path.join(output_path, "camera/frame_{:05d}.png".format(frame_counter)))

    #print("Img", frame_counter)
    return


parser = argparse.ArgumentParser(description='Extract images from rosbag.')
# input will be the folder containing the .db3 and metadata.yml file
parser.add_argument('--input','-i',type=str, help='rosbag input location')
parser.add_argument('--output','-o',type=str, help='image output directory')

args = parser.parse_args()

rosbag_dir = args.input

topic = "/sensing/front_facing_camera/raw"
frame_counter = 0
output_path = args.output

if not os.path.exists( os.path.join(output_path, "camera") ):
    os.makedirs( os.path.join(output_path, "camera") )

if(not os.path.exists(output_path)):
    os.mkdir(output_path)

with ROS2Reader(rosbag_dir) as ros2_reader:

    ros2_conns = [x for x in ros2_reader.connections] # if x.topic in topic_list]
    # print(ros2_conns)
    # print("\n\n")
    print([x.topic for x in ros2_conns])
    ros2_messages = ros2_reader.messages(connections=ros2_conns)

    # create thread pool
    pool = ThreadPool()
    # frame_counter = 0

    # print("\nros2_messages:")
    # print(ros2_messages)
    for m, msg in enumerate(ros2_messages):
        (connection, timestamp, rawdata) = msg
        # print(connection.topic)
        
        if (connection.topic == topic):
            # define custom message type of following:
            # type(connection.msgtype)
            data = deserialize_cdr(rawdata, connection.msgtype)
            img_time = data.header.stamp.sec + data.header.stamp.nanosec/1e9

            #pool.map(write_image(data, img_time, frame_counter), range(393))
            pool.apply_async(write_image, [data, img_time, frame_counter])

            frame_counter += 1


    pool.close()
    pool.join()

