#!/usr/bin/env python
from random import seed
from random import random
from random import randint
from random import gauss
import math
import matplotlib.pyplot as plt

seed(100)

world_sz_x, world_sz_y = 100.0, 100.0
landmarks = [[20.0, 20.0], [20.0, 80.0], [20.0, 50.0], [50.0, 20.0], [50.0, 80.0], [80.0, 80.0], [80.0, 20.0], [80.0, 50.0]]
itr_count = 0


class Robot(object):
    def __init__(self):
        self.x = random() * world_sz_x
        self.y = random() * world_sz_y
        self.th = random() * 2 * math.pi

        self.lin_noise = 0.0
        self.ang_noise = 0.0
        self.sense_noise = 0.0

    def set(self, new_x, new_y, new_th):
        if new_x < 0 or new_x >= world_sz_x:
            raise Exception("X coordinate outside the world")
        if new_y < 0 or new_y >= world_sz_y:
            raise Exception("Y coordinate outside the world")
        if new_th < 0 or new_th >= 2*math.pi:
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
            meas = math.sqrt((self.x - landmarks[i][0])**2 + (self.y - landmarks[i][1])**2)
            # meas += np.random.normal(size=1, loc=0.0, scale=self.sense_noise)[0]  # loc and scale are mean and std respectively.
            meas += gauss(0.0, self.sense_noise) # loc and scale are mean and std respectively.
            meas_array[i] = meas

        return meas_array

    def move(self, move_lin, move_ang):
        if move_lin < 0:
            raise Exception("Backward movement not allowed")

        # Add noise to the move_lin, move_ang
        move_lin += gauss(0.0, self.lin_noise) # np.random.normal(size=1, loc=0.0, scale=self.lin_noise)[0]
        move_ang += gauss(0.0, self.ang_noise) # np.random.normal(size=1, loc=0.0, scale=self.ang_noise)[0]

        # Make the move
        self.x += move_lin * math.cos(self.th)
        self.y += move_lin * math.sin(self.th)
        self.th += move_ang

        # Cyclic truncate
        self.x = mod(self.x, world_sz_x)
        self.y = mod(self.y, world_sz_y)
        self.th = mod(self.th, 2*math.pi)

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
            dist = math.sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= gaussian_pdf(dist, self.sense_noise, meas_arr[i])
        return prob

    def get_copy(self):
        rbt = Robot()
        rbt.set(self.x, self.y, self.th)
        rbt.set_noise(self.lin_noise, self.ang_noise, self.sense_noise)
        return rbt

    def __repr__(self):
        return "current pose: " + "x=" + str(self.x) + " y=" + str(self.y) + " th=" + str(self.th)


def mod(dividend, divisor):
    remainder = dividend - divisor*math.floor(dividend/divisor)
    return remainder


def gaussian_pdf(mean, std, variable):
    return math.exp(-(((mean - variable)/std)**2)/2.0)/(std*math.sqrt(2*math.pi))


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
            plt.plot(landmarks[i][0], landmarks[i][1], "ko", label="land-marks",  markersize=12)
        else:
            plt.plot(landmarks[i][0], landmarks[i][1], "ko", markersize=12)

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

    # plt.legend(loc="upper left", ncol=2)
    plt.legend(bbox_to_anchor=(0.0, 1.15), loc="upper left", ncol=2)

    plt.savefig("./progress_image/itr"+str(itr_count)+".png", dpi=150)

    plt.pause(2.0)

    plt.cla()


if __name__ == "__main__":
    plt.figure()

    # Select number of iterations
    itr = 100
    mv_linear = 5.0
    mv_angular = 0.05

    # Create a bunch of particles (Robot object)
    num_particles = 1000
    particles = []
    for _ in range(num_particles):
        new_rbt = Robot()
        particles.append(new_rbt)

    # Set noise parameters of each particles
    for particle in particles:
        particle.set_noise(0.05, 0.05, 5.0)

    # Simulate a robot with a sensor attached to it which sends sensor data
    fake_rbt = Robot()

    # Create an array to store the measurements
    meas_arr = [0 for _ in range(len(landmarks))]

    # Start localization process iteratively
    for j in range(itr):
        print("Iteration: %d"%j)

        # Step-1: Move fake_rbt to get new sensed measurements
        fake_rbt = fake_rbt.move(mv_linear, mv_angular)
        meas_arr = fake_rbt.sense()
        print("End of step-1")

        # Step-2: Move all the particle with similar motion
        particles2 = []
        for i in range(num_particles):
            current_particle = particles[i]
            current_particle_moved = current_particle.move(mv_linear, mv_angular)
            particles2.append(current_particle_moved)
            particles[i] = current_particle_moved
        print("End of step-2")

        # Step-3: Compute weight of each particle (importance weighting)
        wgt = []
        for i in range(num_particles):
            wgt.append(particles[i].measurement_prob(meas_arr))
        print("End of step-3")

        # Step-4: Re-sample based on importance weight
        particles3 = []
        index = randint(0, num_particles-1)
        beta = 0.0
        max_wgt = max(wgt)

        for i in range(num_particles):
            beta += random() * 2 * max_wgt
            while beta > wgt[index]:
                beta -= wgt[index]
                index = mod(index + 1, num_particles)
            # print("index picked: {}".format(index))
            particles3.append(particles[index].get_copy())

        particles = []
        for i in range(num_particles):
            particles.append(particles3[i])
        print("End of step-4")

        print("end of iteration %d"%j)
        print("---------------------")

        itr_count += 1

        # Visualize
        visualize(particles2, particles3, fake_rbt)