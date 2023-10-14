from flask import Blueprint, flash, render_template, request, redirect, url_for
from .models import UserForm, User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from dns.resolver import resolve, NXDOMAIN
import re

auth = Blueprint("auth", __name__)

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
	form = UserForm()
	if request.method == "POST":
		username = form.username.data
		email = form.email.data
		password = form.password.data
		password1 = form.confirm_password.data

		email_exist = User.query.filter_by(email=email).first()
		username_exist = User.query.filter_by(username=username).first()

		if email_exist:
			flash("Email is already in use", category="error")
		elif username_exist:
			flash("Username is already in use", category="error")
		elif password != password1:
			flash("Passwords is not match", category="error")
		else:
			user = User(username=username, email=email, password=generate_password_hash(password, method="sha256"))
			db.session.add(user)
			db.session.commit()
			
			if "RemeberMe" in request.form:
				cheched_value = True
			else:
				cheched_value = False

			login_user(user, remember=cheched_value)
			flash("User created successfully", category="success")
			return redirect(url_for("views.home"))


	return render_template("sign_up.html", form=form, user=current_user)

@auth.route("/login", methods=["GET", "POST"])
def login():
	form = UserForm()
	if request.method == "POST":
		email = form.email.data
		password = form.password.data
		user = User.query.filter_by(email=email).first()

		if user:
			if check_password_hash(user.password, password):
				flash("Logged in!", category="success")
				
				if "RemeberMe" in request.form:
					cheched_value = True
				else:
					cheched_value = False

				login_user(user, remember=cheched_value)
				return redirect(url_for("views.home"))
			else:
				flash("Password is incorrect.", category="error")
		else:
			flash("Email doesn't exist.", category="error")
	return render_template("login.html", user=current_user, form=form)

@auth.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("views.home"))




def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def has_valid_mx_record(domain):
	try:
		answer = resolve(domain, "MX")
		return len(answer) > 0
	except NXDOMAIN:
		return False