import os

# Enable Development enviroment
Debug = True

# Application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DB_CONFIG = {
	'USER' : 'postgres',
	'PASS' : 'toor',
	'HOST' : 'localhost',
	'NAME' : 'postgres',
	'PORT' : 5432
}

# Database config
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{USER}:{PASS}@{HOST}:{PORT}/{NAME}'.format(**DB_CONFIG)
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

# Mapbox config
MAPBOX_ACCESS_TOKEN = 'pk.eyJ1Ijoiem9yZW4xMDEiLCJhIjoiY2oza3ZtOHJlMDB2ZzJ3bjN2OGVoandzciJ9.-dWEZBmKwQvfkzsh3c72wA'
MAPBOX_MAP_ID  = 'mapbox.satellite'

# Session key
SECRET_KEY = 'secret'