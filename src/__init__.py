from flask import Flask
from src.routes.routes import routes_blueprint
from src.models import db
from src.config import config_settings

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(config_settings['development'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(routes_blueprint)

    db.init_app(app)

    return app