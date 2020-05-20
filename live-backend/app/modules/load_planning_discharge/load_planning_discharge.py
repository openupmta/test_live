from app import db
from app.modules.common.model import Model


class LoadPlanningDischarge(Model):
    __tablename__ = 'load_planning_discharge'

    load_planning_discharge_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    load_planning_id = db.Column(db.Integer, nullable=False)
    # load_planning = db.relationship('Load_Planning', backref=db.backref('load_planning_discharges', lazy=True))

    region_id = db.Column(db.Integer, nullable=False)
    region_name = db.Column(db.String)
    # region = db.relationship('Region', backref=db.backref('load_planning_discharges', lazy=True))

    port_discharge_id = db.Column(db.Integer, nullable=False)
    # port_discharge = db.relationship('Port', backref=db.backref('load_planning_discharges', lazy=True))

    ETA = db.Column(db.Date)
    volume = db.Column(db.Float)

