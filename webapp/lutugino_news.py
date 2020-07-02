import requests
from bs4 import BeautifulSoup  
from datetime import datetime

from webapp.model import db, News

def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False

def get_lutugino_news():
    html = get_html('https://lutugino.su/news/')
    if html:   
        soup = BeautifulSoup(html, "html.parser")
        all_news = soup.findAll('div', class_="items-news-i")
        result_news = []
        for news in range(5):
            date = all_news[news].find('div', class_="date").find("span").text
            try:
                date = datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                date = datetime.now()     
            title = all_news[news].find('div', class_="text").find("a").text
            url = all_news[news].find('div', class_="text").find("a")["href"]
            text = all_news[news].find('div', class_="text").find("p").text[:-16]
            save_news(title, url, text, date)      
    return False

def save_news(title, url, text, date):
    news_exists = News.query.filter(News.url == url).count()
    if not news_exists:
        new_news = News(title=title, url=url, text=text, date=date)
        db.session.add(new_news)
        db.session.commit()