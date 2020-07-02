from flask import Flask, render_template

from webapp.model import db, News
from webapp.lutugino_news import get_lutugino_news
from webapp.weather import weather_by_city

# set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        title = "Новости Лутугино"
        weather = weather_by_city(app.config["WEATHER_DEFAULT_CITY"])
        news_list = News.query.order_by(News.date.desc()).all()
        return render_template("index.html", page_title=title, weather = weather, news_list=news_list)
    
    return app