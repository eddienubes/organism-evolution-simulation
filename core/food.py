import common.simulation_config as sim_config

from random import uniform


class Food:
    def __init__(self):
        self.x = uniform(sim_config.X_MIN, sim_config.X_MAX)
        self.y = uniform(sim_config.Y_MIN, sim_config.Y_MAX)
        self.calories = 1

    def respawn(self):
        self.x = uniform(sim_config.X_MIN, sim_config.X_MAX)
        self.y = uniform(sim_config.Y_MIN, sim_config.Y_MAX)
        self.calories = 1

    # def set_eaten(self):
    #     self.calories = 0
    #
    # def is_eaten(self):
    #     return self.calories == 0
