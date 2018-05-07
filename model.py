from flask_sq import SQLAlchemy

db = SQLAlchemy()

##############################################################################
# Create ORM

class User(db.Model):
	"""User model."""

	
