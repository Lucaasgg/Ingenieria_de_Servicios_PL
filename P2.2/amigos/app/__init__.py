from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import app_config
from flask import render_template

db = SQLAlchemy()

def create_app(config_name):
    #App es instancia de Flask
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    from .html import html as html_blueprint
    app.register_blueprint(html_blueprint, url_prefix='/html')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
