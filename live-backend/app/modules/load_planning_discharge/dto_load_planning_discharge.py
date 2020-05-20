from flask_restplus import Namespace, fields
from app.modules.common.dto import Dto


class DtoLoadPlanningDischarge(Dto):
    name = 'load_planning_discharge'
    api = Namespace(name)
    model = api.model(name, {
        'load_planning_discharge_id': fields.Integer(required=False),
        'load_planning_id': fields.Integer(required=False),
        'region_id': fields.Integer(required=False),
        'port_discharge_id': fields.Integer(required=False),
        'ETA': fields.Date(required=False),
        'volume': fields.Float(required=False)
    })
