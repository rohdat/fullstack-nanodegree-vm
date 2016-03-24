from flask import Flask
app = Flask(__name__)
from database_setup import Restaurant, Base, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/hello')
def helloWorld():
	return "Hello Dumbass"

@app.route('/restaurants')
def allRestaurants():
	rs = session.query(Restaurant).all()
	output = ''
	for r in rs:
		output += '<a href=/restaurants/%s>%s</a>'%(r.id, r.name)
		output += '<br>'
		output += '<br>'

	return output

@app.route('restaurants/<int:restaurant_id>/edit')
def editMenu(restaurant_id):

@app.route('restaurants/<int:restaurant_id>/edit')

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	r = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	output = ''
	for i in items:
		output += i.name
		output += '<br>'
		output += i.price
		output += '<br>'
		output += i.description
		output += '<br>'
		output += '<a href="/restaurants/%s/edit">Edit</a>'%i.id
		output += '\t\t'
		output += '<a href="/restaurants/%s/delete">Delete</a>'%i.id
		output += '<br>'
		output += '<br>'
	return output

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port = 5000)