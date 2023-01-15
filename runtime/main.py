from core.evolution import Evolution
from core.game import Game
from core.simulation import Simulation

if __name__ == '__main__':
    simulation = Simulation()
    evolution = Evolution()
    game = Game(simulation, evolution)
    game.run()
