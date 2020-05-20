from flask_restplus import Resource, reqparse

from .dto_vehicle import DtoVehicle
from .controller_vehicle import ControllerVehicle
from ...utils.auth import token_required

api = DtoVehicle.api
_vehicle = DtoVehicle.model


# @api.route('')
# class VehicleList(Resource):
#     def get(self):
#         """
#         Get all vehicle in the system.
#         ----------------
#         """
#         controller = ControllerVehicle()
#         return controller.get()
#
#     @api.expect(_vehicle)
#     def post(self):
#         """
#         Create new vehicle.
#         ---------------
#         """
#         data = api.payload
#         controller = ControllerVehicle()
#         return controller.create(data=data)

@api.route('/<int:vehicle_id>')
class Vehicle(Resource):
    @token_required
    def get(self, vehicle_id):
        """
        Get information about vehicle by its ID.
        --------------
        """
        controller = ControllerVehicle()
        return controller.get_by_id(object_id=vehicle_id)

    # @api.expect(_vehicle)
    # def put(self, vehicle_id):
    #     """
    #     Update existing vehicle by its ID.
    #     --------------
    #     """
    #     data = api.payload
    #     controller = ControllerVehicle()
    #     return controller.update(object_id=vehicle_id, data=data)
    #
    # def delete(self, vehicle_id):
    #     """
    #     Delete vehicle by its ID.
    #     ---------------
    #     """
    #     controller = ControllerVehicle()
    #     return controller.delete(object_id=vehicle_id)


parser = reqparse.RequestParser()

parser.add_argument('load_planning_id', type=int, required=False, help='The ID of the load planning')

parser.add_argument('port_load_id', type=int, required=False, help='The ID of the port load')
parser.add_argument('port_load_name', type=str, required=False, help='The name of the port load')

parser.add_argument('port_discharge_id', type=int, required=False, help='The ID of the port discharge')
parser.add_argument('port_discharge_name', type=str, required=False, help='The name of the port discharge')

parser.add_argument('vessel_id', type=int, required=False, help='The ID of the vessel')
parser.add_argument('vessel_name', type=str, required=False, help='The name of the vessel')
parser.add_argument('voyage', type=str, required=False, help='The voyage')
parser.add_argument('from_date', type=str, required=False,
                           help='The lower bound of date created (format: yyyy-MM-dd)')
parser.add_argument('to_date', type=str, required=False,
                           help='The upper bound of date created (format: yyyy-MM-dd)')
parser.add_argument('file_type', type=str, required=False,
                           help='The file type to export (support xls, xlsx, csv)')


# parser_search.add_argument('date_loading', type=str, required=False, help='The date of port loading')
# parser_search.add_argument('status', type=str, required=False, help='The current status of the load planning')

@api.route('/search')
@api.expect(parser)
class SearchVehicle(Resource):
    @token_required
    def get(self):
        """
        Search vehicles using different parameters.
        -----------------
        :return: List of vehicles if found and null vice versa.
        """
        args = parser.parse_args()
        controller = ControllerVehicle()
        return controller.search(args=args)

@api.route('/download')
@api.expect(parser)
class VehicleExport(Resource):
    @token_required
    def get(self):
        """
        Search data by parameters and export and return excel file.
        ------------------------
        """
        args = parser.parse_args()
        controlelr = ControllerVehicle()
        return controlelr.download_export(args=args)