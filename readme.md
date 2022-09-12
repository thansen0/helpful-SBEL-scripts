# Helpful Scripts

These are some of the scripts I've written over time, and I decided to collect them into a similar repo to make sharing easier.

Running the python scripts to extract message topics will include installing the dependencies, then 

```
 $ python imu_to_csv.py -i /path/to/rosbag/folder -o /path/to/any/output/folder
```

It will put the output in whatever directory you select (as given the same rosbag folder the data is stored in). What is important however is that the input directory must include both a `metadata.yml` file and the rosbag sqlite database `db_name.db3`. Input directory should be the folder that includes at least those two file. 


## Python packages

I tested these scripts in a virtual environment using `rosbags==0.9.12`, which you will need to install. You can view the [pypi page here](https://pypi.org/project/rosbags/) or install the latest version with 

```
pip install rosbags
```
## Bash scripts

I also have an example bash script if you want to run a variety of scripts against one or more rosbags, although you'll likely have to edit the file to what you need.

