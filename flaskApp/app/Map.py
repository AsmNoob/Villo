import sqlite3
from Station import Station

class Map(object):

	def getAllStationsPos(self):
		connection = sqlite3.connect("sql/villo.db")
		cursor = connection.cursor()
		cursor.execute('SELECT id,nom,xCoords,yCoords,bornePayement FROM Station')
		matches = cursor.fetchall()
		connection.close()
		return matches
	
	def getStation(self,id):
		return Station(id)