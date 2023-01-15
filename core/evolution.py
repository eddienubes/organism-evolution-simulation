import math
import operator
import common.simulation_config as sim_config

from collections import defaultdict
from core.organism import Organism
from math import floor
from random import randint
from random import random
from random import sample
from random import uniform


class Evolution:
    def run(self, organisms_old: list[Organism], gen):
        # how many elite organisms we want?
        elitism_num = int(floor(sim_config.ELITISM_BIAS * sim_config.POPULATION_SIZE))
        new_orgs = sim_config.POPULATION_SIZE - elitism_num

        # calculate stats for the old generation
        stats = defaultdict(float)
        stats['BEST'] = -math.inf
        stats['WORST'] = math.inf

        for org in organisms_old:
            if org.calories > stats['BEST']:
                stats['BEST'] = org.calories

            if org.calories < stats['WORST']:
                stats['WORST'] = org.calories

            stats['SUM'] += org.calories
            stats['VELOCITY_SUM'] += org.velocity
            stats['COUNT'] += 1

        stats['AVG'] = stats['SUM'] / stats['COUNT']
        stats['VELOCITY_AVG'] = stats['VELOCITY_SUM'] / stats['COUNT']

        # select the best ones
        orgs_sorted = sorted(organisms_old, key=operator.attrgetter('calories'), reverse=True)
        organisms_new = []
        for i in range(0, elitism_num):
            organisms_new.append(
                Organism(wih=orgs_sorted[i].wih, who=orgs_sorted[i].who, name=orgs_sorted[i].name))

        # select new organisms, but using their parent traits
        for new_organism in range(0, new_orgs):
            org_1, org_2 = self.__select(elitism_num, orgs_sorted)
            wih_new, who_new = self.__crossover(org_1, org_2)

            mutate = random()
            if mutate <= sim_config.MUTATION_RATE:
                wih_new, who_new = self.__mutate(wih_new, who_new)

            organisms_new.append(
                Organism(wih=wih_new, who=who_new, name='gen[' + str(gen) + ']-org[' + str(new_organism) + ']'))

        return organisms_new, stats

    def __select(self, elitism_num: int, orgs_sorted: list[Organism]):
        candidates = range(0, elitism_num)
        random_indices = sample(candidates, 2)
        org_1 = orgs_sorted[random_indices[0]]
        org_2 = orgs_sorted[random_indices[1]]

        return org_1, org_2

    def __crossover(self, org_1: Organism, org_2: Organism):
        crossover_weight = random()

        # x traits of wih of parent 1 and (1 - x) traits of parent 2 - the same applies to the who matrix
        wih_new = (crossover_weight * org_1.wih) + ((1 - crossover_weight) * org_2.wih)
        who_new = (crossover_weight * org_1.who) + ((1 - crossover_weight) * org_2.who)

        return wih_new, who_new

    def __mutate(self, wih_new, who_new):
        mat_pick = randint(0, 1)

        # mutate whi matrix
        if mat_pick == 0:
            index_row = randint(0, sim_config.HIDDEN_NODES_NUM - 1)
            index_col = randint(0, sim_config.INPUT_NODES_NUM - 1)
            wih_new[index_row][index_col] = wih_new[index_row][index_col] * uniform(0.9, 1.1)
        # mutate who matrix
        if mat_pick == 1:
            index_row = randint(0, sim_config.OUTPUT_NODES_NUM - 1)
            index_col = randint(0, sim_config.HIDDEN_NODES_NUM - 1)
            who_new[index_row][index_col] = who_new[index_row][index_col] * uniform(0.9, 1.1)

        return wih_new, who_new
