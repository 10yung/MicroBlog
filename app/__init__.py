from flask import Flask
from flask_bootstrap import Bootstrap
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()

login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Bind flask extension
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)


    # Load config and initialize flask app
    # import main routes to context
    from .routes.main import main as main_routes_blueprint
    from .routes.auth import auth as auth_routes_blueprint
    app.register_blueprint(main_routes_blueprint)
    app.register_blueprint(auth_routes_blueprint)

    return app
