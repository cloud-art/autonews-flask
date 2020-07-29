import requests

from webapp.db import db
from webapp.news.models import News

def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Mobile Safari/537.36"
    }
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False

def save_news(title, url, date):
    news_exists = News.query.filter(News.url == url).count()
    if not news_exists:
        new_news = News(title=title, url=url, date=date)
        db.session.add(new_news)
        db.session.commit()
