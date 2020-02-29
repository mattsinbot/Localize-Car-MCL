#!/usr/bin/env python
from robot_api import *
import math
import matplotlib.pyplot as plt

world_sz_x, world_sz_y = 100.0, 100.0
landmarks = [[20.0, 20.0], [20.0, 80.0], [20.0, 50.0], [50.0, 20.0], [50.0, 80.0], [80.0, 80.0], [80.0, 20.0], [80.0, 50.0]]


def mod(dividend, divisor):
    remainder = dividend - divisor*math.floor(dividend/divisor)
    return remainder


def gaussian_pdf(mean, std, variable):
    return math.exp(-(((mean - variable)/std)**2)/2.0)/(std*math.sqrt(2*np.pi))


def visualize(particles2, particles3, fake_rbt):
    # Plot the particles
    plt.grid()
    plt.xlim([0, world_sz_x])
    plt.ylim([0, world_sz_y])
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.title("World")

    # Plot the landmarks
    for i in range(len(landmarks)):
        if i == 0:
            plt.plot(landmarks[i][0], landmarks[i][1], "mo", label="land-marks")
        else:
            plt.plot(landmarks[i][0], landmarks[i][1], "mo")

    # Plot all the particles that moved
    for j in range(len(particles2)):
        if j == 0:
            plt.plot(particles2[j].x, particles2[j].y, "r.", label="after move step")
        else:
            plt.plot(particles2[j].x, particles2[j].y, "r.")
    plt.pause(0.1)

    # Plot all the particles after re-sampling step
    for k in range(len(particles3)):
        if k == 0:
            plt.plot(particles3[k].x, particles3[k].y, "b.", label="after re-sampling step")
        else:
            plt.plot(particles3[k].x, particles3[k].y, "b.")
    plt.pause(0.1)

    # Plot actual robot's location
    plt.plot(fake_rbt.x, fake_rbt.y, "go", label="actual location")

    plt.legend(loc="upper left", ncol=2)

    plt.pause(2.0)

    plt.cla()
