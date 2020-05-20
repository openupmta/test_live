from flask_restplus import  Namespace, fields
from ..common.dto import Dto

class DtoPort(Dto):
    name = 'port'
    api = Namespace(name)
    model = api.model(name, {
        'port_id':fields.Integer(required=False),
        'name':fields.String(required=True),
        'type':fields.String(required=False),
        'description':fields.String(required=False),
        'date_created':fields.DateTime(requied=False)
    })
