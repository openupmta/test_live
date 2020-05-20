# from flask import request
from flask_restplus import Resource, reqparse
import flask_excel as excel

from app.modules.load_planning.dto_load_planning import DtoLoadPlanning
from .controller_load_planning import ControllerLoadPlanning
# from app.modules.common.decorator import token_required
from ..port.port import Port
from ...utils.auth import token_required
from ...utils.response import send_result

api = DtoLoadPlanning.api
# region = Routing.route_article
_load_planning = DtoLoadPlanning.model

parser_search = reqparse.RequestParser()

parser_search.add_argument('port_load_id', type=int, required=False, help='The ID of the port load')
parser_search.add_argument('port_load_name', type=str, required=False, help='The name of the port load')

parser_search.add_argument('port_discharge_id', type=int, required=False, help='The ID of the port discharge')
parser_search.add_argument('port_discharge_name', type=str, required=False, help='The name of the port discharge')

parser_search.add_argument('vessel_id', type=int, required=False, help='The ID of the vessel')
parser_search.add_argument('vessel_name', type=str, required=False, help='The name of the vessel')

parser_search.add_argument('region_id', type=int, required=False, help='The ID of the region')
parser_search.add_argument('region_name', type=str, required=False, help='The name of the region')

# parser_search.add_argument('ETS', type=str, required=False, help='The date estimated')
parser_search.add_argument('voyage', type=str, required=False, help='The voyage')
# parser_search.add_argument('date_loading', type=str, required=False, help='The date of port loading')
parser_search.add_argument('status', type=str, required=False,
                           help='The current status of the load planning (it can be \'planned\' or in \'transit\')')
parser_search.add_argument('hash_value', type=str, required=False,
                           help='The hash value to search for')
parser_search.add_argument('from_date', type=str, required=False,
                           help='The lower bound of date created (format: yyyy-MM-dd)')
parser_search.add_argument('to_date', type=str, required=False,
                           help='The upper bound of date created (format: yyyy-MM-dd)')
parser_search.add_argument('file_type', type=str, required=False,
                           help='The file type to export (support xls, xlsx, csv)')


# @api.route('')
# class LoadPlanningList(Resource):
#     # @region.marshal_list_with(_load_planning)
#     # @token_required
#     def get(self):
#         """
#         Get load planning
#         """
#         # args = parser_search.parse_args()
#         controller = ControllerLoadPlanning()
#         return controller.get()
#
#     @api.expect(_load_planning)
#     def post(self):
#         """
#         Create load planning
#         """
#         data = api.payload
#         controller = ControllerLoadPlanning()
#         return controller.create(data=data)


@api.route('<int:load_planning_id>')
class LoadPlanning(Resource):
    @token_required
    def get(self, load_planning_id):
        """
        Return load planning by its ID.
        -------------
        :param `load_planning_id`: The ID of the Load Planning.

        :return: The LoadPlanning with respect ID.
        """
        controller = ControllerLoadPlanning()
        return controller.get_by_id(object_id=load_planning_id)

    # @api.expect(_load_planning)
    # def put(self, load_planning_id):
    #     data = api.payload
    #     controller = ControllerLoadPlanning()
    #     return controller.update(object_id=load_planning_id, data=data)
    #
    # def delete(self, load_planning_id):
    #     controller = ControllerLoadPlanning()
    #     return controller.delete(object_id=load_planning_id)


# @api.route("/voyage")
# class GetVoyages(Resource):
#     def get(self):
#         controller = ControllerLoadPlanning()
#         return controller.get_voyages()
#
#
# @api.route('<string:voyage>')
# class SearchByVoyage(Resource):
#     def get(self, voyage):
#         controller = ControllerLoadPlanning()
#         return controller.search_by_voyage(voyage=voyage)
#
#
# @api.route('/get_vessels_by_voyage/<string:voyage>')
# class SearchVesselsByVoyage(Resource):
#     def get(self, voyage):
#         controller = ControllerLoadPlanning()
#         return controller.search_vessel_by_voyage(voyage=voyage)


@api.route('/search')
@api.expect(parser_search)
class LoadPlanningSearch(Resource):
    @token_required
    def get(self):
        """
        Search all load plannings by params (see list of params below).
        ---------------------

        :return: List of buyers
        """
        args = parser_search.parse_args()
        controller = ControllerLoadPlanning()
        return controller.search(args=args)


parser_port_load = reqparse.RequestParser()
parser_port_load.add_argument('port_load_id', type=int, required=False, help='The ID of the port load')
parser_port_load.add_argument('port_load_name', type=str, required=False, help='The name of the port load')


@api.route('/port_load')
@api.expect(parser_port_load)
class PortLoadSearch(Resource):
    @token_required
    def get(self):
        """
        Search params according to port load information.
        ----------
        Search all related params according to the port load information.

        """
        args = parser_port_load.parse_args()
        controll = ControllerLoadPlanning()
        return controll.search_port_load(args=args)


parser_timeline = reqparse.RequestParser()
parser_timeline.add_argument('hash_value', type=str, required=True,
                             help='The hash value to find all related records in the system')
parser_timeline.add_argument('vessel_id', type=int, required=False, help='The ID of vessel')
parser_timeline.add_argument('vessel_name', type=str, required=False, help='The name of the vessel')
parser_timeline.add_argument('voyage', type=str, required=False, help='The voyage')


@api.route('/timeline')
@api.expect(parser_timeline)
class LoadPlanningTimeline(Resource):
    @token_required
    def get(self):
        """
        Return all load planning by timeline.
        -----------

        :return: List of Load Planning sorted by time.
        """
        args = parser_timeline.parse_args()
        controller = ControllerLoadPlanning()
        return controller.get_timeline(args=args)


@api.route('/download')
@api.expect(parser_search)
class LoadPlanningDownload(Resource):
    @token_required
    def get(self):
        """
        Return excel file from search params.
        ---------------

        :return: The excel file.
        """
        # return excel.make_response_from_array([[1, 2], [3, 4]], "csv",
        #                                       file_name="export_data")

        args = parser_search.parse_args()
        controller = ControllerLoadPlanning()
        return controller.download_export(args=args)

        # column_names = ['port_load_name', 'port_discharge_name', 'vessel_name', 'region_name', 'ETS', 'date_planned',
        #                 'date_transit', 'voyage', 'load_type', 'ETA', 'volume', 'date_created']
        # query_data = controller.download_export(args=args)
        # if query_data is None:
        #     return send_result(message="Could not process your request")
        # try:
        #
        #     # query_sets = Port.query.filter_by(port_id=133).all()
        #     # column_names = ['port_id', 'name', 'type', 'description', 'date_created']
        #     return excel.make_response_from_query_sets(query_sets=query_data, column_names=column_names,
        #                                                file_type='xls', file_name='ExportData')
        # except Exception as e:
        #     print(e.__str__())
        #     return send_result(message="Could not process your request")
