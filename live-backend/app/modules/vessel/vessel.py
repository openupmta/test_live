import datetime
from app.app import db, flask_bcrypt
import datetime

from ..common.model import Model


class Vessel(Model):
    __tablename__ = 'vessel'

    vessel_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    acronym = db.Column(db.String)
    description = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())
