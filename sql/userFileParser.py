#!/usr/bin/python
import sys
from xml.dom import minidom
import sqlite3

class UserFileParser(object):
	"""Parse the xml user file for Villo application"""
	def __init__(self,fileName, dbName):
		super(UserFileParser, self).__init__()
		self.doc = minidom.parse(fileName)
		self.connection = sqlite3.connect(dbName)
		self.cursor = self.connection.cursor()

	def content(self,node,tag):
		return node.getElementsByTagName(tag)[0].childNodes[0].nodeValue

	def parseUser(self,userNode):
		userId = int(self.content(userNode,"userID"))
		password = int(self.content(userNode,"password"))
		card = int(self.content(userNode,"card"))
		expiryDate =  self.content(userNode,"expiryDate")
		self.cursor.execute('INSERT INTO Utilisateur VALUES ({0},{1},{2},"{3}")'.format(userId,password,card,expiryDate))
		return userId

	def parseAbonne(self,userNode,userId):
		rfid = int(self.content(userNode,"RFID"))
		lastName = self.content(userNode,"lastname")
		firstName = self.content(userNode,"firstname")
		phone = self.content(userNode,"phone")
		city = self.content(userNode,"city")
		cp = int(self.content(userNode,"cp"))
		street = self.content(userNode,"street")
		number = int(self.content(userNode,"number"))
		subscribeDate = self.content(userNode,"subscribeDate")
		self.cursor.execute('INSERT INTO Abonne VALUES ({0},"{1}","{2}","{3}","{4}",{5},"{6}",{7},"{8}",{9})'.format(rfid,lastName,firstName,phone,city,cp,street,number,subscribeDate,userId))

	def parse(self):
		subscribrersNodes = self.doc.getElementsByTagName("subscribers")
		for subscribersNode in subscribrersNodes:
			userNodes = subscribersNode.getElementsByTagName("user")
			for userNode in userNodes:
				userId = self.parseUser(userNode)
				self.parseAbonne(userNode,userId)

		tmpUsersNodes = self.doc.getElementsByTagName("temporaryUsers")
		for tmpUsersNode in tmpUsersNodes:
			userNodes = tmpUsersNode.getElementsByTagName("user")
			for userNode in userNodes:
				self.parseUser(userNode)

	def applyChange(self):
		self.connection.commit()
		self.connection.close()

def main():
	if (len(sys.argv)==3):
		P = UserFileParser(sys.argv[1],sys.argv[2])
		P.parse()
		P.applyChange()
	else :
		raise ValueError("Bad argument given to the program, must be a xml file name and a sqlite database file name.")

if __name__=="__main__":
	main()