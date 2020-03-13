#!/usr/bin/env python
from robot_api import *
from tools import *
from random import randint

if __name__ == "__main__":
    plt.figure()

    # Select number of iterations
    itr = 50

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
        fake_rbt = fake_rbt.move(5.0, 0.1)
        meas_arr = fake_rbt.sense()
        print("End of step-1")

        # Step-2: Move all the particle with similar motion
        particles2 = []
        for i in range(num_particles):
            current_particle = particles[i]
            current_particle_moved = current_particle.move(5.0, 0.1)
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

        # Visualize
        visualize(particles2, particles3, fake_rbt)
