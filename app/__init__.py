from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .views import views
from os import environ



db = SQLAlchemy()

DB_NAME = "database.db"


class Config:
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL") or \
        "postgres://yukysjqchtlbep:b4938b192835e830a8c7a62e6500e1e822ac354dae5c955da9c89f3618e0ced1@ec2-44-194-4-127.compute-1.amazonaws.com:5432/ddfnl258civ99s"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

def create_app():
    app = Flask(__name__)

    migrate = Migrate(app, db)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = "iisHcMFopS6ldoeo"

    db.init_app(app)
    migrate.init_app(app, db)

    from .auth import auth

    app.register_blueprint(views, url_prefix=('/'))
    app.register_blueprint(auth, url_prefix=('/'))

    from .models import User


    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app



app = create_app()

if __name__ == "__main__":

    app.run(debug=True)
