from flask_restplus import Resource, reqparse
from app.modules.region.dto_region import DtoRegion
from .controller_region import ControllerRegion
from ...utils.auth import token_required

api = DtoRegion.api
_region = DtoRegion.model

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=False, help='The name of vessel to search')
parser.add_argument('acronym', type=str, required=False, help='The acronym of the vessel name to search')

# @api.route('')
# class RegionList(Resource):
#     # @api.marshal_list_with(_region)
#     def get(self):
#         """
#         Get list of regions in database.
#         -----------------
#         :return: List of regions.
#         """
#         controller = ControllerRegion()
#         return controller.get()
#
#     @api.expect(_region)
#     def post(self):
#         """
#         Create new region.
#         -----------
#         Parameters:
#             `name`: The name of the region
#             `acronym`: The acronym of the region
#             `description`: The description of the region
#         """
#         data = api.payload
#         controller = ControllerRegion()
#         return controller.create(data=data)


@api.route('<int:region_id>')
class Region(Resource):
    @token_required
    def get(self, region_id):
        """
        Return region by its ID.
        --------------
        :param `region_id`: The ID of the region

        :return: The region with the given ID.
        """
        controller = ControllerRegion()
        return controller.get_by_id(object_id=region_id)

    # @api.expect(_region)
    # def put(self, region_id):
    #     """
    #     Update an existing region.
    #     -----------
    #     Parameters in the payload:
    #         `name`: The name of the region
    #         `acronym`: The acronym of the region
    #         `description`: The description of the region
    #
    #     :param `region_id`: The ID of the region.
    #
    #     :return: The region after updating.
    #     """
    #     data = api.payload
    #     controller = ControllerRegion()
    #     return controller.update(object_id=region_id, data=data)
    #
    # def delete(self, region_id):
    #     """
    #     Delete an existing region.
    #     --------------
    #     :param `region_id`: The ID of the region
    #
    #     :return: True if success and False vice versa.
    #     """
    #     controller = ControllerRegion()
    #     return controller.delete(object_id=region_id)


@api.route('/search')
@api.expect(parser)
class SearchRegion(Resource):
    @token_required
    def get(self):
        """
        Search regions by name and acronym.
        ------------
        :params to search: see list below.

        :return: The list of regions.
        """
        args = parser.parse_args()
        controller = ControllerRegion()
        return controller.search(args = args)