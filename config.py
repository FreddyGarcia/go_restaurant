import os

# Enable Development enviroment
Debug = True

# Application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database config
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:toor@localhost:5432/postgres'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

# Mapbox config
MAPBOX_ACCESS_TOKEN = 'pk.eyJ1Ijoiem9yZW4xMDEiLCJhIjoiY2oza3ZtOHJlMDB2ZzJ3bjN2OGVoandzciJ9.-dWEZBmKwQvfkzsh3c72wA'
MAPBOX_MAP_ID  = 'mapbox.satellite'

# Session key
SECRET_KEY = 'secret'