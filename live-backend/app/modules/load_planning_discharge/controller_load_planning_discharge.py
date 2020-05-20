from datetime import date
from flask_restplus import marshal
from app.modules.common.controller import Controller
from .load_planning_discharge import LoadPlanningDischarge
from .dto_load_planning_discharge import DtoLoadPlanningDischarge
from app.app import db
from app.utils.response import send_result, send_error


class ControllerLoadPlanningDischarge(Controller):
    def create(self, data):
        load_planning_discharge = self._parse_load_planning_dischare(data=data, load_planning_discharge=None)
        db.session.add(load_planning_discharge)
        db.session.commit()
        return send_result(data=marshal(load_planning_discharge, DtoLoadPlanningDischarge.model))

    def get(self):
        load_planning_discharges = LoadPlanningDischarge.query.all()
        return send_result(data=marshal(load_planning_discharges, DtoLoadPlanningDischarge.model))

    def get_by_id(self, object_id):
        load_planning_discharge = LoadPlanningDischarge.query.filter_by(load_planning_discharge_id=object_id).first()
        if load_planning_discharge is None:
            return send_error(message="Object not found!")
        return send_result(data=marshal(load_planning_discharge, DtoLoadPlanningDischarge.model))

    def update(self, object_id, data):
        load_planning_discharge = LoadPlanningDischarge.query.filter_by(load_planning_discharge_id=object_id).first()
        if load_planning_discharge is None:
            return send_error(message="Object not found!")
        load_planning_discharge = self._parse_load_planning_dischare(data=data,

                                                                     load_planning_discharge=load_planning_discharge)
        db.session.commit()
        return send_result(data=marshal(load_planning_discharge, DtoLoadPlanningDischarge.model))

    def delete(self, object_id):
        load_planning_discharge = LoadPlanningDischarge.query.filter_by(load_planning_discharge_id=object_id).first()
        if load_planning_discharge is None:
            return send_error(message="Object not found!")
        db.session.delete(load_planning_discharge)
        db.session.commit()
        return send_result("Object was deleted!")

    def _parse_load_planning_dischare(self, data, load_planning_discharge=None):
        load_planning_id, region_id, port_discharge_id, ETA, volume = None, None, None, None, None
        load_planning_id = data['load_planning_id']
        region_id = data['region_id']
        port_discharge_id = data['port_discharge_id']
        if 'ETA' in data:
            try:
                ETA = date.fromisoformat(data['ETA'])
            except Exception as e:
                print(e.__str__())
        if 'volume' in data:
            volume = float(data['volume'])

