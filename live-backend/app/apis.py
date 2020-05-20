from flask_restplus import Api
from app.modules import ns_load_planning, ns_load_planning_discharge, ns_port, ns_region, ns_vessel, ns_vehicle

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}


def init_api():
    api = Api(title='Live Vessel Voyage APIs',
              version='1.0',
              description='Vessel Voyage API',
              authorizations=authorizations,
              security='apikey')
    api.add_namespace(ns_port, '/api/v1/port')
    api.add_namespace(ns_region, '/api/v1/region')
    api.add_namespace(ns_vessel, '/api/v1/vessel')
    api.add_namespace(ns_load_planning, path='/api/v1/load_planning')
    api.add_namespace(ns_vehicle, '/api/v1/vehicle')
    # api.add_namespace(ns_load_planning_discharge, path='/api/v1/load_planning_discharge')
    return api
