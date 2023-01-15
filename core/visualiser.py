import json
from math import cos, radians, sin

import common.visualiser_config as visualiser_config
import common.simulation_config as simulation_config
import matplotlib.animation as animation

from core.organism import Organism
from core.food import Food
from matplotlib import pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D


class Visualiser:
    state = {
        'organisms': [],
        'foods': []
    }

    def __init__(self):
        fig, ax = plt.subplots()
        self.label = plt.figtext(0.025, 0.90, f'TIMESTEP: ')
        self.fig = fig
        self.ax = ax
        self.loaded_state = {}

    def run(self):
        organisms_data_file = open(f'../data/{visualiser_config.ORGANISMS_DATA_FILE_NAME}', 'r')
        state = json.load(organisms_data_file)
        self.loaded_state = state

        ani = animation.FuncAnimation(self.fig, self.__animate, interval=visualiser_config.FRAME_RATE_INTERVAL_MS)
        # writer = animation.PillowWriter(fps=60,
        #                                 metadata=dict(artist='Me'))
        # ani.save('name.gif', writer=writer)
        plt.show()
        organisms_data_file.close()

    def __animate(self, iteration):
        print('Animation iteration: ', iteration)

        self.ax.clear()
        self.ax.set_aspect('equal')
        frame = plt.gca()
        frame.axes.get_xaxis().set_ticks([])
        frame.axes.get_yaxis().set_ticks([])
        plt.xlim([simulation_config.X_MIN + simulation_config.X_MIN * 0.25,
                  simulation_config.X_MAX + simulation_config.X_MAX * 0.25])
        plt.ylim([simulation_config.Y_MIN + simulation_config.Y_MIN * 0.25,
                  simulation_config.Y_MAX + simulation_config.Y_MAX * 0.25])

        # process organism
        for position in self.loaded_state['organisms'][iteration]:
            x1 = float(position['x1'])
            y1 = float(position['y1'])
            x2 = float(position['x2'])
            y2 = float(position['y2'])

            circle = Circle((x1, y1), visualiser_config.ORGANISM_SIZE, edgecolor='g', facecolor='lightgreen', zorder=8)
            edge = Circle((x1, y1), visualiser_config.ORGANISM_EDGE_SIZE, facecolor='None', edgecolor='darkgreen',
                          zorder=8)
            pointer = Line2D((x1, x2), [y1, y2], color='darkgreen', linewidth=1, zorder=10)

            self.ax.add_artist(circle)
            self.ax.add_artist(edge)
            self.ax.add_artist(pointer)

        # process food
        for position in self.loaded_state['foods'][iteration]:
            x1 = float(position['x1'])
            y1 = float(position['y1'])

            outer_circle = Circle((x1, y1), visualiser_config.FOOD_SIZE, edgecolor='darkslateblue',
                                  facecolor='mediumslateblue',
                                  zorder=5)
            self.ax.add_artist(outer_circle)

        self.label.set_text(f'TIMESTEP: {iteration}')

    @staticmethod
    def append_to_state(organisms: list[Organism], foods: list[Food]):
        organism_positions = []
        foods_positions = []
        for organism in organisms:
            x2 = cos(radians(organism.rotation)) * visualiser_config.DIRECTION_POINTER_LENGTH + organism.x
            y2 = sin(radians(organism.rotation)) * visualiser_config.DIRECTION_POINTER_LENGTH + organism.y
            position = {
                'x1': organism.x,
                'y1': organism.y,
                'x2': x2,
                'y2': y2,
                'tail_x': organism.tail_x,
                'tail_y': organism.tail_y
            }
            organism_positions.append(position)

        for food in foods:
            position = {
                'x1': food.x,
                'y1': food.y
            }

            foods_positions.append(position)

        Visualiser.state['organisms'].append(organism_positions)
        Visualiser.state['foods'].append(foods_positions)

    @staticmethod
    def save_state():
        organisms_data_file = open(f'../data/{visualiser_config.ORGANISMS_DATA_FILE_NAME}', 'w+')

        json.dump(Visualiser.state, organisms_data_file)
        organisms_data_file.close()
