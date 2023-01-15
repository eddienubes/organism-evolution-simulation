import math

# Initials settings
GENERATIONS = 30
POPULATION_SIZE = 50  # organisms population
FOOD_NUM = 100 # food initial quantity
ELITISM_BIAS = 0.40  # elitism stage selection bias
MUTATION_RATE = 0.20  # chance for characteristics to be altered

# Simulation agents settings
GENERATION_TIMESTEPS_NUM = 100
DELTA_TIME = 0.09  # how much time does each frame consume
MAX_ROTATIONAL_SPEED_DG_PER_TIMESTEP = 720
MAX_VELOCITY_UNITS_PER_SEC = 0.85
MAX_ACCELERATION_UNITS_PER_TIMESTEP = 0.25
MIN_FOOD_DISTANCE_TO_CONSUME = 0.075
DEFAULT_ORGANISM_FOOD_DISTANCE = math.inf
DEFAULT_ORGANISM_FOOD_ROTATION = 0
DEFAULT_ORGANISM_NEIGHBOUR_DISTANCE = math.inf
CROWD_SLOWNESS_BIAS = 0.03
MIN_NEIGHBOUR_DISTANCE_FOR_CROWD = 0.03

# Arena settings
X_MIN = -2.0  # west
X_MAX = 2.0  # east
Y_MIN = -2.0  # south
Y_MAX = 2.0  # north

# Neural network set
# velocity, distance to food, rotation to food, distance to neighbour
INPUT_NODES_NUM = 4
HIDDEN_NODES_NUM = 3
OUTPUT_NODES_NUM = 2
