from flask import Flask
from mongokit import Connection, Document, IS
import datetime
import re


# Configuration
DEBUG = True
MONGODB_HOST = "localhost"
MONGODB_PORT = 27017

# Create the application object
app = Flask(__name__)
app.config.from_object(__name__)

# Connect to the database
connection = Connection(app.config["MONGODB_HOST"], app.config["MONGODB_PORT"])

# Mongo Validators
def email_validator(value):
	email = re.compile(r'(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)',re.IGNORECASE)
	if not bool(email.match(value)):
		raise ValidatorError('%s is not a valid email')   


# Mongo Schema
@connection.register
class RootDocument(Document):
	"""Foundation class for MongoKit usage."""
	use_dot_notation = True
	use_autorefs = True
	skip_validation = False
	structure = {}
	__database__ = "yr-internal"


@connection.register
class Person(RootDocument):
	__collection__ = "People"
	structure = {
		"first_name": unicode,
		"last_name": unicode,
		"nickname": unicode,
		"email": {
			"work": unicode,
			"home": unicode,
		},
		"phone": {
			"extension": basestring,
			"cell": basestring,
		},
		"emergency_contacts": {
			"full_name_1": unicode,
			"phone_1": basestring,
			"full_name_2": unicode,
			"phone_2": basestring,
		},
		"work_information": {
			"department": unicode,
			"title": unicode,
			"supervisor": unicode,
			"floor_captain": unicode,
		},
		"date_created": datetime.datetime,
		"date_modified": datetime.datetime
	}
	required_fields = ["first_name", "last_name", "email.work", "phone.cell"]
	default_values = {
		"date_created": datetime.datetime.utcnow,
		"date_modified": datetime.datetime.utcnow
	}

	def __repr__(self):
		return "<Person %r>" % (self.name)


@connection.register
class CheckIn(RootDocument):
	__collection__ = "CheckIns"
	structure = {
		"person": basestring,
		"status": IS(u'IN', u'OUT'),
		"timestamp": datetime.datetime
	}
	required_fields = ["person", "status", "timestamp"]
	default_values = {
		"timestamp": datetime.datetime.utcnow
	}

	def __repr__(self):
		return "<CheckIn %r>" % (self.name)


@app.route("/checkin/<user>", methods=["GET"])
def flask_checkin(user):
	error = None
	currentCheckin = connection.CheckIn()
	currentCheckin["person"] = user
	currentCheckin["status"] = u'IN'
	currentCheckin.save()
	return "{Success: True}"


if __name__ == "__main__":
	app.debug = app.config["DEBUG"]
	app.run()