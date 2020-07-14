from flask import Blueprint, current_app, render_template

from webapp.news.models import News
from webapp.weather import weather_by_city

blueprint = Blueprint("news", __name__)

@blueprint.route('/')
def index():
    title = "Новости Лутугино"
    weather = weather_by_city(current_app.config["WEATHER_DEFAULT_CITY"])
    news_list = News.query.order_by(News.date.desc()).all()
    return render_template("news/index.html", page_title=title, weather = weather, news_list=news_list)