import os

class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    
    USERS_FILE = os.path.join(DATA_DIR, 'users.xlsx')
    PRODUCTS_FILE = os.path.join(DATA_DIR, 'products.xlsx')
    RATINGS_FILE = os.path.join(DATA_DIR, 'ratings.xlsx')
    BEHAVIOR_FILE = os.path.join(DATA_DIR, 'behavior.xlsx')
    
    # Genetic Algorithm Settings
    GA_POPULATION_SIZE = 50
    GA_GENERATIONS = 20
    GA_MUTATION_RATE = 0.1
    GA_CROSSOVER_RATE = 0.8
