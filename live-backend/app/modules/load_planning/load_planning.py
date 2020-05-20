from app.app import db, flask_bcrypt
import datetime
import jwt

from app.settings.config import key
from ..common.model import Model


class LoadPlanning(Model):
    __tablename__ = "load_planning"

    load_planning_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    port_load_id = db.Column(db.Integer)
    port_load_name = db.Column(db.String)
    # port_load = db.relationship('Port', backref=db.backref('load_plannings', lazy=True))

    port_discharge_id = db.Column(db.Integer)
    port_discharge_name = db.Column(db.String)
    # port_discharge = db.relationship('Port', backref=db.backref('load_plannings', lazy=True))

    vessel_id = db.Column(db.Integer)
    vessel_name = db.Column(db.String)
    # vessel = db.relationship('Vessel', backref=db.backref('load_plannings', lazy=True))

    region_id = db.Column(db.Integer)
    region_name = db.Column(db.String)
    # region = db.relationship('Region', backref=db.backref('load_plannings', lazy=True))

    ETS_text = db.Column(db.String)
    ETS = db.Column(db.Date)

    date_planned_text = db.Column(db.String)
    date_planned = db.Column(db.Date)
    date_transit_text = db.Column(db.String)
    date_transit = db.Column(db.Date)

    voyage = db.Column(db.String)
    load_type = db.Column(db.String)

    ETA_text = db.Column(db.String)
    ETA = db.Column(db.Date)
    volume = db.Column(db.Integer)

    date_created = db.Column(db.DateTime, default=datetime.datetime.now())
    hash_value = db.Column(db.String)
