from flask_sqlalchemy import SQLAlchemy
from correlation import pearson
from collections import defaultdict

db = SQLAlchemy()

##############################################################################
# Create ORM

class User(db.Model):
	"""User model."""

	__tablename__ = "users"

	user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	# fname = db.Column(db.String(25), nullable=False)
	# lname = db.Column(db.String(25), nullable=False)
	username = db.Column(db.String(25), unique=True)
	password = db.Column(db.String(25), unique=True)
	# email = db.Column(db.String(50), nullable=False)
	score_avg = db.Column(db.Float)

	def __repr__(self):
		return "<User user_id={id} username={username}>".format(id=self.user_id,
																username=self.username)

	def get_user_recs(self):
		"""Find other users who are most similar in their ratings to self."""

		UserRestaurants = db.aliased(Rating)
		RestaurantUsers = db.aliased(Rating)
		SimilarUsers = db.aliased(Rating)

		query = (db.session.query(Rating.user_id, Rating.user_rating, 
						  UserRestaurants.user_rating, UserRestaurants.restaurant_id,
						  RestaurantUsers.user_rating, RestaurantUsers.user_id).join(UserRestaurants, UserRestaurants.restaurant_id == Rating.restaurant_id)
																			   .join(RestaurantUsers, Rating.user_id == RestaurantUsers.user_id)
																			   .filter(UserRestaurants.user_id == self.user_id))

		paired_ratings = defaultdict(list)

		#  pairs are being duplicated (why?)
		#  create pairs of self's ratings and other user's ratings of restaurants
		for (rating_user_id, rating_user_rating,
			 user_restaurants_user_rating, user_restaurants_restaurant_id,
			 restaurant_users_user_rating, restaurant_users_user_id) in query:
			paired_ratings[rating_user_id].append((user_restaurants_user_rating, rating_user_rating))

		# find most similar users to self
		similarities = []

		for user, pairs in paired_ratings.iteritems():
			sim_score = pearson(pairs)
			similarities.append((pearson(pairs), user))
		
		similarities.sort(reverse=True)
		sim_users = similarities[:len(similarities)/2 + 1]
		sim_users_id = [s[1] for s in sim_users]

		#  use sim_users_id to generate user-based recommendations
		self_restaurants = set(r.restaurant_id for r in self.ratings)
		sim_user_restaurants = defaultdict(set)
		recommendations = set()

		for s in sim_users_id:
			sim_user_restaurants = (db.session.query(Rating, Restaurant)
				  				   .join(Restaurant, Restaurant.restaurant_id == Rating.restaurant_id)
				  				   .filter(Rating.user_id == s))

			for rating, restaurant in sim_user_restaurants:
				if rating.restaurant_id not in self_restaurants and rating.user_rating >= 4:
					recommendations.add(restaurant)

		return recommendations

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
	latitude = db.Column(db.Float)
	longitude = db.Column(db.Float)
	hours = db.Column(db.String(500))
	price = db.Column(db.Integer,
					  db.ForeignKey('prices.price'))
	yelp_rating = db.Column(db.Float)

	def __repr__(self):
		name = self.name
		name_for_output = name.encode('utf8', 'replace')
		return "<Restaurant restaurant_id={id} name={name}>".format(id=self.restaurant_id,
															  		name=name_for_output)

	def get_attributes(self):
		"""Return dictionary of self's attributes."""

		attributes = {}

		categories = [r.category for r in self.rest_cats]
		attributes['categories'] = categories
		attributes['price'] = self.price
		attributes['yelp_rating'] = self.yelp_rating
		# total is the total number of points a perfect match restaurant can have (total number of categories plus one for price and yelp_rating each)
		attributes['total'] = len(categories) + 2

		return attributes

	def find_sim_restaurants(self, city=None, price=None):
		"""Compares restaurant to all other restaurants in database and counts match score (based on categories, price and yelp_rating).
		Return top 5 matches."""

		matches = []
		self_attributes = self.get_attributes()

		#  only look at restaurants with 4 stars or above on yelp
		other_restaurants = Restaurant.query.filter(Restaurant.restaurant_id != self.restaurant_id, Restaurant.yelp_rating >= 4)

		for r in other_restaurants:
			other_attributes = r.get_attributes()
			match_score = 0.0

			for c in self_attributes['categories']:
				if c in other_attributes['categories']:
					match_score += 1

			if self_attributes['price'] == other_attributes['price']:
				match_score += 1

			if self_attributes['yelp_rating'] == other_attributes['yelp_rating']:
				match_score += 1

			# divide category match score by total possible points (number of anchor's categories + number of other's categories)
			match_score /= (self_attributes['total'] + other_attributes['total'])

			matches.append((match_score, r))

		matches.sort(reverse=True)

		top_matches = matches[:5]

		return top_matches

class Rating(db.Model):
	"""Rating model."""

	__tablename__ = "ratings"

	rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	restaurant_id = db.Column(db.String(50), 
							  db.ForeignKey('restaurants.restaurant_id'), nullable=False)
	user_id = db.Column(db.Integer,
						db.ForeignKey('users.user_id'), nullable=False)
	user_rating = db.Column(db.Float, nullable=False)


	restaurants = db.relationship('Restaurant', backref=db.backref('ratings',
																	order_by=rating_id))
	users = db.relationship('User', backref=db.backref('ratings',
														order_by=rating_id))

	def __repr__(self):
		return "<Rating rating_id={id} user_rating={rating}>".format(id=self.rating_id,
																	 rating=self.user_rating)

class Category(db.Model):
	"""Category model."""

	__tablename__ = "categories"

	category = db.Column(db.String(50), primary_key=True)

	def __repr__(self):
		return "<Category category={category}>".format(category=self.category)


class Rest_cat(db.Model):
	"""Rest_cat model."""

	__tablename__ = "rest_cats"

	rest_cat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	restaurant_id = db.Column(db.String(50),
							  db.ForeignKey('restaurants.restaurant_id'), nullable=False)
	category = db.Column(db.String(50),
					  	 db.ForeignKey('categories.category'), nullable=False)


	restaurants = db.relationship('Restaurant', backref=db.backref('rest_cats',
																   order_by=rest_cat_id))
	categories = db.relationship('Category', backref=db.backref('rest_cats',
																order_by=rest_cat_id))

	def __repr__(self):
		return "<Rest_cat restaurant_id={rest_id} category={category}>".format(rest_id=self.restaurant_id,
																     		   category=self.category)


class Price(db.Model):
	"""Price model."""

	__tablename__ = "prices"

	price = db.Column(db.Integer, primary_key=True)

	restaurants = db.relationship('Restaurant', backref=db.backref('prices',
																   order_by=price))

	def __repr__(self):
		return "<Price price={price}>".format(price=self.price)


##############################################################################
############################## Helper functions ##############################
##############################################################################

def init_app():
	from flask import Flask
	app = Flask(__name__)

	connect_to_db(app)
	print "Connected to DB"


def connect_to_db(app):
	"""Connect the database to my Flask app"""

	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///projectdb'
	app.config['SQLALCHEMY_ECHO'] = False
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.app = app
	db.init_app(app)


if __name__ == "__main__":

	init_app()
	db.create_all()

