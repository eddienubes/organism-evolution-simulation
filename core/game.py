import numpy as np
import numpy.random

import common.simulation_config as sim_config
from core.evolution import Evolution

from core.food import Food
from core.organism import Organism
from core.simulation import Simulation
from core.visualiser import Visualiser


class Game:
    def __init__(self, simulation: Simulation, evolution: Evolution):
        self.__simulation = simulation
        self.__evolution = evolution

    def run(self):
        numpy.random.seed()

        foods = []
        for i in range(0, sim_config.FOOD_NUM):
            foods.append(Food())

        organisms = []
        for i in range(0, sim_config.POPULATION_SIZE):
            wih_init = np.random.uniform(-1, 1,
                                         (sim_config.HIDDEN_NODES_NUM,
                                          sim_config.INPUT_NODES_NUM))  # mlp weights (input -> hidden)
            who_init = np.random.uniform(-1, 1,
                                         (sim_config.OUTPUT_NODES_NUM,
                                          sim_config.HIDDEN_NODES_NUM))  # mlp weights (hidden -> output)

            organisms.append(Organism(wih_init, who_init, name='generation[x]-org[' + str(i) + ']'))

        avgs = []
        avgs_v = []
        for gen in range(0, sim_config.GENERATIONS):
            organisms = self.__simulation.run(organisms, foods, gen)

            organisms, stats = self.__evolution.run(organisms, gen)
            avgs.append(stats['AVG'])
            avgs_v.append(stats['VELOCITY_AVG'])
            print('[Generation]: ', gen, ' [Best Calories]: ', stats['BEST'], ' [AVG Calories]: ', stats['AVG'],
                  '[Worst Calories]: ', stats['WORST'])

        print('[Entire game AVG]: ', sum(avgs) / len(avgs))
        print('[Entire game VELOCITY_AVG]: ', sum(avgs_v) / len(avgs_v))
        Visualiser.save_state()
