from flask_bcrypt import Bcrypt
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager
)
from flask_talisman import Talisman

csp = {
    'default-src': '\'self\'',
    'script-src': ['\'unsafe-inline\'', '\'unsafe-eval\'', 'https://cdn.plot.ly/plotly-latest.min.js'],
    'img-src': ['\'unsafe-inline\'', '*'], 
    'style-src': ['\'unsafe-inline\'', 'stackpath.bootstrapcdn.com'],
    'script-src-elem': ['\'unsafe-inline\'', '*']
}

db = MongoEngine()
login_manager = LoginManager()
login_manager.login_view = "login"
bcrypt = Bcrypt()

from .posts.routes import posts
from .users.routes import users

def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(posts)
    app.register_blueprint(users)

    login_manager.login_view = "users.login"

    Talisman(app, content_security_policy=csp)

    return app