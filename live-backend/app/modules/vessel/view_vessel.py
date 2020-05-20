from flask_restplus import Resource
from flask_restplus import reqparse
from .dto_vessel import DtoVessel
from .controller_vessel import ControllerVessel
from ...utils.auth import token_required

api = DtoVessel.api
_vessel = DtoVessel.model

# @api.route('')
# class VesselList(Resource):
#     # @api.marshal_list_with(_vessel)
#     def get(self):
#         """
#         Get list of vessels.
#         --------------
#         :return: List of vessels.
#         """
#         controller = ControllerVessel()
#         return controller.get()
#
#     @api.expect(_vessel)
#     def post(self):
#         """
#         Create a new vessel.
#         -------------------
#         Parameters:
#             `name`: The name of the vessel
#             `acronym`: The acronym of the vessel
#             `description`: The description of the vessel
#
#         :return: The new vessel which created
#         """
#         data = api.payload
#         controller = ControllerVessel()
#         return controller.create(data=data)

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=False, help='The name of vessel to search')
parser.add_argument('acronym', type=str, required=False, help='The acronym of the vessel name to search')


@api.route('<int:vessel_id>')
class Vessel(Resource):
    @token_required
    def get(self, vessel_id):
        """
        Get vessel by its ID.
        ----------
        :param `vessel_id`: The ID of the vessel.

        :return: The vessel with the given ID.
        """
        controller = ControllerVessel()
        return controller.get_by_id(object_id=vessel_id)

    # @api.expect(_vessel)
    # def put(self, vessel_id):
    #     """
    #     Update an existing vessel.
    #     -----------------
    #     Parameters:
    #         `name`: The name of the vessel
    #         `acronym`: The acronym of the vessel
    #         `description`: The description of the vessel
    #
    #     :param `vessel_id`: The ID of the vessel
    #
    #     :return: The updated vessel.
    #     """
    #     data = api.payload
    #     controller = ControllerVessel()
    #     return controller.update(object_id=vessel_id, data=data)

    # def delete(self, vessel_id):
    #     """
    #     Delete an existing vessel by its ID.
    #     --------------
    #     :return: True if success and False vice versa.
    #     """
    #     controller = ControllerVessel()
    #     return controller.delete(object_id=vessel_id)


@api.route('/search')
@api.expect(parser)
class SearchVesselByName(Resource):
    @token_required
    def get(self):
        """
        Search vessels by name and acronym.
        -----------
        :return: The list of vessels if exist and null vice versa
        """
        args = parser.parse_args()
        controller = ControllerVessel()
        return controller.search(args=args)
