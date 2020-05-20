import datetime

from flask_restplus import marshal
from app.modules.common.controller import Controller
from app.app import db
from app.utils.response import send_error, send_result
from .vessel import Vessel
from .dto_vessel import DtoVessel


class ControllerVessel(Controller):
    def create(self, data):
        vessel = self._parse_vessel(data=data, vessel=None)
        db.session.add(vessel)
        db.session.commit()
        return send_result(data=marshal(vessel, DtoVessel.model))

    def get(self):
        vessels = Vessel.query.all()
        return send_result(data=marshal(vessels, DtoVessel.model))

    def get_by_id(self, object_id):
        vessel = Vessel.query.filter_by(vessel_id=object_id).first()
        if vessel is None:
            return send_error(message="Could not find the vessel")
        return send_result(data=marshal(vessel, DtoVessel.model))

    def update(self, object_id, data):
        vessel = Vessel.query.filter_by(vessel_id=object_id).first()
        if vessel is None:
            return send_error(message="Could not find the vessel")
        vessel = self._parse_vessel(data=data, vessel=vessel)
        db.session.commit()
        return send_result(data=marshal(vessel, DtoVessel.model))

    def delete(self, object_id):
        vessel = Vessel.query.filter_by(vessel_id=object_id).first()
        if vessel is None:
            return send_error(message="Could not find the vessel")
        db.session.delete(vessel)
        db.session.commit()
        return send_result(message='Vessel was deleted')

    def search_by_name(self, vessel_name):
        vessel = Vessel.query.filter_by(name=vessel_name).first()
        if vessel_name is None:
            return send_error("No vessel found")
        return send_result(data=marshal(vessel, DtoVessel.model))

    def search(self, args):
        if not isinstance(args, dict):
            return send_error(message="Please give the params to search")
        name, acronym = None, None
        if 'name' in args:
            name = args['name']
        if 'acronym' in args:
            acronym = args['acronym']
        query = db.session.query(Vessel)
        is_filter = False
        if name is not None and not str(name).strip().__eq__(''):
            query = query.filter(Vessel.name == name)
            is_filter = True
        if acronym is not None and not str(acronym).strip().__eq__(''):
            query = query.filter(Vessel.acronym == acronym)
            is_filter = True
        if is_filter:
            try:
                vessels = query.all()
                data = marshal(vessels, DtoVessel.model)
                return send_result(data=data)
            except Exception as e:
                print(e.__str__())
                return send_result(message="Could not find any result.")
        else:
            return send_result(message="Could not find any result.")

    def _parse_vessel(self, data, vessel=None):
        name, acronym, description, date_created = None, None, None, None
        if 'name' in data:
            name = data['name']
        if 'acronym' in data:
            acronym = data['acronym']
        if 'description' in data:
            description = data['description']
        if 'date_created' in data:
            try:
                date_created = datetime.datetime.fromisoformat(data['date_created'])
            except Exception as e:
                print(e.__str__())
                date_created = datetime.datetime.now()

        if vessel is None:
            vessel = Vessel(name=name, acronym=acronym, description=description, date_created=date_created)
        else:
            vessel.name = name
            vessel.acronym = acronym
            vessel.description = description
            vessel.date_created = date_created
        return vessel
