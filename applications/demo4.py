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

DIR_PATH = dirname(realpath(__file__))
PROJECT_PATH = realpath(DIR_PATH + '/..')
IMAGE_FILE_PATH = '/Users/greenl/Downloads/cablepull1.jpg'
VIDEO_FILE_PATH = '/home/ubuntu/Landing/pullups3.mp4'
SAVED_SESSIONS_DIR = PROJECT_PATH + '/data/saved_sessions'
SESSION_PATH = SAVED_SESSIONS_DIR + '/init_session/init'
PROB_MODEL_PATH = SAVED_SESSIONS_DIR + '/prob_model/prob_model_params.mat'
RUN_ON_SAVED = False

def main():
    if RUN_ON_SAVED:
        poses = np.load('poses-pullups3-lqtest.npy')
    else:
        poses = []
        count = 0
        vidcap = cv2.VideoCapture(VIDEO_FILE_PATH)
        success,image = vidcap.read()
        success = True
        image = cv2.resize(image, (0,0), fx=0.3, fy=0.3)
        image_size = image.shape


        pose_estimator = PoseEstimator(image_size, SESSION_PATH, PROB_MODEL_PATH)

        # load model
        pose_estimator.initialise()

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        pose_2d, visibility, pose_3d = pose_estimator.estimate(image)

        poses.append(pose_3d)

        err_count = 0
        timestep = 50
        start_time = time.time()
        while success:
            try:
                vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*timestep))    # added this line
                success,image = vidcap.read()
                image = cv2.resize(image, (0,0), fx=0.3, fy=0.3)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            except:
                count = count + 1
                err_count = err_count + 1
                if err_count == 2:
                    break
                else:
                    next
            #print('a')
            #print ('Read a new frame: ', success)
            try:
                pose_2d, visibility, pose_3d = pose_estimator.estimate(image)
                #print('Successfully processed')
            except:
                pose_3d = pose_3d
                #print('Not successfully processed - used last pose estimates')
            poses.append(pose_3d)
            count = count + 1
            print(count)
        time_taken = time.time() - start_time
        print('number of frame processed: {} in {} seconds'.format(count,time_taken))
        np.save('poses-pullups3-lqtest2.npy',poses)
        print('FPS calculation rate: {}'.format(float(count)/time_taken))
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
