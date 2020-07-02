from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)

def __repr__(self):
    return '<News {} {}>'.format(self.title, self,url)