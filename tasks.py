from celery import Celery
from celery.schedules import crontab

from webapp import create_app
from webapp.news.parsers import autonews

flask_app = create_app()
celery_app = Celery("tasks", broker="redis://localhost:6379/0")

@celery_app.task
def autonews_snippets():
    with flask_app.app_context():
        autonews.get_news_snippets()

@celery_app.task
def autonews_content():
    with flask_app.app_context():
        autonews.get_news_content()

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute="*/1"), autonews_snippets.s())
    sender.add_periodic_task(crontab(minute="*/1"), autonews_content.s())

#celery -A tasks worker --loglevel=info
#celery -A tasks worker -B --loglevel=info
#celery -A tasks beat