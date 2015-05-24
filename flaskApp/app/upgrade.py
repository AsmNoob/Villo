# -*- coding: utf8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, validators
from wtforms.validators import ValidationError
import sqlite3
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

def alphaValidation(form,field):
	if len(field.errors)<1:
		if not field.data.isalpha():
			raise ValidationError("The field {0} must consists of numeric characters only.".format(field.name))

def numericValidation(form,field):
	if len(field.errors)<1:
		if not field.data.isnumeric():
			raise ValidationError("The field {0} must consists of numeric characters only.".format(field.name))

class UpgradeForm(Form):
	name = TextField(u'Nom', [notEmptyValidation,sizeValidation(min=minSize, max=maxSize),alphaValidation])
	firstName = TextField(u'Prénom', [notEmptyValidation,sizeValidation(min=minSize, max=maxSize),alphaValidation])
	phone = TextField(u'Téléphone', [notEmptyValidation,sizeValidation(min=7, max=maxSize),numericValidation])
	street = TextField(u'Rue', [notEmptyValidation,sizeValidation(min=minSize, max=maxSize),alphaValidation])
	number = TextField(u'Numéro', [notEmptyValidation,sizeValidation(min=0, max=maxSize),numericValidation])
	postal = TextField(u'Code postal', [notEmptyValidation,sizeValidation(min=minSize, max=maxSize),numericValidation])
	city = TextField(u'Ville', [notEmptyValidation,sizeValidation(min=minSize, max=maxSize),alphaValidation])

def dateFromString(string):
	s = string.split('T')
	d = s[0].split('-')
	t = s[1].split(':')
	return datetime(int(d[0]),int(d[1]),int(d[2]),int(t[0]),int(t[1]),int(t[2]))

class UpgradeManager():
	def manage(self, form, uid):
		self.connection = sqlite3.connect("sql/villo.db")
		self.cursor = self.connection.cursor()
		currDate = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
		self.cursor.execute("SELECT dateFinValidite FROM Utilisateur WHERE id={0}".format(uid))
		oldExpiricy = dateFromString(self.cursor.fetchone()[0])

		self.expiricy = (oldExpiricy+timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%S")
		rfid = randint(1000000000000000,10000000000000000)
		self.cursor.execute("SELECT * FROM Abonne WHERE rfid={0}".format(rfid))
		while (len(self.cursor.fetchall())>0):
			rdif = randint(1000000000000000,10000000000000000)
			self.cursor.execute("SELECT * FROM Abonne WHERE rfid={0}".format(rfid))

		self.cursor.execute('UPDATE Utilisateur SET dateFinValidite="{0}" WHERE id={1}'.format(self.expiricy,uid))
		self.cursor.execute('INSERT INTO Abonne VALUES ({0},"{1}","{2}","{3}","{4}",{5},"{6}",{7},"{8}",{9})'.format(	rfid,
																														form.name.data,
																														form.firstName.data,
																														form.phone.data,
																														form.city.data,
																														form.postal.data,
																														form.street.data,
																														form.number.data,
																														currDate,
																														uid))
		self.connection.commit()
		self.connection.close()