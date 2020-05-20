from flask_restplus import Namespace, fields
from ..common.dto import Dto


class DtoLoadPlanning(Dto):
    name = 'load_planning'
    api = Namespace(name)
    model = api.model(name, {
        'load_planning_id': fields.Integer(required=False),

        'port_load_id': fields.Integer(required=False),
        'port_load_name': fields.String(required=False),

        'port_discharge_id': fields.Integer(required=False),
        'port_discharge_name': fields.String(required=False),

        'vessel_id': fields.Integer(required=False),
        'vessel_name': fields.String(required=False),

        'region_id': fields.Integer(required=False),
        'region_name': fields.String(required=False),

        # 'VIN': fields.String(required=False),
        'ETS_text': fields.String(required=False),
        'ETS': fields.Date(required=False),

        'date_planned_text': fields.String(required=False),
        'date_planned': fields.Date(required=False),
        'date_transit_text': fields.String(required=False),
        'date_transit': fields.Date(required=False),

        'voyage': fields.String(required=False),
        'load_type': fields.String(required=False),

        'ETA_text': fields.String(required=False),
        'ETA': fields.Date(required=False),
        'volume': fields.Integer(required=False),

        'date_created': fields.DateTime(required=False),
        'hash_value': fields.String(required=True),
    })
