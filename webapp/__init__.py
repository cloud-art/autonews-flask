from flask import Flask, flash, render_template, redirect, url_for
from flask_login import LoginManager, current_user, login_required

from webapp.db import db
from webapp.admin.views import blueprint as admin_blueprint
from webapp.news.models import News
from webapp.news.views import blueprint as news_blueprint
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint
from webapp.weather import weather_by_city

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.login" #название функции с логином

    app.register_blueprint(admin_blueprint)
    app.register_blueprint(news_blueprint)
    app.register_blueprint(user_blueprint)
   
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app