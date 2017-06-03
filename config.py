import os

# Enable Development enviroment
Debug = True

# Application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database config
SQLALCHEMY_DATABASE_URI = 'mysql://freddie:freddie@localhost/propietaria'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

SECRET_KEY = 'secret'