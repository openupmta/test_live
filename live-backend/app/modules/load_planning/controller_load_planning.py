import datetime
import json
import ast
from collections import defaultdict
from io import BytesIO

import pandas as pd
from flask import send_file
from flask_restplus import marshal
import flask_excel as excel
from sqlalchemy import inspect

from app.app import db
from app.modules.port.port import Port
from app.modules.common.controller import Controller
from app.modules.vessel.vessel import Vessel
from app.modules.load_planning.dto_load_planning import DtoLoadPlanning
from app.utils.response import send_result, send_error
from .load_planning import LoadPlanning
from ..port.controller_port import ControllerPort
from ..vessel.dto_vessel import DtoVessel
from datetime import date


class ControllerLoadPlanning(Controller):
    """
    Controller to mamage all interaction to load_planning table in database.
    """

    def __init__(self):
        self.query_data = None

    def create(self, data):
        """
        """
        load_planning = self._parse_load_planning(data=data, load_planning=None)
        db.session.add(load_planning)
        db.session.commit()
        return send_result(data=marshal(load_planning, DtoLoadPlanning.model))

    def get(self):
        """
        """
        load_plannings = LoadPlanning.query.all()
        return send_result(data=marshal(load_plannings, DtoLoadPlanning.model))

    def get_by_id(self, object_id):
        load_planning = LoadPlanning.query.filter_by(load_planning_id=object_id).first()
        if load_planning is None:
            return send_error(message="Load planning not found")
        return send_result(data=marshal(load_planning, DtoLoadPlanning.model))

    def update(self, object_id, data):
        load_planning = LoadPlanning.query.filter_by(load_planning_id=object_id).first()
        if load_planning is None:
            return send_error("Could not update, object not found.")
        load_planning = self._parse_load_planning(data=data, load_planning=load_planning)
        db.session.commit()
        return send_result(data=marshal(load_planning, DtoLoadPlanning.model))

    def delete(self, object_id):
        load_planning = LoadPlanning.query.filter_by(load_planning_id=object_id).first()
        if load_planning is None:
            return send_error("Could not delete, object not found.")
        db.session.delete(load_planning)
        db.session.commit()
        return send_result(message="Load planning was deleted.")

    def search_vessel_by_voyage(self, voyage):
        if voyage is None or str(voyage).strip().__eq__(''):
            return send_error(message="Voyage can not be null or empty")
        load_planning_vessels = LoadPlanning.query.filter_by(voyage=voyage).all()
        if load_planning_vessels is None:
            return send_error(message="Not found any vessel according to voyage {}".format(voyage))
        vessels = list()
        for load_planning_vessel in load_planning_vessels:
            vessel_id = load_planning_vessel.vessel_id
            vessel = Vessel.query.filter_by(vessel_id).first()
            if vessel is not None:
                vessels.append(vessel)
        return send_result(data=marshal(vessels, DtoVessel.model))

    def search_by_voyage(self, voyage):
        if voyage is None or str(voyage).strip().__eq__(''):
            return send_error(message="Voyage can not be null or empty")
        load_planning_vessels = LoadPlanning.query.filter_by(voyage=voyage).all()
        if load_planning_vessels is None:
            return send_error(message="Not found any vessel according to voyage {}".format(voyage))
        return send_result(data=marshal(load_planning_vessels, DtoLoadPlanning.model))

    def get_voyages(self):
        voyages = db.session.query(LoadPlanning.voyage).distinct()
        return ast.literal_eval(str(voyages))

    def search(self, args, returned=True):
        """
        Search by params.

        :param args: The dictionary of all params
        :param returned: The indicator to return to client.

        :return:
        """
        if not isinstance(args, dict):
            return send_error(message='Please enter params for searching')

        port_load_id, port_load_name, port_discharge_id, port_discharge_name, vessel_id, vessel_name, region_id, region_name, voyage, status, from_date, to_date, hash_value = None, None, None, None, None, None, None, None, None, None, None, None, None

        if 'port_load_id' in args:
            port_load_id = args['port_load_id']
        if 'port_load_name' in args:
            port_load_name = args['port_load_name']

        if 'port_discharge_id' in args:
            port_discharge_id = args['port_discharge_id']
        if 'port_discharge_name' in args:
            port_discharge_name = args['port_discharge_name']

        if 'vessel_id' in args:
            vessel_id = args['vessel_id']
        if 'vessel_name' in args:
            vessel_name = args['vessel_name']

        if 'region_id' in args:
            region_id = args['region_id']
        if 'region_name' in args:
            region_name = args['region_name']

        if 'voyage' in args:
            voyage = args['voyage']
        if 'status' in args:
            status = args['status']

        if 'hash_value' in args:
            hash_value = args['hash_value']

        if 'from_date' in args:
            try:
                from_date = datetime.datetime.fromisoformat(args['from_date'])
            except Exception as e:
                print(e.__str__())
                from_date = None

        if 'to_date' in args:
            try:
                to_date = datetime.datetime.fromisoformat(args['to_date'])
            except Exception as e:
                print(e.__str__())
                to_date = None

        if port_load_id is None and port_load_name is None and port_discharge_id is None and port_discharge_name is None and vessel_id is None and vessel_name is None and region_id is None and region_name is None and voyage is None and status is None and hash_value is None and from_date is None and to_date is None:
            return send_error(message='Please enter params to search')

        query = db.session.query(LoadPlanning)
        is_filter = False
        if port_load_id is not None and not str(port_load_id).strip().__eq__(''):
            query = query.filter(LoadPlanning.port_load_id == port_load_id)
            is_filter = True
        if port_load_name is not None and not str(port_load_name).strip().__eq__(''):
            query = query.filter(LoadPlanning.port_load_name == port_load_name)
            is_filter = True

        if port_discharge_id is not None and not str(port_discharge_id).strip().__eq__(''):
            query = query.filter(LoadPlanning.port_discharge_id == port_discharge_id)
            is_filter = True
        if port_discharge_name is not None and not str(port_discharge_name).strip().__eq__(''):
            query = query.filter(LoadPlanning.port_discharge_name == port_discharge_name)
            is_filter = True

        if vessel_id is not None and not str(vessel_id).strip().__eq__(''):
            query = query.filter(LoadPlanning.vessel_id == vessel_id)
            is_filter = True
        if vessel_name is not None and not str(vessel_name).strip().__eq__(''):
            query = query.filter(LoadPlanning.vessel_name == vessel_name)
            is_filter = True

        if region_id is not None and not str(region_id).strip().__eq__(''):
            query = query.filter(LoadPlanning.region_id == region_id)
            is_filter = True
        if region_name is not None and not str(region_name).strip().__eq__(''):
            query = query.filter(LoadPlanning.region_name == region_name)
            is_filter = True

        if voyage is not None and not str(voyage).strip().__eq__(''):
            query = query.filter(LoadPlanning.voyage == voyage)
            is_filter = True
        if status is not None and not str(status).strip().__eq__(''):
            query = query.filter(LoadPlanning.load_type == status)
            is_filter = True

        if hash_value is not None and not str(hash_value).strip().__eq__(''):
            query = query.filter(LoadPlanning.hash_value == hash_value)
            is_filter = True

        if from_date is not None:
            query = query.filter(LoadPlanning.date_created >= from_date)
            is_filter = True

        if to_date is not None:
            query = query.filter(LoadPlanning.date_created <= (to_date + datetime.timedelta(days=1)))
            is_filter = True

        if is_filter:
            try:
                load_plannings = query.order_by(LoadPlanning.date_created.asc()).all()
                # self.query_data = load_plannings
                if returned:
                    data = marshal(load_plannings, DtoLoadPlanning.model)
                    return send_result(data=data)
                else:
                    self.query_data = load_plannings
            except Exception as e:
                # self.query_data = None
                print(e.__str__())
                if returned:
                    return send_result(message="Could not find any result")
                else:
                    self.query_data = None
        else:
            # self.query_data = None
            if returned:
                send_result(message="Could not find any result")
            else:
                self.query_data = None

    def search_port_load(self, args):
        if not isinstance(args, dict):
            return send_error(message='Please enter params for searching')

        port_load_id, port_load_name = None, None

        if 'port_load_id' in args:
            port_load_id = args['port_load_id']
        if 'port_load_name' in args:
            port_load_name = args['port_load_name']

        if port_load_id is None and port_load_name is None:
            return send_error(message="Please enter the params to search")

        query = db.session.query(LoadPlanning)
        # get port_discharge
        is_filter = False
        port_discharges = list()
        regions = list()
        status = list()
        vessels = list()
        voyages = list()

        if port_load_id is not None and not str(port_load_id).strip().__eq__(''):
            query = query.filter(LoadPlanning.port_load_id == port_load_id)
            is_filter = True
        if port_load_name is not None and not str(port_load_name).strip().__eq__(''):
            query = query.filter(LoadPlanning.port_load_name == port_load_name)
            is_filter = True
        if is_filter:
            try:
                load_plannings = query.all()
                if load_plannings is not None and len(load_plannings) > 0:
                    for load_planning in load_plannings:
                        port_discharge_name = load_planning.port_discharge_name
                        port_discharges.append(port_discharge_name)
                        region = load_planning.region_name
                        regions.append(region)
                        load_type = load_planning.load_type
                        status.append(load_type)
                        vessel = load_planning.vessel_name
                        vessels.append(vessel)
                        voyage = load_planning.voyage
                        voyages.append(voyage)
                data = dict()
                data['port_discharge'] = sorted(list(set(port_discharges)))
                data['region'] = sorted(list(set(regions)))
                data['vessel'] = sorted(list(set(vessels)))
                data['voyage'] = sorted(list(set(voyages)))
                data['status'] = list(set(status))
                return send_result(data=data)
            except Exception as e:
                print(e.__str__())
                return send_error(message="Could not find any result.")
        else:
            return send_error(message="Could not find any result.")

    def get_timeline(self, args):
        if not isinstance(args, dict):
            return send_error(message='Please enter params for searching')

        vessel_id, vessel_name, voyage, hash_value = None, None, None, None
        # get values of params
        if 'vessel_id' in args:
            vessel_id = args['vessel_id']
        if 'vessel_name' in args:
            vessel_name = args['vessel_name']
        if 'voyage' in args:
            voyage = args['voyage']
        if 'hash_value' in args:
            hash_value = args['hash_value']

        if vessel_id is None and vessel_name is None and voyage is None and hash_value is None:
            return send_error(message='Please enter params to search')

        query = db.session.query(LoadPlanning)
        query_volum = db.session.query(LoadPlanning)
        is_filter = False

        if vessel_id is not None and not str(vessel_id).strip().__eq__(''):
            query = query.filter(LoadPlanning.vessel_id == vessel_id)
            query_volum = query_volum.filter(LoadPlanning.vessel_name == 'VOLUMENPROGNOSE')
            is_filter = True
        if vessel_name is not None and not str(vessel_name).strip().__eq__(''):
            query = query.filter(LoadPlanning.vessel_name == vessel_name)
            query_volum = query_volum.filter(LoadPlanning.vessel_name == 'VOLUMENPROGNOSE')
            is_filter = True
        if voyage is not None and not str(voyage).strip().__eq__(''):
            query = query.filter(LoadPlanning.voyage == voyage)
            query_volum = query_volum.filter(LoadPlanning.voyage == voyage)
            is_filter = True

        if hash_value is not None and not str(hash_value).strip().__eq__(''):
            query = query.filter(LoadPlanning.hash_value == hash_value)
            query_volum = query_volum.filter(LoadPlanning.hash_value == hash_value)
            is_filter = True
        if is_filter:
            try:
                # lay ra nhung records ko phai la VOLUMENPROGNOSE
                query_total = query.union(query_volum)
                # lay ra record la VOLUMENPROGNOSE
                load_plannings = query_total.order_by(LoadPlanning.date_created.asc()).all()
                data = marshal(load_plannings, DtoLoadPlanning.model)
                return send_result(data=data)
            except Exception as e:
                print(e.__str__())
                return send_result(message="Could not find any result")
        else:
            send_result(message="Could not find any result")

    def _query_to_dict(self, rset):
        result = defaultdict(list)
        for obj in rset:
            instance = inspect(obj)
            for key, x in instance.attrs.items():
                result[key].append(x.value)
        return result

    def download_export(self, args):
        if not isinstance(args, dict):
            return send_error(message='Please enter params for searching')
        self.search(args=args, returned=False)
        file_type = None
        if 'file_type' in args:
            file_type = args['file_type']
        if file_type is None:
            file_type = 'xls'
        if self.query_data is None:
            return send_result(message="Could not process")
        # return self.query_data
        try:

            column_names = ['port_load_name', 'port_discharge_name', 'vessel_name', 'region_name', 'ETS',
                            'date_planned',
                            'date_transit', 'voyage', 'load_type', 'ETA', 'volume', 'date_created']

            df1 = pd.DataFrame(self._query_to_dict(self.query_data), columns=column_names)
            df1['date_created'] = df1['date_created'].dt.date

            # df1 = pd.DataFrame(self.query_data, columns=column_names)

            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')

            # taken from the original question
            df1.to_excel(writer, startrow=0, merge_cells=False, sheet_name="Sheet_1")
            workbook = writer.book
            worksheet = writer.sheets["Sheet_1"]
            format = workbook.add_format()
            format.set_bg_color('#eeeeee')
            worksheet.set_column(0, 0, 5)
            worksheet.set_column(1, 3, 20)
            worksheet.set_column(4, 4, 12)
            worksheet.set_column(5, 10, 15)
            worksheet.set_column(11, 11, 10)
            formatdict = {'num_format': 'yyyy-MM-dd'}
            fmt = workbook.add_format(formatdict)
            worksheet.set_column(12, 12, 15, fmt)

            # the writer has done its job
            writer.close()

            # go back to the beginning of the stream
            output.seek(0)

            # finally return the file
            return send_file(output, attachment_filename="load_planning.xlsx", as_attachment=True)

            # excel_file = excel.make_response_from_query_sets(query_sets=self.query_data, column_names=column_names,
            #                                                  file_type=file_type, file_name='load_planning')
            # return excel_file
            # return self.query_data
        except Exception as e:
            print(e.__str__())
            return None  # send_result(message="Could not process your request")

    def _parse_load_planning(self, data, load_planning=None):
        port_load_id, port_load_name, port_discharge_id, port_discharge_name, vessel_id, vessel_name, region_id, region_name, ETS_text, ETS, date_planned_text, date_planned, date_transit_text, date_transit, voyage, load_type, ETA_text, ETA, volume, date_created, hash_value = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None

        if 'port_load_id' in data:
            port_load_id = data['port_load_id']
        if 'port_load_name' in data:
            port_load_name = data['port_load_name']

        if 'port_discharge_id' in data:
            port_discharge_id = data['port_discharge_id']
        if 'port_discharge_name' in data:
            port_discharge_name = data['port_discharge_name']

        if 'vessel_id' in data:
            vessel_id = data['vessel_id']
        if 'vessel_name' in data:
            vessel_name = data['vessel_name']

        if 'region_id' in data:
            region_id = data['region_id']
        if 'region_name' in data:
            region_name = data['region_name']

        if 'ETS_text' in data:
            ETS_text = data['ETS_text']
        if 'ETS' in data:
            try:
                ETS = date.fromisoformat(data['ETS'])
            except Exception as e:
                print(e.__str__())

        if 'date_planned_text' in data:
            date_planned_text = data['date_planned_text']
        if 'date_planned' in data:
            try:
                date_planned = date.fromisoformat(data['date_planned'])
            except Exception as e:
                print(e.__str__())

        if 'date_transit_text' in data:
            date_transit_text = data['date_transit_text']
        if 'date_transit' in data:
            try:
                date_transit = date.fromisoformat(data['date_transit'])
            except Exception as e:
                print(e.__str__())

        if 'voyage' in data:
            voyage = data['voyage']

        if 'load_type' in data:
            load_type = data['load_type']

        if 'ETA_text' in data:
            ETA_text = data['ETA_text']
        if 'ETA' in data:
            try:
                ETA = date.fromisoformat(data['ETA'])
            except Exception as e:
                print(e.__str__())

        if 'volume' in data:
            volume = float(data['volume'])

        if 'date_created' in data:
            try:
                date_created = datetime.datetime.fromisoformat(data['date_created'])
            except Exception as e:
                print(e.__str__())
                date_created = datetime.datetime.now()
        if 'hash_value' in data:
            hash_value = data['hash_value']

        if load_planning is None:
            load_planning = LoadPlanning(port_load_id=port_load_id, port_load_name=port_load_name,
                                         port_discharge_id=port_discharge_id, port_discharge_name=port_discharge_name,
                                         vessel_id=vessel_id, vessel_name=vessel_name, region_id=region_id,
                                         region_name=region_name, ETS_text=ETS_text, ETS=ETS,
                                         date_planned_text=date_planned_text, date_planned=date_planned,
                                         date_transit_text=date_transit_text,
                                         date_transit=date_transit, voyage=voyage, load_type=load_type,
                                         ETA_text=ETA_text, ETA=ETA,
                                         volume=volume, date_created=date_created, hash_value=hash_value)
        else:
            load_planning.port_load_id = port_load_id
            load_planning.port_load_name = port_load_name
            load_planning.port_discharge_id = port_discharge_id
            load_planning.port_discharge_name = port_discharge_name

            load_planning.vessel_id = vessel_id
            load_planning.vessel_name = vessel_name
            load_planning.region_id = region_id
            load_planning.region_name = region_name

            load_planning.ETS_text = ETS_text
            load_planning.ETS = ETS

            load_planning.date_planned_text = date_planned_text
            load_planning.date_planned = date_planned

            load_planning.date_transit_text = date_transit_text
            load_planning.date_transit = date_transit

            load_planning.voyage = voyage
            load_planning.load_type = load_type

            load_planning.ETA_text = ETA_text
            load_planning.ETA = ETA
            load_planning.volume = volume

            load_planning.date_created = date_created
            load_planning.hash_value = hash_value
        return load_planning
