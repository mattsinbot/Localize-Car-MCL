#!/usr/bin/env python
from random import seed
from random import random
from random import randint
import numpy as np
import math
from tools import *


class Robot(object):
    def __init__(self):
        self.x = random() * world_sz_x
        self.y = random() * world_sz_y
        self.th = random() * 2 * np.pi

        self.lin_noise = 0.0
        self.ang_noise = 0.0
        self.sense_noise = 0.0

    def set(self, new_x, new_y, new_th):
        if new_x < 0 or new_x >= world_sz_x:
            raise Exception("X coordinate outside the world")
        if new_y < 0 or new_y >= world_sz_y:
            raise Exception("Y coordinate outside the world")
        if new_th < 0 or new_th >= 2*np.pi:
            raise Exception("Invalid: th must be in [0, ..., 2pi]")

        self.x = new_x
        self.y = new_y
        self.th = new_th

    def set_noise(self, new_lin_noise, new_ang_noise, new_sense_noise):
        self.lin_noise = new_lin_noise
        self.ang_noise = new_ang_noise
        self.sense_noise = new_sense_noise

    def sense(self):
        meas_array = [0]*len(landmarks)
        meas = 0

        for i in range(len(landmarks)):
            meas = np.sqrt((self.x - landmarks[i][0])**2 + (self.y - landmarks[i][1])**2)
            meas += np.random.normal(size=1, loc=0.0, scale=self.sense_noise)[0]  # loc and scale are mean and std respectively.
            meas_array[i] = meas

        return meas_array

    def move(self, move_lin, move_ang):
        if move_lin < 0:
            raise Exception("Backward movement not allowed")

        # Add noise to the move_lin, move_ang
        move_lin += np.random.normal(size=1, loc=0.0, scale=self.lin_noise)[0]
        move_ang += np.random.normal(size=1, loc=0.0, scale=self.ang_noise)[0]

        # Make the move
        self.x += move_lin * np.cos(self.th)
        self.y += move_lin * np.sin(self.th)
        self.th += move_ang

        # Cyclic truncate
        self.x = mod(self.x, world_sz_x)
        self.y = mod(self.y, world_sz_y)
        self.th = mod(self.th, 2*np.pi)

        # Create a new Robot object and set these values
        new_robot = Robot()
        new_robot.set(self.x, self.y, self.th)
        new_robot.set_noise(self.lin_noise, self.ang_noise, self.sense_noise)

        return new_robot

    def read_sensors(self):
        data = self.sense()
        data_str = "sensed readings: "
        for i in range(len(data)):
            data_str += str(data[i]) + " "
        return data_str

    def measurement_prob(self, meas_arr):
        prob = 1.0
        dist = 0.0
        for i in range(len(landmarks)):
            dist = np.sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= gaussian_pdf(dist, self.sense_noise, meas_arr[i])
        return prob

    def get_copy(self):
        rbt = Robot()
        rbt.set(self.x, self.y, self.th)
        rbt.set_noise(self.lin_noise, self.ang_noise, self.sense_noise)
        return rbt

    def __repr__(self):
        return "current pose: " + "x=" + str(self.x) + " y=" + str(self.y) + " th=" + str(self.th)
