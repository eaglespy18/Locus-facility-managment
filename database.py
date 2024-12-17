import sqlite3

d=sqlite3.connect('Locus.db')
c=d.cursor()

def CreateAllTables():
	with sqlite3.connect('Locus.db')as db:
		c=db.cursor()
		c.execute("CREATE TABLE IF NOT EXISTS Client(ClientID INTEGER PRIMARY KEY, ClientName TEXT, ClientPhoneNum TEXT, ClientEmail TEXT)")
		c.execute("CREATE TABLE IF NOT EXISTS Account(Username TEXT PRIMARY KEY, Password TEXT, ClientID INTEGER)")
		c.execute("CREATE TABLE IF NOT EXISTS Booking(BookingID INTEGER PRIMARY KEY , ClientID INTEGER, FacilityID INTEGER, Date TEXT)")
		c.execute("CREATE TABLE IF NOT EXISTS Facility(FacilityID INTEGER PRIMARY KEY, FacilityName TEXT, FacilityDescription TEXT)")
		c.execute("CREATE TABLE IF NOT EXISTS AdminAccount(Username TEXT PRIMARY KEY, Password TEXT)")
		
