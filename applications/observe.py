#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Dec 20 17:39 2016

@author: Denis Tome'
"""

import __init__

from lifting import PoseEstimator
from lifting.utils import draw_limbs
from lifting.utils import plot_pose, plot_poses

import cv2
import matplotlib.pyplot as plt
from os.path import dirname, realpath
import numpy as np

import time

poses = np.load('Strong_Girl_Gymnast_Does_20+_Pull_Ups_Chin_Up_marcusbondi_pullup_f_cm_np1_fr_med_0.npy')

plot_poses(poses)