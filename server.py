from flask import Flask, session, render_template, request, flash, redirect, Markup, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import func
from model import *
from recommender import *

# -- coding: utf-8 --

app = Flask(__name__)
app.secret_key = "athena"

@app.route("/")
def welcome_user():
	"""Show login, signup, and search forms."""

	cities = (Restaurant.query.with_entities(Restaurant.city).group_by(Restaurant.city)
															 .order_by(Restaurant.city))
	print cities.all()

	return render_template("index.html", cities=cities)

@app.route("/cities.json")
def show_cities():
	"""Return list of cities from restaurants table."""

	cities = (Restaurant.query.with_entities(Restaurant.city).group_by(Restaurant.city)
															 .order_by(Restaurant.city)).all()

	return jsonify({'cities': cities})

@app.route("/signup")
def display_signup():
	"""Show signup form."""

	return render_template("signup.html")

@app.route("/handle-signup", methods=['POST'])
def create_user_account():
	"""Add new user to database."""

	# get username from form submission
	username = request.form['username']
	pw = request.form['password']

	# redirect to login page if user already has account
	if User.query.filter_by(username=username, password=pw).all():
		flash('Account already exists. Please log in.')
		return redirect("/login")
	
	# if user does not yet exist, add to db and redirect to login
	else:
		new_user = User(username=username,
						password=pw,
						score_avg=None)

		db.session.add(new_user)
		db.session.commit()
		flash("Account created! Please log in.")
		return redirect("/login")

@app.route("/login")
def display_login():
	"""Show login form."""

	return render_template("login.html")

@app.route("/handle-login", methods=['POST'])
def handle_login():
	"""Validate user info and save username in session."""
	
	# get username from form submission
	username = request.form['username']
	pw = request.form['password']

	user = User.query.filter_by(username=username, password=pw).first()

	# check if username and pw exist in db
	if user:
		session['username'] = user.username
		session['user_id'] = user.user_id
		return redirect("/profile")
	else:
		flash(Markup('Email and/or password is invalid. Please try again or <a href="/signup">create an account</a>.'))
		return redirect("/login")

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
		return redirect("/login")

	else:
		user = User.query.options(db.joinedload('ratings').joinedload('restaurants')).filter_by(username=session['username']).one()
		recs = show_top_picks(user)

		return render_template("profile.html", recs=recs)

@app.route("/top-picks.json")
def send_top_picks():
		user = User.query.options(db.joinedload('ratings').joinedload('restaurants')).filter_by(username=session['username']).one()
		recs = show_top_picks(user)

		return jsonify({'recs': recs})

@app.route("/search")
def show_search():
	"""Show search form and results."""

	return render_template("search-form.html")

@app.route("/search.json")
def show_search_results():
	"""Return user search results as a list."""

	search_string = request.args.get('search_string', None)
	city = request.args.get('city')
	price = request.args.get('price', None)
	
	results = user_search_results(city, search_string)

	return jsonify(results)

@app.route("/details/<restaurant_id>")
def show_details(restaurant_id):
	"""Show restaurant details."""

	r = Restaurant.query.filter_by(restaurant_id=restaurant_id).one()

	if 'user_id' in session:
		user = User.query.get(session['user_id'])
		rating = Rating.query.filter(Rating.user_id==session['user_id'], Rating.restaurant_id==restaurant_id).all()
		
		if rating:
			rating = rating[0].user_rating
	else:
		user = None
		rating = None

	return render_template("details.html", restaurant=r, session=session, user=user, rating=rating)

@app.route("/rate-restaurant", methods=['POST'])
def record_rating():
	"""Add user_rating to database."""

	rating = request.form.get('rating')
	restaurant_id = request.form.get('restaurant_id')
	user = User.query.filter_by(username=session['username']).one()

	existing_rating = Rating.query.filter(Rating.user_id==user.user_id, Rating.restaurant_id==restaurant_id).all()
	
	if existing_rating:
		existing_rating[0].user_rating = rating
		db.session.commit()
	else:
		new_rating = Rating(restaurant_id=restaurant_id,
							user_id=user.user_id,
							user_rating=rating)

		db.session.add(new_rating)
		db.session.commit()

	return redirect("/details/" + restaurant_id)

@app.route("/reviews")
def show_rated_restaurants():
	"""Show user restaurants she has already rated (and the rating she gave)."""

	if 'user_id' in session:
		# query for restaurant_id, name, price, user_rating
		reviews = (db.session.query(Rating.restaurant_id,
									Restaurant.name,
									Restaurant.price,
									Rating.user_rating).join(Restaurant, Restaurant.restaurant_id==Rating.restaurant_id)
													   .filter(Rating.user_id==session['user_id'])
													   .order_by(Rating.rating_id)).all()
		
		return render_template("user-reviews.html", reviews=reviews)

	else:
		return redirect("/search")


if __name__ == "__main__": # pragma: no cover
	app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
	app.debug = True

	connect_to_db(app)

	# Use the DebugToolbar
	DebugToolbarExtension(app)

	app.run(host="0.0.0.0")