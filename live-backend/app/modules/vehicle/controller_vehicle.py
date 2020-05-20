import datetime
from collections import defaultdict
from io import BytesIO

import pandas as pd
from flask import send_file
from flask_restplus import marshal
import flask_excel as excel
from sqlalchemy import inspect

from app.app import db
from app.modules.common.controller import Controller
from app.utils.response import send_result, send_error
from .vehicle import Vehicle
from .dto_vehicle import DtoVehicle
from ..port.controller_port import ControllerPort


class ControllerVehicle(Controller):

    def __init__(self):
        self.query_data = None

    def create(self, data):
        vehicle = self._parse_vehicle(data=data, vehicle=None)
        db.session.add(vehicle)
        db.session.commit()
        return send_result(data=marshal(vehicle, DtoVehicle.model))

    def get(self):
        vehicles = Vehicle.query.all()
        return send_result(data=marshal(vehicles, DtoVehicle.model))

    def get_by_id(self, object_id):
        vehicle = Vehicle.query.filter_by(vehicle_id=object_id).first()
        if vehicle is None:
            return send_error(message='Could not find any vehicle according to this ID {}'.format(object_id))
        return send_result(data=marshal(vehicle, DtoVehicle.model))

    def update(self, object_id, data):
        vehicle = Vehicle.query.filter_by(vehicle_id=object_id).first()
        if vehicle is None:
            return send_error(message='Could not find any vehicle according to this ID {}'.format(object_id))
        vehicle = self._parse_vehicle(data=data, vehicle=vehicle)
        db.session.commit()
        return send_result(data=marshal(vehicle, DtoVehicle.model))

    def search(self, args, returned=True):
        if not isinstance(args, dict):
            return send_error(message='Please enter params for searching')

        load_planning_id, port_load_id, port_load_name, port_discharge_id, port_discharge_name, vessel_id, vessel_name, region_id, region_name, voyage, status, from_date, to_date = None, None, None, None, None, None, None, None, None, None, None, None, None

        if 'load_planning_id' in args:
            load_planning_id = args['load_planning_id']

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

        # if 'region_id' in args:
        #     region_id = args['region_id']
        # if 'region_name' in args:
        #     region_name = args['region_name']

        if 'voyage' in args:
            voyage = args['voyage']
        # if 'status' in args:
        #     status = args['status']

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

        if load_planning_id is None and port_load_id is None and port_load_name is None and port_discharge_id is None and port_discharge_name is None and vessel_id is None and vessel_name is None and region_id is None and region_name is None and voyage is None and status is None and from_date is None and to_date is None:
            return send_error(message='Please enter params to search')

        query = db.session.query(Vehicle)
        is_filter = False
        if load_planning_id is not None and not str(load_planning_id).strip().__eq__(''):
            query = query.filter(Vehicle.load_planning_id == load_planning_id)
            is_filter = True

        if port_load_id is not None and not str(port_load_id).strip().__eq__(''):
            query = query.filter(Vehicle.port_load_id == port_load_id)
            is_filter = True
        if port_load_name is not None and not str(port_load_name).strip().__eq__(''):
            query = query.filter(Vehicle.port_load_original_name == port_load_name)
            is_filter = True

        if port_discharge_id is not None and not str(port_discharge_id).strip().__eq__(''):
            query = query.filter(Vehicle.port_discharge_id == port_discharge_id)
            is_filter = True
        if port_discharge_name is not None and not str(port_discharge_name).strip().__eq__(''):
            query = query.filter(Vehicle.port_discharge_name == port_discharge_name)
            is_filter = True

        if vessel_id is not None and not str(vessel_id).strip().__eq__(''):
            query = query.filter(Vehicle.vessel_id == vessel_id)
            is_filter = True
        if vessel_name is not None and not str(vessel_name).strip().__eq__(''):
            query = query.filter(Vehicle.vessel_name == vessel_name)
            is_filter = True

        # if region_id is not None and not str(region_id).strip().__eq__(''):
        #     query = query.filter(Vehicle.region_id == region_id)
        #     is_filter = True
        # if region_name is not None and not str(region_name).strip().__eq__(''):
        #     query = query.filter(Vehicle.region_name == region_name)
        #     is_filter = True

        if voyage is not None and not str(voyage).strip().__eq__(''):
            query = query.filter(Vehicle.vessel_voyage == voyage)
            is_filter = True
        # if status is not None and not str(status).strip().__eq__(''):
        #     query = query.filter(Vehicle.load_type == status)
        #     is_filter = True

        if from_date is not None:
            query = query.filter(Vehicle.date_created >= from_date)
            is_filter = True

        if to_date is not None:
            query = query.filter(Vehicle.date_created <= (to_date + datetime.timedelta(days=1)))
            is_filter = True

        if is_filter:
            try:
                vehicles = query.all()
                if returned:
                    data = marshal(vehicles, DtoVehicle.model)
                    return send_result(data=data)
                else:
                    self.query_data = vehicles
            except Exception as e:
                print(e.__str__())
                if returned:
                    return send_result(message="Could not find any result")
                else:
                    self.query_data = None
        else:
            if returned:
                send_result(message="Could not find any result")
            else:
                self.query_data = None

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
            # column_names = ['VIN', 'model', 'status', 'port_load_name', 'port_load_in', 'port_load_out_ETS',
            #                 'port_load_out_ATS', 'port_discharge_name', 'port_discharge_in_ETA',
            #                 'port_discharge_in_ATA', 'vessel_name', 'vessel_voyage']
            column_names = ['VIN', 'model', 'status', 'port_load_name', 'port_discharge_name', 'vessel_name',
                            'vessel_voyage']

            df1 = pd.DataFrame(self._query_to_dict(self.query_data), columns=column_names)
            # df1['date_created'] = df1['date_created'].dt.date

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
            worksheet.set_column(1, 1, 12)
            worksheet.set_column(2, 3, 25)
            worksheet.set_column(4, 4, 40)
            worksheet.set_column(5, 7, 20)
            # worksheet.set_column(7, 7, 15)

            # the writer has done its job
            writer.close()

            # go back to the beginning of the stream
            output.seek(0)

            # finally return the file
            return send_file(output, attachment_filename="vehicles.xlsx", as_attachment=True)

            # excel_file = excel.make_response_from_query_sets(query_sets=self.query_data, column_names=column_names,
            #                                                  file_type=file_type, file_name='vehicles')
            # return excel_file
            # return self.query_data
        except Exception as e:
            print(e.__str__())
            return None  # send_result(message="Could not process your request")

    def delete(self, object_id):
        vehicle = Vehicle.query.filter_by(vehicle_id=object_id).first()
        if vehicle is None:
            return send_error(message='Could not find any vehicle according to this ID {}'.format(object_id))
        db.session.delete(vehicle)
        db.session.commit()
        return send_result(message="Vehicle was deleted.")

    def _parse_vehicle(self, data, vehicle=None):
        load_planning_id, VIN, model, status, port_load_id, port_load_original_name, port_load_name, port_load_in, port_load_out_ETS, port_load_out_ATS, port_discharge_id, port_discharge_original_name, port_discharge_name, port_discharge_in_ETA, port_discharge_in_ATA, vessel_id, vessel_name, vessel_voyage, date_created, hash_value, port_load_in_text, port_load_out_ETS_text, port_load_out_ATS_text, port_discharge_in_ETA_text, port_discharge_in_ATA_text = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
        if 'load_planning_id' in data:
            load_planning_id = data['load_planning_id']

        if 'VIN' in data:
            VIN = data['VIN']
        if 'model' in data:
            model = data['model']
        if 'status' in data:
            status = data['status']

        if 'port_load_id' in data:
            port_load_id = data['port_load_id']
        if 'port_load_original_name' in data:
            port_load_original_name = data['port_load_original_name']
        if 'port_load_name' in data:
            port_load_name = data['port_load_name']
        if 'port_load_in' in data:
            try:
                port_load_in = datetime.date.fromisoformat(data['port_load_in'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'port_load_out_ETS' in data:
            try:
                port_load_out_ETS = datetime.date.fromisoformat(data['port_load_out_ETS'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'port_load_out_ATS' in data:
            try:
                port_load_out_ATS = datetime.date.fromisoformat(data['port_load_out_ATS'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'port_discharge_id' in data:
            port_discharge_id = data['port_discharge_id']
        if 'port_discharge_original_name' in data:
            port_discharge_original_name = data['port_discharge_original_name']
        if 'port_discharge_name' in data:
            port_discharge_name = data['port_discharge_name']
        if 'port_discharge_in_ETA' in data:
            try:
                port_discharge_in_ETA = datetime.date.fromisoformat(data['port_dischare_in_ETA'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'port_discharge_in_ATA' in data:
            try:
                port_discharge_in_ATA = datetime.date.fromisoformat(data['port_discharge_in_ATA'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'vessel_id' in data:
            vessel_id = data['vessel_id']
        if 'vessel_name' in data:
            vessel_name = data['vessel_name']
        if 'vessel_voyage' in data:
            vessel_voyage = data['vessel_voyage']

        if 'date_created' in data:
            try:
                date_created = datetime.datetime.fromisoformat(data['date_created'])
            except Exception as e:
                print(e.__str__())
                date_created = datetime.datetime.now()
        if 'hash_value' in data:
            hash_value = data['hash_value']

        if 'port_load_in_text' in data:
            port_load_in_text = data['port_load_in_text']
        if 'port_load_out_ETS_text' in data:
            port_load_out_ETS_text = data['port_load_out_ETS_text']
        if 'port_load_out_ATS_text' in data:
            port_load_out_ATS_text = data['port_load_out_ATS_text']
        if 'port_discharge_in_ETA_text' in data:
            port_discharge_in_ETA_text = data['port_discharge_in_ETA_text']
        if 'port_discharge_in_ATA_text' in data:
            port_discharge_in_ATA_text = data['port_discharge_in_ATA_text']

        if vehicle is None:
            vehicle = Vehicle(load_planning_id=load_planning_id, VIN=VIN, port_load_id=port_load_id,
                              port_load_original_name=port_load_original_name, port_load_name=port_load_name,
                              port_load_in=port_load_in, port_load_out_ETS=port_load_out_ETS,
                              port_load_out_ATS=port_load_out_ATS, port_discharge_id=port_discharge_id,
                              port_discharge_original_name=port_discharge_original_name,
                              port_discharge_name=port_discharge_name, port_discharge_in_ETA=port_discharge_in_ETA,
                              port_discharge_in_ATA=port_discharge_in_ATA, vessel_id=vessel_id, vessel_name=vessel_name,
                              vessel_voyage=vessel_voyage, date_created=date_created, hash_value=hash_value,
                              port_load_in_text=port_load_in_text, port_load_out_ETS_text=port_load_out_ETS_text,
                              port_load_out_ATS_text=port_load_out_ATS_text,
                              port_discharge_in_ETA_text=port_discharge_in_ETA_text,
                              port_discharge_in_ATA_text=port_discharge_in_ATA_text)
        else:

            vehicle.load_planning_id = load_planning_id
            vehicle.VIN = VIN
            vehicle.model = model
            vehicle.status = status

            vehicle.port_load_id = port_load_id
            vehicle.port_load_original_name = port_load_original_name
            vehicle.port_load_name = port_load_name
            vehicle.port_load_in = port_load_in
            vehicle.port_load_out_ETS = port_load_out_ETS
            vehicle.port_load_out_ATS = port_load_out_ATS

            vehicle.port_discharge_id = port_discharge_id
            vehicle.port_discharge_original_name = port_discharge_original_name
            vehicle.port_discharge_name = port_discharge_name
            vehicle.port_dischare_in_ETA = port_discharge_in_ETA
            vehicle.port_discharge_in_ATA = port_discharge_in_ATA

            vehicle.vessel_id = vessel_id
            vehicle.vessel_name = vessel_name
            vehicle.vessel_voyage = vessel_voyage

            vehicle.date_created = date_created
            vehicle.hash_value = hash_value

            vehicle.port_load_in_text = port_load_in_text
            vehicle.port_load_out_ETS_text = port_load_out_ETS_text
            vehicle.port_load_out_ATS_text = port_load_out_ATS_text
            vehicle.port_discharge_in_ETA_text = port_discharge_in_ETA_text
            vehicle.port_discharge_in_ATA_text = port_discharge_in_ATA_text

        return vehicle
