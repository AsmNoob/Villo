from flask.ext.login import UserMixin
from datetime import datetime
import sqlite3 

def dateFromString(string):
	s = string.split('T')
	d = s[0].split('-')
	t = s[1].split(':')
	return datetime(int(d[0]),int(d[1]),int(d[2]),int(t[0]),int(t[1]),int(t[2]))

class User(UserMixin):
	users = {}
	def __init__(self,id):
		self.id = id
		self.authenticated = (id in User.users)
		if (self.authenticated):
			connection = sqlite3.connect("sql/villo.db")
			cursor = connection.cursor()

			cursor.execute('SELECT dateFinValidite FROM Utilisateur WHERE id={0}'.format(id))
			self.validityDate = cursor.fetchone()[0]

			cursor.execute('SELECT nom,prenom,telephone,ville,codePostal,rue,numero,dateSouscription FROM Abonne WHERE utilisateur={0}'.format(id))
			matches = cursor.fetchall()
			self.isAbonne=(len(matches)==1)
			if self.isAbonne:
				self.name,self.firstName,self.phone,self.city,self.postal,self.street,self.number,self.subscribeDate = matches[0]

			connection.close()
	
	@classmethod
	def login(cls,aUser):
		cls.users[aUser.get_id()] = aUser
		aUser.authenticated = True

	def hasVillo(self):
		connection = sqlite3.connect("sql/villo.db")
		cursor = connection.cursor()
		cursor.execute('SELECT * FROM Deplacement WHERE utilisateur={0} AND stationArrivee="None"'.format(self.id))
		matches = cursor.fetchall()
		connection.close()
		return len(matches)>0

	def getMoves(self):
		connection = sqlite3.connect("sql/villo.db")
		cursor = connection.cursor()
		cursor.execute('SELECT heureDepart,St1.nom,heureArrivee,St2.nom FROM Deplacement JOIN Station St1 ON stationDepart=St1.id JOIN Station St2 ON stationArrivee=St2.id  WHERE utilisateur={0} ORDER BY heureDepart'.format(self.id))
		matches = cursor.fetchall()
		connection.close()
		return matches

	def isStillValid(self):
		return dateFromString(self.validityDate)>datetime.now()

	def is_active(self):
		"""True, as all users are active."""
		return True

	def get_id(self):
		"""Return the email address to satisfy Flask-Login's requirements."""
		return self.id

	def is_authenticated(self):
		"""Return True if the user is authenticated."""
		return self.authenticated

	def is_anonymous(self):
		"""False, as anonymous users aren't supported."""
		return False