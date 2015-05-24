from wtforms import SelectField
from datetime import datetime
import sqlite3	

class Station(object):
	def __init__(self,id):
		self.id = id

	def getAvailableVillos(self):
		connection = sqlite3.connect("sql/villo.db")
		cursor = connection.cursor()
		cursor.execute('SELECT COUNT(*) FROM (SELECT * FROM Deplacement GROUP BY velo HAVING MAX(heureArrivee)=heureArrivee AND stationArrivee<>"None" AND velo IN (SELECT id FROM Velo WHERE etat="True") ) GROUP BY stationArrivee HAVING stationArrivee={0}'.format(self.id))
		try:
			match = cursor.fetchone()[0]
		except TypeError:
			match = 0
		connection.close()
		return match

	def getFreeSpots(self):
		connection = sqlite3.connect("sql/villo.db")
		cursor = connection.cursor()
		cursor.execute('SELECT (SELECT capacite FROM Station WHERE id={0})-COUNT(*) FROM (SELECT * FROM Deplacement GROUP BY velo HAVING MAX(heureArrivee)=heureArrivee AND stationArrivee<>"None") GROUP BY stationArrivee HAVING stationArrivee={0}'.format(self.id))
		match = cursor.fetchone()[0]
		connection.close()
		return match

	def getCapacity(self):
		connection = sqlite3.connect("sql/villo.db")
		cursor = connection.cursor()
		cursor.execute('SELECT capacite FROM Station WHERE id={0}'.format(self.id))
		match = cursor.fetchone()[0]
		connection.close()
		return match

	def getVilloOptions(self):
		matches = []
		if self.id!="None":
			connection = sqlite3.connect("sql/villo.db")
			cursor = connection.cursor()
			cursor.execute('SELECT velo FROM (SELECT * FROM Deplacement GROUP BY velo HAVING MAX(heureArrivee)=heureArrivee AND stationArrivee<>"None" AND velo IN (SELECT id FROM Velo WHERE etat="True") ) WHERE stationArrivee={0}'.format(self.id))
			matches = cursor.fetchall()
			matches = [(matches[i][0],i+1) for i in range(len(matches))]
			connection.close()
		return [(-1,"Villo")]+matches

	def rentVillo(self, veloId, userId):
		if  self.id!="None" and veloId!="-1":
			currDate = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
			connection = sqlite3.connect("sql/villo.db")
			cursor = connection.cursor()
			cursor.execute('INSERT INTO Deplacement VALUES ({0},{1},{2},"{3}","{4}","{4}")'.format(veloId, userId, self.id, currDate, "None"))
			connection.commit()
			connection.close()

	def stopRent(self,userId):
		if self.id!="None":
			currDate = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
			connection = sqlite3.connect("sql/villo.db")
			cursor = connection.cursor()
			cursor.execute('UPDATE Deplacement SET stationArrivee={0}, heureArrivee="{1}" WHERE utilisateur={2} AND stationArrivee="None" '.format(self.id, currDate, userId))
			connection.commit()
			connection.close()

	def brokenBike(self,bid):
		if bid!="None":
			print("psspar ici",bid)
			connection = sqlite3.connect("sql/villo.db")
			cursor = connection.cursor()
			cursor.execute('UPDATE Velo SET etat="False" WHERE id={0} '.format(bid))
			connection.commit()
			connection.close()

		