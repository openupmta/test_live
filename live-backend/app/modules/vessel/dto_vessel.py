from flask_restplus import Namespace, fields
from app.modules.common.dto import Dto


class DtoVessel(Dto):
    name = 'vessel'
    api = Namespace(name)
    model = api.model(name, {
        'vessel_id': fields.Integer(required=False),
        'name': fields.String(required=False),
        'acronym': fields.String(required=False),
        'description': fields.String(required=False),
        'date_created': fields.DateTime(requied=False)
    })
