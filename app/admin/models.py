from app import db
from app import signals
import enum

class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(120), unique=False, nullable=False)
    priority = db.Column(db.Integer, unique=True, nullable=False)

    def __init__(self, name=None, image=None, priority=None):
        self.name = name
        self.image = image
        self.priority = priority

    def __repr__(self):
        return '<Level %r>' % self.name
