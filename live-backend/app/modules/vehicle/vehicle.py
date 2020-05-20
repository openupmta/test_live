import datetime
from app.app import db
from app.modules.common.model import Model


class Vehicle(Model):
    """
    This class describes all information about vehicle.
    """
    __tablename__ = 'vehicle'

    vehicle_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    load_planning_id = db.Column(db.Integer)  # the load planning id

    VIN = db.Column(db.String)
    model = db.Column(db.String)
    status = db.Column(db.String)

    port_load_id = db.Column(db.Integer)
    port_load_original_name = db.Column(db.String)
    port_load_name = db.Column(db.String)
    port_load_in = db.Column(db.Date)
    port_load_out_ETS = db.Column(db.Date)
    port_load_out_ATS = db.Column(db.Date)

    port_discharge_id = db.Column(db.Integer)
    port_discharge_original_name = db.Column(db.String)
    port_discharge_name = db.Column(db.String)
    port_discharge_in_ETA = db.Column(db.Date)
    port_discharge_in_ATA = db.Column(db.Date)

    vessel_id = db.Column(db.Integer)
    vessel_name = db.Column(db.String)
    vessel_voyage = db.Column(db.String)

    date_created = db.Column(db.DateTime, default=datetime.datetime.now())
    hash_value = db.Column(db.String)

    port_load_in_text = db.Column(db.String)
    port_load_out_ETS_text = db.Column(db.String)
    port_load_out_ATS_text = db.Column(db.String)
    port_discharge_in_ETA_text = db.Column(db.String)
    port_discharge_in_ATA_text = db.Column(db.String)
