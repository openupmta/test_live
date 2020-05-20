from flask_restplus import Resource, reqparse
from .dto_load_planning_discharge import DtoLoadPlanningDischarge
from .controller_load_planning_discharge import ControllerLoadPlanningDischarge
from ...utils.auth import token_required

api = DtoLoadPlanningDischarge.api
_load_planning_discharge = DtoLoadPlanningDischarge.model


@api.route('')
class LoadPlanningDischargeList(Resource):
    @api.marshal_list_with(_load_planning_discharge)
    @token_required
    def get(self):
        controller = ControllerLoadPlanningDischarge()
        return controller.get()

    @api.expect(_load_planning_discharge)
    @token_required
    def post(self):
        data = api.payload
        controller = ControllerLoadPlanningDischarge()
        return controller.create(data=data)


@api.route('<int:load_planning_discharge_id>')
class LoadPlanningDischarge(Resource):
    @token_required
    def get(self, load_planning_discharge_id):
        controller = ControllerLoadPlanningDischarge()
        return controller.get_by_id(object_id=load_planning_discharge_id)

    @api.expect(_load_planning_discharge)
    @token_required
    def put(self, load_planning_discharge_id):
        data = api.payload
        controller = ControllerLoadPlanningDischarge()
        return controller.update(object_id=load_planning_discharge_id, data=data)

    @token_required
    def delete(self, load_planning_discharge_id):
        controller = ControllerLoadPlanningDischarge()
        return controller.delete(object_id=load_planning_discharge_id)
