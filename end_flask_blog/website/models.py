from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, equal_to
from . import db
from datetime import datetime
from flask_login import UserMixin

class UserForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	email = EmailField("Email", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	confirm_password = PasswordField("Confirm_password", validators=[DataRequired()])
	submit = SubmitField("Submit")

class PostForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired()])
	text = TextAreaField("Text", validators=[DataRequired()])
	submit = SubmitField("Post")

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(120), nullable=False, unique=True)
	password = db.Column(db.String(128), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	profile_pic = db.Column(db.String(), nullable=True)

	posts = db.relationship("Post", backref="user", passive_deletes=True)
	comments = db.relationship("Comment", backref="user", passive_deletes=True)
	likes = db.relationship("Like", backref="user", passive_deletes=True)


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(256), nullable=False)
	text = db.Column(db.Text, nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

	comments = db.relationship("Comment", backref="post", passive_deletes=True)
	likes = db.relationship("Like", backref="post", passive_deletes=True)

class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(200), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
	post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)

class Like(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
	post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)