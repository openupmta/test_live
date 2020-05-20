from flask_restplus import Namespace, fields
from app.modules.common.dto import Dto


class DtoVehicle(Dto):
    name = 'vehicle'
    api = Namespace(name)
    model = api.model(name, {
        'vehicle_id': fields.Integer(required=False),
        'load_planning_id': fields.Integer(required=False),

        'VIN': fields.String(required=False),
        'model': fields.String(required=False),
        'status': fields.String(required=False),

        'port_load_id': fields.Integer(required=False),
        'port_load_original_name': fields.String(required=False),
        'port_load_name': fields.String(required=False),
        'port_load_in': fields.Date(required=False),
        'port_load_out_ETS': fields.Date(required=False),
        'port_load_out_ATS': fields.Date(required=False),

        'port_discharge_id': fields.Integer(required=False),
        'port_discharge_original_name': fields.String(required=False),
        'port_discharge_name': fields.String(required=False),
        'port_discharge_in_ETA': fields.Date(required=False),
        'port_discharge_in_ATA': fields.Date(required=False),

        'vessel_id': fields.Integer(required=False),
        'vessel_name': fields.String(required=False),
        'vessel_voyage': fields.String(required=False),
        'date_created': fields.DateTime(required=False),

        'port_load_in_text': fields.String(required=False),
        'port_load_out_ETS_text': fields.String(required=False),
        'port_load_out_ATS_text': fields.String(required=False),
        'port_discharge_in_ETA_text': fields.String(required=False),
        'port_discharge_in_ATA_text': fields.String(required=False)
    })
