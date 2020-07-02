from webapp import create_app
from webapp.lutugino_news import get_lutugino_news

app = create_app()
with app.app_context():
    get_lutugino_news()