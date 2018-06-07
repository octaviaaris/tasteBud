from flask import Flask, session, render_template, request, flash, redirect, Markup, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import func
from model import *
from recommender import *
import json

# -- coding: utf-8 --

app = Flask(__name__)
app.secret_key = "athena"

@app.route("/")
def welcome_user():
	"""Show login, signup, and search forms."""
	if 'username' in session:
		return redirect("/profile")
	return render_template("index.html", home=True)

@app.route("/signup")
def display_signup():
	"""Show signup form."""

	return render_template("signup.html", signup=True)

@app.route("/handle-signup", methods=['POST'])
def create_user_account():
	"""Add new user to database."""

	# get username from form submission
	username = request.form['username']
	pw = request.form['password']

	# redirect to login page if user already has account
	if User.query.filter_by(username=username, password=pw).all():
		flash('Account already exists. Please log in.')
		return redirect("/")
	
	# if user does not yet exist, add to db and redirect to login
	else:
		new_user = User(username=username,
						password=pw,
						score_avg=None)

		db.session.add(new_user)
		db.session.commit()
		flash("Account created! Please log in.")
		return redirect("/")

# @app.route("/handle-login", methods=['POST'])
# def handle_login():
# 	"""Validate user info and save username in session."""

# 	# get username from form submission
# 	username = request.form['username']
# 	pw = request.form['password']

# 	user = User.query.filter_by(username=username, password=pw).first()

# 	# check if username and pw exist in db
# 	if user:
# 		session['username'] = user.username
# 		session['user_id'] = user.user_id
# 		return redirect("/profile")
# 	else:
# 		flash(Markup('Email and/or password is invalid. Please try again or <a href="/signup">create an account</a>.'))
# 		return redirect("/")

@app.route("/handle-login", methods=['POST'])
def handle_login():
	"""Redirects user to profile."""
	if 'username' in session:
		return redirect("/profile")
	else:
		return redirect("/")

@app.route("/handle-logout")
def handle_logout():
	"""Clear username from session."""

	session.clear()

	return redirect("/")

@app.route("/profile")
def show_profile():
	"""Show user's top recommendations."""

	if 'username' not in session:
		flash(Markup('Log in to see your profile or <a href="/signup">create one now</a>!'))
		return redirect("/")

	return render_template("profile.html", profile=True)

@app.route("/search")
def show_search():
	"""Show search form and results."""
	
	if 'username' not in session:
		flash(Markup('Log in to find new eats or <a href="/signup">create a new profile now</a>!'))
		return redirect("/")

	return render_template("search-form.html")


@app.route("/details/<restaurant_id>")
def show_details(restaurant_id):
	"""Show restaurant details."""

	session["restaurant_id"] = restaurant_id

	if 'user_id' in session:
		return render_template("details.html")
	
	else:
		flash(Markup('Log in to review new restaurants or <a href="/signup">create a new profile now</a>!'))
		return redirect("/")


@app.route("/reviews")
def show_rated_restaurants():
	"""Show user restaurants she has already rated (and the rating she gave)."""

	if 'user_id' in session:
		return render_template("user-reviews.html", reviews=True)

	else:
		flash(Markup('Log in to see your reviews or <a href="/signup">create a new profile now</a>!'))
		return redirect("/")

########################################
####### routes for ajax requests #######
########################################

@app.route("/check-credentials.json", methods=['POST'])
def check_credentials():
	"""Validate user info and save username in session."""

	# get username from form submission
	username = request.form['username']
	pw = request.form['password']

	user = User.query.filter_by(username=username, password=pw).first()

	# check if username and pw exist in db, add to session
	if user:
		session['username'] = user.username
		session['user_id'] = user.user_id
		return "success"
	else:
		return "fail"

@app.route("/cities.json")
def show_cities():
	"""Return list of cities from restaurants table."""

	cities = (Restaurant.query.with_entities(Restaurant.city).group_by(Restaurant.city)
															 .order_by(Restaurant.city)).all()
	print cities
	return jsonify({'cities': cities})

@app.route("/top-picks.json")
def send_top_picks():
	"""Return dictionary of top restaurant recommendations."""

	user = (db.session.query(User).join(Rating, Rating.user_id==User.user_id)
								 .join(Restaurant, Restaurant.restaurant_id==Rating.restaurant_id)
								 .filter(User.username==session['username']).one())
		
	recs = show_top_picks(user)

	recs_dict = {rec.restaurant_id: {"name": rec.name,
									 "price": rec.price,
									 "yelp_rating": rec.yelp_rating,
									 "categories": [c.category for c in rec.rest_cats],
									 "address1": rec.address1,
									 "city": rec.city,
									 "state": rec.state,
									 "zipcode": rec.zipcode} for rec in recs}

	return jsonify(recs_dict)

@app.route("/search.json")
def show_search_results():
	"""Return user search results as a list."""

	search_string = request.args.get('search_string', None)
	city = request.args.get('city')
	
	results = user_search_results(city, search_string)

	return jsonify(results)

@app.route("/details.json")
def get_retaurant_details():
	"""Return dictionary of retaurant details."""

	restaurant_id = session['restaurant_id']

	r = Restaurant.query.filter_by(restaurant_id=restaurant_id).one()

	details = {'restaurant_id': restaurant_id,
			   'name': r.name,
			   'categories': [c.category for c in r.rest_cats],
			   'price': r.price,
			   'yelp_rating': r.yelp_rating,
			   'address1': r.address1,
			   'city': r.city,
			   'state': r.state,
			   'zipcode': r.zipcode,
			   'yelp_url': r.url}

	return jsonify(details)

@app.route("/rate-restaurant.json")
def rate_restaurant():
	
	rating = float(request.args.get('rating'))
	restaurant_id = session['restaurant_id']
	user_id = session['user_id']

	existing_rating = Rating.query.filter(Rating.user_id==user_id,
										  Rating.restaurant_id==restaurant_id).first()

	if existing_rating:
		existing_rating.user_rating = rating
		db.session.commit()
	else:
		new_rating = Rating(restaurant_id=restaurant_id,
							user_id=user_id,
							user_rating=rating)

	return jsonify({"rating": rating})

@app.route("/user-rating.json")
def get_user_rating():
	"""Return user rating for retaurant."""

	restaurant_id = session['restaurant_id']
	user_id = session['user_id']

	rating = Rating.query.filter(Rating.restaurant_id==restaurant_id,
								 Rating.user_id==user_id).first()

	if rating:
		return jsonify({'userRating': rating.user_rating})

	return None

@app.route("/reviews.json")
def show_user_reviews():
	"""Return list of restaurants (and details in tuples) user has rated.
	
	reviews = [(restaurant_id, name, price, city, user_rating)]

	"""

	reviews = (db.session.query(Rating.restaurant_id,
								Restaurant.name,
								Restaurant.price,
								Restaurant.city,
								Rating.user_rating,).join(Restaurant, Restaurant.restaurant_id==Rating.restaurant_id)
												    .filter(Rating.user_id==session['user_id'])
												    .order_by(Rating.rating_id)).all()
	
	review_dict = {}
	i = 0
	for review in reviews:
		review_dict[i] = {'restaurant_id': review[0],
						  'name': review[1],
						  'price': review[2],
						  'city': review[3],
						  'user_rating': review[4]}
		i+= 1

	return jsonify(review_dict)

if __name__ == "__main__": # pragma: no cover
	app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
	app.debug = True

	connect_to_db(app)

	# Use the DebugToolbar
	DebugToolbarExtension(app)

	app.run(host="0.0.0.0")