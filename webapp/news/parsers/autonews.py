from datetime import datetime
import locale
import platform

from bs4 import BeautifulSoup

from webapp import db
from webapp.news.models import News
from webapp.news.parsers.utils import get_html, save_news

if platform.system() == "Windows":
    locale.setlocale(locale.LC_ALL, "russian")
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8' )

def parse_autonews_date(date_str):
    dates = {
        "января" : "январь",
        "февраля" : "февраль",
        "марта" : "март",
        "апреля" : "апрель",
        "мая" : "май",
        "июня" : "июнь",
        "июля" : "июль",
        "августа" : "август",
        "сентября" : "сентябрь",
        "октября" : "октябрь",
        "ноября" : "ноябрь",
        "декабря" : "декабрь",
    }
    date_str = date_str.lower()
    for month in dates.keys():
        if month in date_str:
            date_str = date_str.replace(month, dates.get(month))
    
    try: 
        date_str = datetime.strptime(date_str, "%d %B %Y")
        return date_str
    except(ValueError):
        try:
            curr_date = datetime.now()
            curr_year = datetime.strftime(curr_date, " %Y")
            date_str += curr_year
            date_str = datetime.strptime(date_str, "%d %B %Y")
            return date_str
        except(ValueError):
            return datetime.now()

def get_news_snippets():
    html = get_html('https://www.autonews.ru/tags/?tag=%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B8')
    if html:   
        soup = BeautifulSoup(html, "html.parser")
        all_news = soup.find("div", class_="tag-news__container").findAll('div', class_="item-big")
        for news in all_news:
            url = news.find("a", class_="item-big__link")["href"]
            title = news.find('span', class_="item-big__title").text
            date = news.find("span", class_="item-big__date").text
            date = parse_autonews_date(date)
            save_news(title, url, date)
   
    return False    

def get_news_content():
    news_without_text = News.query.filter(News.text.is_(None))
    for news in news_without_text:
        html = get_html(news.url)
        if html:
            soup = BeautifulSoup(html, "html.parser")
            news_text = soup.find("div", class_="article__text").decode_contents()
            if news_text:   
                news.text = news_text
                db.session.add(news)
                db.session.commit()
    