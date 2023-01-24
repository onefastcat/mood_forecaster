from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .views import views






db = SQLAlchemy()



DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)

    migrate = Migrate(app, db)
    app.config['SECRET_KEY'] = "iisHcMFopS6ldoeo"
    #check where to put this
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
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


    #make sure I need this. maybe it is not useful for me
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
