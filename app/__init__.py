from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .confs import Core

db = SQLAlchemy()

def create_app():
	print("Creating App")
	#app = Flask(__name__ , static_folder = "../apex/pictures")
	app = Flask(__name__ , static_folder="static")
	app.config.from_object(Core)
	db.init_app(app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app