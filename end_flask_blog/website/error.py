from flask import Blueprint

error = Blueprint("error", __name__)

@error.errorhandler(404)
def error404():
	return render_template("404.html")

@error.errorhandler(500)
def error500():
	return render_template("500.html")