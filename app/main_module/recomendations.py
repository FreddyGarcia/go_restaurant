from app import app

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData, Table
from collections import namedtuple

def initialize_db():

	DB_CONFIG = {
	    'PROTOCOL': 'mysql+pymysql',
	    'HOST': '127.0.0.1',
	    'USER': 'root',
	    'PASS': 'toor',
	    'DB': 'go_restaurant'
	}

	# uri connection string
	DATABASE_URI = "{PROTOCOL}://{USER}:{PASS}@{HOST}/{DB}?charset".format(**DB_CONFIG)

	Base = automap_base()

	# engine
	engine = create_engine(DATABASE_URI)

	# reflect the tables
	Base.prepare(engine, reflect=True)

	# Session object
	session = Session(engine)

	return session, Base


def get_recomendation_by_id(user_id):

	session, Base = initialize_db()

	result = session.execute('call get_recomended({0})'.format(user_id))

	Record = namedtuple('Record', result.keys())
	records = [Record(*r) for r in result.fetchall()]

	return records
