from flask.ext.wtf import Form
from wtforms import StringField, SelectField, HiddenField, validators
from wtforms.validators import DataRequired
import sqlite3
from random import randint
from datetime import datetime
from Station import Station

def getStationList():
	connection = sqlite3.connect("sql/villo.db")
	cursor = connection.cursor()
	cursor.execute("SELECT id,nom FROM Station")
	matches = cursor.fetchall()
	connection.close()
	return [(-1,"Station")]+matches

class StationSelectField(SelectField):
	def getStation(self):
		return Station(self.data)

class StationForm(Form):
	stations = StationSelectField("Station",choices=getStationList())



