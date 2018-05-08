from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from model import *

app = Flask(__name__)
app.secret_key = "athena"

@app.route("/")
def welcome_user():

	return render_template("index.html", session=session)

@app.route("/login")
def display_login():

	return render_template("login.html")

@app.route("/handle-login", methods=['POST'])
def handle_login():
	"""Validate user info and save username in session."""
	
	# get username from form submission
	username = request.form['username']
	pw = request.form['password']

	# check if username and pw exist in db
	if User.query.filter_by(username=username, password=pw).all():
		session['username'] = username
		return redirect("/")
	else:
		flash('Email and/or password is invalid. Please try again.')
		return redirect("/login")

@app.route("/handle-logout")
def handle_logout():

	session.clear()

	return redirect("/")

@app.route("/signup")
def display_signup():

	return render_template("signup.html")

if __name__ == "__main__":
	# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

	connect_to_db(app)

	# Use the DebugToolbar
	DebugToolbarExtension(app)

	app.run(debug=True, host="0.0.0.0")