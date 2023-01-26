#!/bin/bash
# To use this file you simply pass in the director(ies) where your data is 
# stored, and it writes it back to those directories

if [ $# -le 0 ];
then
    echo "You must pass in at least one argument"
    exit
fi
echo "Recieved $# arg(s)"

for rb in "$@"
do
    python imu_to_csv.py -i $rb -o $rb
    python imu_filter_free_acceleration.py -i $rb -o $rb
    python imu_filter_positionlla.py -i $rb -o $rb
    python imu_filter_quaternion.py -i $rb -o $rb
    python imu_filter_twist.py -i $rb -o $rb
    python imu_filter_velocity.py -i $rb -o $rb
    python imu_mag_to_csv.py -i $rb -o $rb
    python mocap_pose_to_csv.py -i $rb -o $rb
    python control_inputs_to_csv.py -i $rb -o $rb
    python gnss_to_csv.py -i $rb -o $rb
    python mult_thread_camera_to_png.py -i $rb -o $rb
done
