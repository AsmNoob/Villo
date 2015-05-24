# -*- coding: utf8 -*-

from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, login_required, LoginManager, current_user, logout_user
from app import app
from app.register import RegistrationForm, RegisterManager
from app.villoviewer import StationForm
from app.login import LoginForm
from app.User import User
from app.Map import Map
from app.Station import Station
from app.ticket import TmpUserForm, TmpUserManager
from app.upgrade import UpgradeForm, UpgradeManager

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(user_id):
	if (user_id in User.users):
		return User.users[user_id]

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.get_id() in User.users:
		return redirect(url_for("index"))
	form = RegistrationForm(request.form)
	if (request.method=='POST') and form.validate():
		r = RegisterManager()
		r.manage(form)
		flash("Merci d'utiliser le service Villo.")
		flash("La somme de 30€ vient d'être retirée de votre compte.")
		flash("Votre identifiant est le {2} et mot de passe est le {0}. Votre abonnement prendra fin le {1}.".format(r.password,r.expiricy.replace('T',' à '),r.newId))
		flash("Votre carte va être envoyée à l'adresse que vous avez donné.")
		return redirect(url_for('index'))
	return render_template('register.html', form=form, user=User(current_user.get_id()), map=Map())

@app.route('/upgrade', methods=['GET', 'POST'])
def upgrade():
	uid=current_user.get_id()
	if uid not in User.users or (uid in User.users and User(uid).isAbonne) :
		return redirect(url_for("index"))
	form = UpgradeForm(request.form)
	if (request.method=='POST') and form.validate():
		r = UpgradeManager()
		r.manage(form,uid)
		flash("Merci d'utiliser le service Villo.")
		flash("La somme de 30€ vient d'être retirée de votre compte.")
		flash("Votre identifiant reste le même ainsi que votre mot de passe. Votre abonnement prendra fin le {0}.".format(r.expiricy.replace('T',' à ')))
		flash("Votre carte va être envoyée à l'adresse que vous avez donné.")
		return redirect(url_for('index'))
	return render_template('upgrade.html', form=form, user=User(current_user.get_id()), map=Map())


@app.route('/ticket', methods=['GET', 'POST'])
def ticket():
	form = TmpUserForm(request.form)
	if (request.method=='POST') and form.validate():
		r = TmpUserManager()
		r.manage(form)
		flash("Merci d'utiliser le service Villo.")
		flash("La somme de {0}€ vient d'être retirée de votre compte.".format("1,50" if form.price.data==0 else "7,00"))
		flash("Votre identifiant est le {2} et mot de passe est le {0}. La validité de la carte prendra fin le {1}.".format(r.password,r.expiricy.replace('T',' à '),r.newId))
		return redirect(url_for('index'))
	print(form.errors)
	return render_template("ticket.html", form=form, user=User(current_user.get_id()), map=Map())

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
	form = StationForm(request.form)
	return render_template('index.html',form=form, user=User(current_user.get_id()), map=Map())

@app.route('/logout', methods=['GET', 'POST'])
def logout():
	if current_user.get_id() in User.users:
		del User.users[current_user.get_id()]
		logout_user()
		return redirect(url_for("index"))
	else:
		return redirect(url_for("login"))

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.get_id() in User.users:
		return redirect(url_for("index"))
	form = LoginForm(request.form)
	if (request.method=='POST') and (form.validate()):
		u = User(form.uid.data)
		User.login(u)
		login_user(u,remember=True)
		return redirect(url_for("index"))
	else:
		return render_template("login.html", form=form, user=User(current_user.get_id()), map=Map())

@app.route('/history', methods=['GET', 'POST'])
def history():
	if current_user.get_id() not in User.users:
		return redirect(url_for("index"))
	return render_template("history.html", user=User(current_user.get_id()), map=Map())

@app.route('/_get_station_info', methods=['GET', 'POST'])
def getStationInfo():
	id = request.args.get("id")
	return render_template("station.html", station=Station(id), user=User(current_user.get_id()))

@app.route('/_rent_villo', methods=['GET', 'POST'])
def rentVillo():
	user = User(current_user.get_id())
	if not user.is_authenticated():
		return ''
	sid = request.args.get("id1")
	vid = request.args.get("id2")
	station = Station(sid)
	station.rentVillo(vid,user.id)
	return render_template("station.html", station=station, user=user)

@app.route('/_stop_rent', methods=['GET', 'POST'])
def stopRent():
	user = User(current_user.get_id())
	if not user.is_authenticated():
		return ''
	sid = request.args.get("id")
	station = Station(sid)
	station.stopRent(user.id)
	return render_template("station.html", station=station, user=user)

@app.route('/_broken_bike', methods=['GET', 'POST'])
def brokenBike():
	user = User(current_user.get_id())
	if not user.is_authenticated():
		return ''
	sid = request.args.get("id1")
	bid = request.args.get("id2")
	station = Station(sid)
	station.brokenBike(bid)
	return render_template("station.html", station=station, user=user)
