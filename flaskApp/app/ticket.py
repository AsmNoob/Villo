# -*- coding: utf8 -*-

import sqlite3
from flask.ext.wtf import Form
from wtforms import TextField, RadioField
from wtforms import TextField, validators
from wtforms.validators import ValidationError
from random import randint
from datetime import datetime,timedelta

minSize = 3
maxSize = 25

def notEmptyValidation(form,field):
	if len(field.data)<1:
		raise ValidationError("The field {0} cannot be empty.".format(field.name))

class sizeValidation(object):
	def __init__(self, min=-1, max=-1):
		self.min = min
		self.max = max
	def __call__(self,form,field):
		if len(field.errors)<1:
			if not (self.min <= len(field.data) <= self.max):
				raise ValidationError("Field {0} must be between {1} and {2} characters long.".format(field.name,self.min,self.max))

def numericValidation(form,field):
	if len(field.errors)<1:
		if not field.data.isnumeric():
			raise ValidationError("The field {0} must consists of numeric characters only.".format(field.name))

class TmpUserForm(Form):
	price = RadioField(0, choices=[(0, u"1 jour - 1,50€"),(1, u"7 jours - 7,00€")],coerce=int)
	bank = TextField(u"Données Bancaires", [notEmptyValidation,sizeValidation(min=minSize, max=maxSize),numericValidation])

class TmpUserManager(object):
	def manage(self, form):
		self.connection = sqlite3.connect("sql/villo.db")
		self.cursor = self.connection.cursor()
		self.cursor.execute("SELECT MAX(id) FROM Utilisateur")
		self.newId = int(self.cursor.fetchone()[0])+1
		self.password = str(randint(1000,10000))
		currDate = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
		self.expiricy = (datetime.now()+timedelta(days=( 1 if form.price.data==0 else 7))).strftime("%Y-%m-%dT%H:%M:%S")
		self.cursor.execute('INSERT INTO Utilisateur VALUES ({0},{1},{2},"{3}")'.format(self.newId,self.password,form.bank.data,self.expiricy))
		self.connection.commit()
		self.connection.close()