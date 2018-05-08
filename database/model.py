from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##############################################################################
# Create ORM

class User(db.Model):
	"""User model."""

	__tablename__ = "users"

	user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	fname = db.Column(db.String(25), nullable=False)
	lname = db.Column(db.String(25), nullable=False)
	email = db.Column(db.String(50), nullable=False)
	score_avg = db.Column(db.Float(asdecimal=True))

	def __repr__(self):
		return "<User user_id={id} email={email}>".format(id=self.user_id,
														  email=self.email)


class Restaurant(db.Model):
	"""Restaurant model."""

	__tablename__ = "restaurants"

	restaurant_id = db.Column(db.String(50), primary_key=True)
	name = db.Column(db.String(125), nullable=False)
	url = db.Column(db.String(300))
	address1 = db.Column(db.String(50))
	address2 = db.Column(db.String(50))
	address3 = db.Column(db.String(50))
	city = db.Column(db.String(25), nullable=False)
	state = db.Column(db.String(25), nullable=False)
	zipcode = db.Column(db.String(10), nullable=False)
	latitude = db.Column(db.Float(asdecimal=True))
	longitude = db.Column(db.Float(asdecimal=True))
	hours = db.Column(db.String(500))
	price = db.Column(db.Integer,
					  db.ForeignKey('prices.price_id'))
	yelp_rating = db.Column(db.Float(asdecimal=True))

	def __repr__(self):
		return "<Restaurant restaurant_id={id} name={name}>".format(id=self.restaurant_id,
															  		name=self.name)


class Rating(db.Model):
	"""Rating model."""

	__tablename__ = "ratings"

	rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	restaurant_id = db.Column(db.String(50), 
							  db.ForeignKey('restaurants.restaurant_id'), nullable=False)
	user_id = db.Column(db.Integer,
						db.ForeignKey('users.user_id'), nullable=False)
	user_rating = db.Column(db.Float(asdecimal=True), nullable=False)


	restaurants = db.relationship('Restaurant', backref='ratings')
	users = db.relationship('User', backref='ratings')

	def __repr__(self):
		return "<Rating rating_id={id}> user_rating={rating}".format(id=self.rating_id,
																	 rating=self.user_rating)


class Category(db.Model):
	"""Category model."""

	__tablename__ = "categories"

	category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	alias = db.Column(db.String(50))

	def __repr__(self):
		return "<Category category_id={id} alias={alias}>".format(id=self.category_id,
															 	  alias=self.alias)


class Rest_cat(db.Model):
	"""Rest_cat model."""

	__tablename__ = "rest_cats"

	rest_cat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	restaurant_id = db.Column(db.String(50),
							  db.ForeignKey('restaurants.restaurant_id'), nullable=False)
	category_id = db.Column(db.Integer,
					  		db.ForeignKey('categories.category_id'), nullable=False)


	categories = db.relationship('Category', backref='rest_cat')

	def __repr__(self):
		return "<Rest_cat restaurant_id={rest_id} category_id={cat_id}>".format(rest_id=self.restaurant_id,
																     			cat_id=self.category_id)


class Price(db.Model):
	"""Price model."""

	__tablename__ = "prices"

	price_id = db.Column(db.Integer, primary_key=True)

	def __repr__(self):
		return "<Price price_id={id}>".format(id=self.price_id)


##############################################################################
# Helper functions

def init_app():
	from flask import Flask
	app = Flask(__name__)

	connect_to_db(app)
	print "Connected to DB"


def connect_to_db(app):
	"""Connect the database to my Flask app"""

	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///project_db'
	app.config['SQLALCHEMY_ECHO'] = False
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.app = app
	db.init_app(app)


if __name__ == "__main__":

	init_app()
	db.create_all()

