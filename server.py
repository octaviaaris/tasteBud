from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from model import *

app = Flask(__name__)
app.secret_key = "athena"

@app.route("/")
def welcome_user():

	return "Welcome!"


if __name__ == "__main__":
	app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

	# Use the DebugToolbar
	DebugToolbarExtension(app)

	app.run(debug=True, host="0.0.0.0")