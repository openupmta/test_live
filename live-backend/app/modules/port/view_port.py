from flask_restplus import Resource, reqparse
from app.modules.port.dto_port import DtoPort
from .controller_port import ControllerPort
from ...utils.auth import token_required

api = DtoPort.api
_port = DtoPort.model

parser = reqparse.RequestParser()


# @api.route('')
# class PortList(Resource):
#     # @api.marshal_list_with(_port)
#     def get(self):
#         """
#         Return all ports in the systems. This functions is used for administration only.
#
#         :return: List of ports.
#         """
#         controller = ControllerPort()
#         return controller.get()
#
#     @api.expect(_port)
#     def post(self):
#         """
#         Create port
#         ------------
#         Parameters:
#             name: The name of the port
#             type: The type of the port
#             description: The description of the port
#         """
#         data = api.payload
#         controller = ControllerPort()
#         return controller.create(data=data)


@api.route('/<int:port_id>')
class Port(Resource):
    @token_required
    def get(self, port_id):
        """
        Return specific port by its ID.

        :param port_id: The ID of the port.

        :return: The port with specific ID if port exists and null vice versa.
        """
        controller = ControllerPort()
        return controller.get_by_id(object_id=port_id)

    # @api.expect(_port)
    # def put(self, port_id):
    #     """
    #     Update port.
    #     -------------
    #     Parameters:
    #         port_id: The ID of the port used to update data.
    #         name: The new name of the port.
    #         type: The new type of the port.
    #         description: The new description of the port.
    #     """
    #     data = api.payload
    #     controller = ControllerPort()
    #     return controller.update(object_id=port_id, data=data)
    #
    # def delete(self, port_id):
    #     """
    #     Delete port by its ID.
    #     -----------
    #     :param port_id: The ID of the port.
    #
    #     :return: True if success.
    #             False vice versa.
    #     """
    #     controller = ControllerPort()
    #     return controller.delete(object_id=port_id)


parser.add_argument('name', type=str, required=False, help='The name of the port')
parser.add_argument('type', type=str, required=False, help='The type of port')


@api.route('/search')
@api.expect(parser)
class SearchPortByName(Resource):
    @token_required
    def get(self):
        """
        Search port by using different params.
        ---------------
        :params to search: see list below.

        :return list of ports.
        """
        args = parser.parse_args()
        controller = ControllerPort()
        return controller.search(args=args)
