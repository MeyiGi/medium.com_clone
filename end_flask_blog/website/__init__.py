from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

month_name = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'May',
    6: 'Jun',
    7: 'Jul',
    8: 'Aug',
    9: 'Sep',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec'
}

db = SQLAlchemy()

def create_app():
	app = Flask(__name__)
	app.config["SECRET_KEY"] = "Samat.2004"
	app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
	db.init_app(app)
	migrate = Migrate(app, db)

	from .views import views
	from .error import error
	from .auth import auth

	app.register_blueprint(views, url_prefix="/")
	app.register_blueprint(error, url_prefix="/")
	app.register_blueprint(auth, url_prefix="/")

	from .models import User

	create_database(app=app)

	login_manager = LoginManager()
	login_manager.login_view = "auth.login"
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))

	return app

def create_database(app):
	with app.app_context():
		db.create_all()