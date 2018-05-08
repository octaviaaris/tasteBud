from flask import Flask, sessoin, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolBarExtension
from model import *

app = Flask(__name__)


if __name__ == "__main__":
	app.run(debug=True)