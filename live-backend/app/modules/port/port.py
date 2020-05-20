import datetime
from app.modules.common.model import Model

from app import db


class Port(Model):
    __tablename__ = "port"

    port_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    type = db.Column(db.String)
    description = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())
