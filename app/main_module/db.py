from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


'''
# Populate database
db.drop_all()
db.create_all()

# restaurants
db.session.add(Restaurant('Buen Sabor'))
db.session.add(Restaurant('Chino'))
db.session.add(Restaurant('Sabor'))
db.session.add(Restaurant('Test'))
db.session.commit()

# locations
db.session.add(Location('27 de febrero', (1,2), Restaurant.query.filter_by(name='Buen Sabor').one()))
db.session.add(Location('Por la Gomez', (1,2), Restaurant.query.filter_by(name='Buen Sabor').one()))
db.session.add(Location('Villa Faro', (1,2), Restaurant.query.filter_by(name='Sabor').one()))
db.session.add(Location('Zona Colonial', (1,2), Restaurant.query.filter_by(name='Chino').one()))
db.session.commit()
'''
