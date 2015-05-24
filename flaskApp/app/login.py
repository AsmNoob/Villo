from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, HiddenField, validators
from wtforms.validators import ValidationError
import sqlite3

minSize = 1
maxSize = 25
passSize = 4

def matchValidation(form,field):
	if (len(form.uid.errors)<1 and len(form.password.errors)<1):
		connection = sqlite3.connect("sql/villo.db")
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM Utilisateur WHERE id={0} AND motDePasse={1}".format(form.uid.data,form.password.data))
		matches = cursor.fetchall()
		connection.close()
		if (len(matches)!=1):
			raise ValidationError("No user with this password found. There may be a mistake in the id or the password.")

def idValidation(form,field):
	if not field.data.isnumeric():
		raise ValidationError("The id is a number.")

def passValidation(form,field):
	if not field.data.isnumeric():
		raise ValidationError("The password is a 4 digit number.")
	if len(field.data)!=passSize:
		raise ValidationError("The password is a 4 digit number.")

class LoginForm(Form):
	uid = TextField('Identifiant', [idValidation])
	password = PasswordField('Password',[passValidation])
	hidden = HiddenField('',[matchValidation])