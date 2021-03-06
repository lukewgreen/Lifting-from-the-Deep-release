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


DIR_PATH = dirname(realpath(__file__))
PROJECT_PATH = realpath(DIR_PATH + '/..')
IMAGE_FILE_PATH = '/Users/greenl/Downloads/cablepull1.jpg'
VIDEO_FILE_PATH = '/Users/greenl/Documents/pullups3.mp4'
SAVED_SESSIONS_DIR = PROJECT_PATH + '/data/saved_sessions'
SESSION_PATH = SAVED_SESSIONS_DIR + '/init_session/init'
PROB_MODEL_PATH = SAVED_SESSIONS_DIR + '/prob_model/prob_model_params.mat'
RUN_ON_SAVED = True

def main():
    if RUN_ON_SAVED:
        poses = np.load('poses-pullups3.npy')
    else:
        poses = []
        count = 0
        vidcap = cv2.VideoCapture(VIDEO_FILE_PATH)
        success,image = vidcap.read()
        success = True
        image_size = image.shape
        

        pose_estimator = PoseEstimator(image_size, SESSION_PATH, PROB_MODEL_PATH)

        # load model
        pose_estimator.initialise()

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        pose_2d, visibility, pose_3d = pose_estimator.estimate(image)

        poses.append(pose_3d)
        err_count = 0
        timestep = 50
        while success:
            vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*timestep))    # added this line 
            success,image = vidcap.read()
            try:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            except:
                print('skipping frame')
                count = count + 1
                err_count = err_count + 1
                if err_count == 2:
                    break
                else:
                    next
            print('a')
            print ('Read a new frame: ', success)
            try:
                pose_2d, visibility, pose_3d = pose_estimator.estimate(image)
                print('Successfully processed')
            except:
                pose_3d = pose_3d
                print('Not successfully processed - used last pose estimates')
            poses.append(pose_3d)
            print('Frames processed at {} frames per second: {}'.format(str(1000/timestep),str(count)))
            count = count + 1
        np.save('poses-pullups3.npy',poses)
        # Show 2D and 3D poses
        #display_results(image, pose_2d, visibility, pose_3d)
    plot_poses(poses)


def display_results(in_image, data_2d, joint_visibility, data_3d):
    """Plot 2D and 3D poses for each of the people in the image."""
    plt.figure()
    draw_limbs(in_image, data_2d, joint_visibility)
    plt.imshow(in_image)
    plt.axis('off')

    # Show 3D poses
    for single_3D in data_3d:
        # or plot_pose(Prob3dPose.centre_all(single_3D))
        plot_pose(single_3D)

    plt.show()

if __name__ == '__main__':
    import sys
    sys.exit(main())
