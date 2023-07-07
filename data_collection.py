# Setup
from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Camera
from pathlib import Path
from datetime import datetime
from bngseg import util
import beamngpy
import bngseg
import matplotlib.pyplot as plt
import numpy as np
import time
import random

## VARIABLES ##

# Setup variables
home_dir = r"C:\Users\jazzy\Desktop\BeamNG"
user_dir = r"C:\Users\jazzy\Desktop\BeamNG"

# Scenario variables
map = "rb_ks_monza"
car_model = "2022__4_navaro_ssr_700_indycar"
start_pos = (-177.105, -106.766, 155.2)
start_rot_quat = (0, 0, -0.998, 0.0598)

# Number of images to capture
n = 10

# Camera positions
camera_positions = [((-0.3, 1, 2), (0, -1, 0))]

##############

# Start scenario
bng = util.quick_start(home_dir, user_dir)
scenario, car0 = util.quick_scenario(bng, map, car_model, start_pos, start_rot_quat)

# wait
input("Press Enter to start recording...")

# Record points
recorded_points = bngseg.record_points_from_car(car0)

# Create list of locations and directions to capture images on the track
locations = [bngseg.generate_random_point(recorded_points) for _ in range(n)]

# Attach cameras to car
cameras = bngseg.attach_cameras(camera_positions, car0)

# Generate images and save
bngseg.generate_paired_images_and_save(car0, locations, cameras)
