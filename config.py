import os

# Enable Development enviroment
Debug = True

# Application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DB_CONFIG = {
    'PROTOCOL': 'mysql+pymysql',
    'HOST': '127.0.0.1',
    'USER': 'root',
    'PASS': 'toor',
    'PORT': '3306',
    'DB': 'go_restaurant'
}

# Database config
SQLALCHEMY_DATABASE_URI = "{PROTOCOL}://{USER}:{PASS}@{HOST}/{DB}".format(**DB_CONFIG)
# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{USER}:{PASS}@{HOST}:{PORT}/{NAME}'.format(**DB_CONFIG)
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

# Mapbox config
MAPBOX_ACCESS_TOKEN = 'pk.eyJ1Ijoiem9yZW4xMDEiLCJhIjoiY2oza3ZtOHJlMDB2ZzJ3bjN2OGVoandzciJ9.-dWEZBmKwQvfkzsh3c72wA'
MAPBOX_MAP_ID  = 'zoren101.cj3n1pd1k002x33ojv3fcogoq-1eqxa'

# Session key
SECRET_KEY = 'secret'