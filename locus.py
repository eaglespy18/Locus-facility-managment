from database import CreateAllTables
CreateAllTables()
from flask import Flask, render_template, url_for, flash, redirect
from flask_bootstrap import Bootstrap
from form import SignUpForm, LoginForm, AdminForm, BookForm
import sqlite3
app = Flask(__name__)
app.config['SECRET_KEY'] = 'e'
Bootstrap(app)

CID=0
@app.route("/")
@app.route("/home")
def home():
	global CID
	CID=0
	return render_template('home.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
	form = SignUpForm()
	with sqlite3.connect('Locus.db')as db:
		c=db.cursor()
		check="SELECT * FROM Account"
		for row in c.execute(check):
			if row[0]==form.username.data:
				flash(f'Username is already taken','danger')
				return redirect(url_for('signup'))
	if form.validate_on_submit():
		with sqlite3.connect('Locus.db')as db:
			c=db.cursor()
			c.execute("INSERT INTO Client( ClientName, ClientPhoneNum, ClientEmail) VALUES (?,?,?)", (form.name.data, form.phoneNum.data, form.email.data))
			c.execute("SELECT ClientID FROM Client WHERE ClientName=? and ClientPhoneNum=? and ClientEmail=?", (form.name.data, form.phoneNum.data, form.email.data))
			CCID=c.fetchall()       
			c.execute("INSERT INTO Account( Username, Password, ClientID) VALUES (?,?,?)", (form.username.data, form.password.data, CCID[0][0]))
			flash(f'Account created. You can now login','success')
		return redirect(url_for('login'))
	if form.email.errors:
			for error in form.email.errors:
				flash(f'{error}', 'danger')
	if form.phoneNum.errors:
			for error in form.phoneNum.errors:
				flash(f'Invalid phone number.', 'danger')
	if form.password.errors:
			for error in form.password.errors:
				flash(f'Invalid password length. Password must be atleast 8 charcters long', 'danger')
	if form.confirmPassword.errors:
			for error in form.confirmPassword.errors:
				flash(f'Passwords do not match!', 'danger')
	return render_template('signup.html', form= form)

@app.route("/admin", methods=['GET', 'POST'])
def admin():
	form= AdminForm()
	if form.validate_on_submit():
		with sqlite3.connect('Locus.db')as db:
			c=db.cursor()
			check="SELECT * FROM AdminAccount"
			flag=False
			for row in c.execute(check):
				if row[0]==form.username.data and row[1]==form.password.data:
					flag=True
					flash(f'Login successful.','success')
					return adminpannel()
			if flag==False:
				flash(f'Invalid username or password.', 'danger')
				return redirect(url_for('admin'))
	return render_template('admin.html', form= form)

def adminpannel():
	with sqlite3.connect('Locus.db')as db:
		c=db.cursor()
		sql = "SELECT * FROM Booking"
		c.execute(sql)
		data=c.fetchall()
		sql="SELECT * FROM Client"
		c.execute(sql)
		info=c.fetchall()		
	return render_template('adminpannel.html',data=data, info=info)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form= LoginForm()
	if form.validate_on_submit():
		with sqlite3.connect('Locus.db')as db:
			c=db.cursor()
			check="SELECT * FROM Account"
			flag=False
			for row in c.execute(check):
				if row[0]==form.username.data and row[1]==form.password.data:
					global CID
					CID=int(row[2])
					flag=True
					flash(f'Login successful.','success')
					return userpannel()
			if flag==False:
				flash(f'Invalid username or password', 'danger')
				return redirect(url_for('login'))
	return render_template('login.html', form= form)

@app.route("/userpannel")
def userpannel():
	if CID!=0:
		return render_template('userpannel.html')
	else:
		return redirect(url_for('login'))


def rendirect(param):
	pass


@app.route("/mybookings")
def mybookings():
	if CID!=0:
		with sqlite3.connect('Locus.db')as db:
			c=db.cursor()
			sql = "SELECT FacilityID , Date FROM Booking WHERE ClientID={}".format(CID)
			c.execute(sql)
			data=c.fetchall()		
		return render_template('mybookings.html',data=data)
	else:
		return rendirect(url_for('home.html'))

@app.route("/9-aside(1)", methods=['GET', 'POST'])
def nineaside1():
	if CID!=0:
		form=BookForm()
		with sqlite3.connect('Locus.db')as db:
			c=db.cursor()
			check="SELECT * FROM Booking"
			for row in c.execute(check):
				if row[3]==str(form.date.data) and row[2]==1:
					flash(f'The facility is already booked for that date','danger')
					return redirect(url_for('nineaside1'))
		if form.validate_on_submit():
			with sqlite3.connect('Locus.db')as db:
				c=db.cursor()
				c.execute("INSERT INTO Booking(ClientID, FacilityID, Date) VALUES(?,?,?)", (CID, 1, form.date.data))
				global FID
				FID=1
				global BDate
				BDate=form.date.data
			return redirect(url_for('confirmation'))
		if form.date.errors:
			flash(f'Enter date in dd/mm/yy format', 'danger')
		return render_template('9-aside(1).html', form=form)
	else:
		return redirect(url_for('login'))

@app.route("/9-aside(2)", methods=['GET', 'POST'])
def nineaside2():
	if CID!=0:
		form=BookForm()
		with sqlite3.connect('Locus.db')as db:
			c=db.cursor()
			check="SELECT * FROM Booking"
			for row in c.execute(check):
				if row[3]==str(form.date.data) and row[2]==2:
					flash(f'The facility is already booked for that date','danger')
					return redirect(url_for('nineaside2'))
		if form.validate_on_submit():
			with sqlite3.connect('Locus.db')as db:
				c=db.cursor()
				c.execute("INSERT INTO Booking(ClientID, FacilityID, Date) VALUES(?,?,?)", (CID, 2, form.date.data))
				global FID
				FID=2
				global BDate
				BDate=form.date.data
			return redirect(url_for('confirmation'))
		if form.date.errors:
			flash(f'Enter date in dd/mm/yy format', 'danger')
		return render_template('9-aside(2).html', form=form)
	else:
		return redirect(url_for('login'))

@app.route("/7-aside(1)", methods=['GET', 'POST'])
def sevenaside1():
	if CID!=0:
		form=BookForm()
		with sqlite3.connect('Locus.db')as db:
			c=db.cursor()
			check="SELECT * FROM Booking"
			for row in c.execute(check):
				if row[3]==str(form.date.data) and row[2]==3:
					flash(f'The facility is already booked for that date','danger')
					return redirect(url_for('sevenaside1'))
		if form.validate_on_submit():
			with sqlite3.connect('Locus.db')as db:
				c=db.cursor()
				c.execute("INSERT INTO Booking(ClientID, FacilityID, Date) VALUES(?,?,?)", (CID, 3, form.date.data))
				global FID
				FID=3
				global BDate
				BDate=form.date.data
			return redirect(url_for('confirmation'))
		if form.date.errors:
			flash(f'Enter date in dd/mm/yy format', 'danger')
		return render_template('7-aside(1).html', form=form)
	else:
		return redirect(url_for('login'))

@app.route("/7-aside(2)", methods=['GET', 'POST'])
def sevenaside2():
	if CID!=0:
		form=BookForm()
		with sqlite3.connect('Locus.db')as db:
			c=db.cursor()
			check="SELECT * FROM Booking"
			for row in c.execute(check):
				if row[3]==str(form.date.data) and row[2]==4:
					flash(f'The facility is already booked for that date','danger')
					return redirect(url_for('sevenaside2'))
		if form.validate_on_submit():
			with sqlite3.connect('Locus.db')as db:
				c=db.cursor()
				c.execute("INSERT INTO Booking(ClientID, FacilityID, Date) VALUES(?,?,?)", (CID, 4, form.date.data))
				global FID
				FID=4
				global BDate
				BDate=form.date.data
			return redirect(url_for('confirmation'))
		if form.date.errors:
			flash(f'Enter date in dd/mm/yy format', 'danger')
		return render_template('7-aside(2).html', form=form)
	else:
		return redirect(url_for('login'))

@app.route("/11-aside", methods=['GET', 'POST'])
def elevenaside():
	if CID!=0:
		form=BookForm()
		with sqlite3.connect('Locus.db')as db:
			c=db.cursor()
			check="SELECT * FROM Booking"
			for row in c.execute(check):
				if row[3]==str(form.date.data) and row[2]==5:
					flash(f'The facility is already booked for that date','danger')
					return redirect(url_for('elevenaside'))
		if form.validate_on_submit():
			with sqlite3.connect('Locus.db')as db:
				c=db.cursor()
				c.execute("INSERT INTO Booking(ClientID, FacilityID, Date) VALUES(?,?,?)", (CID, 5, form.date.data))
				global FID
				FID=5
				global BDate
				BDate=form.date.data
			return redirect(url_for('confirmation'))
		if form.date.errors:
			flash(f'Enter date in dd/mm/yy format', 'danger')
		return render_template('11-aside.html', form=form)
	else:
		return redirect(url_for('login'))

@app.route("/5-aside", methods=['GET', 'POST'])
def fiveaside():
	if CID!=0:
		form=BookForm()
		with sqlite3.connect('Locus.db')as db:
			c=db.cursor()
			check="SELECT * FROM Booking"
			for row in c.execute(check):
				if row[3]==str(form.date.data) and row[2]==6:
					flash(f'The facility is already booked for that date','danger')
					return redirect(url_for('fiveaside'))
		if form.validate_on_submit():
			with sqlite3.connect('Locus.db')as db:
				c=db.cursor()
				c.execute("INSERT INTO Booking(ClientID, FacilityID, Date) VALUES(?,?,?)", (CID, 6, form.date.data))
				global FID
				FID=6
				global BDate
				BDate=form.date.data
			return redirect(url_for('confirmation'))
		if form.date.errors:
			flash(f'Enter date in dd/mm/yy format', 'danger')
		return render_template('5-aside.html', form=form)
	else:
		return redirect(url_for('login'))

@app.route("/rugby", methods=['GET', 'POST'])
def rugby():
	if CID!=0:
		form=BookForm()
		with sqlite3.connect('Locus.db')as db:
			c=db.cursor()
			check="SELECT * FROM Booking"
			for row in c.execute(check):
				if row[3]==str(form.date.data) and row[2]==7:
					flash(f'The facility is already booked for that date','danger')
					return redirect(url_for('rugby'))
		if form.validate_on_submit():
			with sqlite3.connect('Locus.db')as db:
				c=db.cursor()
				c.execute("INSERT INTO Booking(ClientID, FacilityID, Date) VALUES(?,?,?)", (CID, 7, form.date.data))
				global FID
				FID=7
				global BDate
				BDate=form.date.data
			return redirect(url_for('confirmation'))
		if form.date.errors:
			flash(f'Enter date in dd/mm/yy format', 'danger')
		return render_template('Rugby.html', form=form)
	else:
		return redirect(url_for('login'))

@app.route("/cricket", methods=['GET', 'POST'])
def cricket():
	if CID!=0:
		form=BookForm()
		with sqlite3.connect('Locus.db')as db:
			c=db.cursor()
			check="SELECT * FROM Booking"
			for row in c.execute(check):
				if row[3]==str(form.date.data) and row[2]==8:
					flash(f'The facility is already booked for that date','danger')
					return redirect(url_for('cricket'))
		if form.validate_on_submit():
			with sqlite3.connect('Locus.db')as db:
				c=db.cursor()
				c.execute("INSERT INTO Booking(ClientID, FacilityID, Date) VALUES(?,?,?)", (CID, 8, form.date.data))
				global FID
				FID=8
				global BDate
				BDate=form.date.data
			return redirect(url_for('confirmation'))
		if form.date.errors:
			flash(f'Enter date in dd/mm/yy format', 'danger')
		return render_template('cricket.html', form=form)
	else:
		return redirect(url_for('login'))

@app.route("/netball(1)", methods=['GET', 'POST'])
def netball1():
	if CID!=0:
		form=BookForm()
		with sqlite3.connect('Locus.db')as db:
			c=db.cursor()
			check="SELECT * FROM Booking"
			for row in c.execute(check):
				if row[3]==str(form.date.data) and row[2]==9:
					flash(f'The facility is already booked for that date','danger')
					return redirect(url_for('netball1'))
		if form.validate_on_submit():
			with sqlite3.connect('Locus.db')as db:
				c=db.cursor()
				c.execute("INSERT INTO Booking(ClientID, FacilityID, Date) VALUES(?,?,?)", (CID, 9, form.date.data))
				global FID
				FID=9
				global BDate
				BDate=form.date.data
			return redirect(url_for('confirmation'))
		if form.date.errors:
			flash(f'Enter date in dd/mm/yy format', 'danger')
		return render_template('netball(1).html', form=form)
	else:
		return redirect(url_for('login'))

@app.route("/netball(2)", methods=['GET', 'POST'])
def netball2():
	if CID!=0:
		form=BookForm()
		with sqlite3.connect('Locus.db')as db:
			c=db.cursor()
			check="SELECT * FROM Booking"
			for row in c.execute(check):
				if row[3]==str(form.date.data) and row[2]==10:
					flash(f'The facility is already booked for that date','danger')
					return redirect(url_for('netball2'))
		if form.validate_on_submit():
			with sqlite3.connect('Locus.db')as db:
				c=db.cursor()
				c.execute("INSERT INTO Booking(ClientID, FacilityID, Date) VALUES(?,?,?)", (CID, 10, form.date.data))
				global FID
				FID=10
				global BDate
				BDate=form.date.data
			return redirect(url_for('confirmation'))
		if form.date.errors:
			flash(f'Enter date in dd/mm/yy format', 'danger')
		return render_template('netball(2).html', form=form)
	else:
		return redirect(url_for('login'))

@app.route("/netball(3)", methods=['GET', 'POST'])
def netball3():
	if CID!=0:
		form=BookForm()
		with sqlite3.connect('Locus.db')as db:
			c=db.cursor()
			check="SELECT * FROM Booking"
			for row in c.execute(check):
				if row[3]==str(form.date.data) and row[2]==11:
					flash(f'The facility is already booked for that date','danger')
					return redirect(url_for('netball3'))
		if form.validate_on_submit():
			with sqlite3.connect('Locus.db')as db:
				c=db.cursor()
				c.execute("INSERT INTO Booking(ClientID, FacilityID, Date) VALUES(?,?,?)", (CID, 11, form.date.data))
				global FID
				FID=11
				global BDate
				BDate=form.date.data
			return redirect(url_for('confirmation'))
		if form.date.errors:
			flash(f'Enter date in dd/mm/yy format', 'danger')
		return render_template('netball(3).html', form=form)
	else:
		return redirect(url_for('login'))

@app.route("/netball(4)", methods=['GET', 'POST'])
def netball4():
	if CID!=0:
		form=BookForm()
		with sqlite3.connect('Locus.db')as db:
			c=db.cursor()
			check="SELECT * FROM Booking"
			for row in c.execute(check):
				if row[3]==str(form.date.data) and row[2]==12:
					flash(f'The facility is already booked for that date','danger')
					return redirect(url_for('netball4'))
		if form.validate_on_submit():
			with sqlite3.connect('Locus.db')as db:
				c=db.cursor()
				c.execute("INSERT INTO Booking(ClientID, FacilityID, Date) VALUES(?,?,?)", (CID, 12, form.date.data))
				global FID
				FID=12
				global BDate
				BDate=form.date.data
			return redirect(url_for('confirmation'))
		if form.date.errors:
			flash(f'Enter date in dd/mm/yy format', 'danger')
		return render_template('netball(4).html', form=form)
	else:
		return redirect(url_for('login'))

@app.route("/tennis(1)", methods=['GET', 'POST'])
def tennis1():
	if CID!=0:
		form=BookForm()
		with sqlite3.connect('Locus.db')as db:
			c=db.cursor()
			check="SELECT * FROM Booking"
			for row in c.execute(check):
				if row[3]==str(form.date.data) and row[2]==13:
					flash(f'The facility is already booked for that date','danger')
					return redirect(url_for('tennis1'))
		if form.validate_on_submit():
			with sqlite3.connect('Locus.db')as db:
				c=db.cursor()
				c.execute("INSERT INTO Booking(ClientID, FacilityID, Date) VALUES(?,?,?)", (CID, 13, form.date.data))
				global FID
				FID=13
				global BDate
				BDate=form.date.data
			return redirect(url_for('confirmation'))
		if form.date.errors:
			flash(f'Enter date in dd/mm/yy format', 'danger')
		return render_template('tennis(1).html', form=form)
	else:
		return redirect(url_for('login'))

@app.route("/tennis(2)", methods=['GET', 'POST'])
def tennis2():
	if CID!=0:
		form=BookForm()
		with sqlite3.connect('Locus.db')as db:
			c=db.cursor()
			check="SELECT * FROM Booking"
			for row in c.execute(check):
				if row[3]==str(form.date.data) and row[2]==14:
					flash(f'The facility is already booked for that date','danger')
					return redirect(url_for('tennis2'))
		if form.validate_on_submit():
			with sqlite3.connect('Locus.db')as db:
				c=db.cursor()
				c.execute("INSERT INTO Booking(ClientID, FacilityID, Date) VALUES(?,?,?)", (CID, 14, form.date.data))
				global FID
				FID=14
				global BDate
				BDate=form.date.data
			return redirect(url_for('confirmation'))
		if form.date.errors:
			flash(f'Enter date in dd/mm/yy format', 'danger')
		return render_template('tennis(2).html', form=form)
	else:
		return reditect(url_for('login'))

@app.route("/tennis(3)", methods=['GET', 'POST'])
def tennis3():
	if CID!=0:
		form=BookForm()
		with sqlite3.connect('Locus.db')as db:
			c=db.cursor()
			check="SELECT * FROM Booking"
			for row in c.execute(check):
				if row[3]==str(form.date.data) and row[2]==15:
					flash(f'The facility is already booked for that date','danger')
					return redirect(url_for('tennis3'))
		if form.validate_on_submit():
			with sqlite3.connect('Locus.db')as db:
				c=db.cursor()
				c.execute("INSERT INTO Booking(ClientID, FacilityID, Date) VALUES(?,?,?)", (CID, 15, form.date.data))
				global FID
				FID=15
				global BDate
				BDate=form.date.data
			return redirect(url_for('confirmation'))
		if form.date.errors:
			flash(f'Enter date in dd/mm/yy format', 'danger')
		return render_template('tennis(3).html', form=form)
	else:
		return redirect(url_for('login'))

@app.route("/tennis(4)", methods=['GET', 'POST'])
def tennis4():
	if CID!=0:
		form=BookForm()
		with sqlite3.connect('Locus.db')as db:
			c=db.cursor()
			check="SELECT * FROM Booking"
			for row in c.execute(check):
				if row[3]==str(form.date.data) and row[2]==16:
					flash(f'The facility is already booked for that date','danger')
					return redirect(url_for('tennis4'))
		if form.validate_on_submit():
			with sqlite3.connect('Locus.db')as db:
				c=db.cursor()
				c.execute("INSERT INTO Booking(ClientID, FacilityID, Date) VALUES(?,?,?)", (CID, 16, form.date.data))
				global FID
				FID=16
				global BDate
				BDate=form.date.data
			return redirect(url_for('confirmation'))
		if form.date.errors:
			flash(f'Enter date in dd/mm/yy format', 'danger')
		return render_template('tennis(4).html', form=form)
	else:
		return redirect(url_for('login'))

@app.route("/confirmation")
def confirmation():
	if CID!=0:
		with sqlite3.connect('Locus.db')as db:
			c=db.cursor()
			sql = "SELECT FacilityName , FacilityDescription FROM Facility WHERE FacilityID={}".format(FID)
			c.execute(sql)
			info=c.fetchall()
			title=info[0][0]
			des=info[0][1]
		return render_template('confirmation.html',title=title, date=BDate, des=des)
	else:
		return redirect(url_for('login'))

if __name__ == "__main__":
	app.run(debug=True)


