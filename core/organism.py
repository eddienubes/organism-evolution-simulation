import numpy as np
import common.simulation_config as sim_config

from math import cos
from math import radians
from math import sin
from random import uniform


class Organism:
    def __init__(self, wih=None, who=None, name=None):

        self.x = uniform(sim_config.X_MIN, sim_config.X_MAX)  # position (x)
        self.y = uniform(sim_config.Y_MIN, sim_config.Y_MAX)  # position (y)
        self.tail_x = self.x
        self.tail_y = self.y

        # theta angle
        self.rotation = uniform(0, 360)
        # self.velocity = uniform(0, sim_config.MAX_VELOCITY_UNITS_PER_SEC)
        self.velocity = 0
        self.acceleration = uniform(-sim_config.MAX_ACCELERATION_UNITS_PER_TIMESTEP,
                                    sim_config.MAX_ACCELERATION_UNITS_PER_TIMESTEP)

        # used for nearest food
        self.food_distance = sim_config.DEFAULT_ORGANISM_FOOD_DISTANCE
        self.food_rotation = sim_config.DEFAULT_ORGANISM_FOOD_ROTATION
        self.calories = 0
        self.neighbour_distance = sim_config.DEFAULT_ORGANISM_NEIGHBOUR_DISTANCE

        self.wih = wih
        self.who = who

        self.name = name

    def move(self):
        activation_func = lambda x: np.tanh(x)

        inputs = [
            self.velocity,
            self.food_distance,
            self.food_rotation,
            self.neighbour_distance
        ]

        hidden_layer = activation_func(np.dot(self.wih, inputs))  # hidden layer
        output_layer = activation_func(np.dot(self.who, hidden_layer))  # output layer

        self.nn_delta_velocity = float(output_layer[0])  # [-1, 1]
        self.nn_delta_rotation = float(output_layer[1])  # [-1, 1]

        self.__update_rotation()
        self.__update_velocity()
        self.__update_position()

    def __update_rotation(self):
        self.rotation += self.nn_delta_rotation * sim_config.MAX_ROTATIONAL_SPEED_DG_PER_TIMESTEP * sim_config.DELTA_TIME
        self.rotation = self.rotation % 360


    def __update_velocity(self):
        self.velocity += self.nn_delta_velocity * sim_config.DELTA_TIME

        # clamp our value depending on what new velocity is
        if self.velocity < 0:
            self.velocity = 0
        if self.velocity > sim_config.MAX_VELOCITY_UNITS_PER_SEC:
            self.velocity = sim_config.MAX_VELOCITY_UNITS_PER_SEC

    def __update_position(self):
        # degrees * (pi / 180) = radian

        # calculate new vector heading proper way
        dx = self.velocity * cos(radians(self.rotation)) * sim_config.DELTA_TIME
        dy = self.velocity * sin(radians(self.rotation)) * sim_config.DELTA_TIME

        # move in the direction of this vector
        self.tail_x = self.x
        self.tail_y = self.y
        self.x += dx
        self.y += dy

    def apply_crowd_affect(self):
        self.velocity -= sim_config.CROWD_SLOWNESS_BIAS
