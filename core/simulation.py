import common.simulation_config as sim_config
from core.food import Food

from core.organism import Organism
from core.math_utils import distance, calc_heading
from core.visualiser import Visualiser


class Simulation:
    def run(self, organisms: list[Organism], foods, gen):
        total_time_steps = int(sim_config.GENERATION_TIMESTEPS_NUM / sim_config.DELTA_TIME)

        for t_step in range(0, total_time_steps, 1):
            # save timestep to the visualiser state
            if gen == sim_config.GENERATIONS - 1:
                # time.sleep(visualiser_config.FRAME_RATE_INTERVAL_MS / 1000)
                Visualiser.append_to_state(organisms, foods)

            self.__process_timestep(organisms, foods)
        return organisms

    def __process_timestep(self, organisms: list[Organism], foods: list[Food]):
        for org in organisms:
            self.__update_and_consume_food(org, foods)
            self.__update_neighbours(org, organisms)

            org.move()

    def __update_and_consume_food(self, org: Organism, foods: list[Food]):
        for food in foods:
            food_org_dist = distance(org.x, org.y, food.x, food.y)

            if food_org_dist <= sim_config.MIN_FOOD_DISTANCE_TO_CONSUME:
                org.calories += food.calories
                org.food_distance = sim_config.DEFAULT_ORGANISM_FOOD_DISTANCE
                org.food_rotation = sim_config.DEFAULT_ORGANISM_FOOD_ROTATION
                food.respawn()
                continue

            if food_org_dist < org.food_distance:
                org.food_distance = food_org_dist
                org.food_rotation = calc_heading(org, food)

    def __update_neighbours(self, current_org: Organism, organisms: list[Organism]):
        for neighbour in organisms:
            if neighbour is current_org:
                continue

            org_org_dist = distance(current_org.x, current_org.y, neighbour.x, neighbour.y)
            # update closest food if necessary
            if org_org_dist < current_org.neighbour_distance:
                current_org.neighbour_distance = org_org_dist

            # if org_org_dist <= sim_config.MIN_NEIGHBOUR_DISTANCE_FOR_CROWD:
            #     # print('Neighbour: ', neighbour.name)
            #     # print('Org: ', current_org.name)
            #     # print(org_org_dist)
            #     current_org.apply_crowd_affect()
