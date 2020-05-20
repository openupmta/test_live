import datetime
from app import db
from app.modules.common.model import Model


class Region(Model):
    __tablename__ = 'region'

    region_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    acronym = db.Column(db.String)
    description = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())
