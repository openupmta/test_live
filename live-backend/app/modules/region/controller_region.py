import datetime

from flask_restplus import marshal
from app.modules.common.controller import Controller
from app.utils.response import send_error, send_result
from .region import Region
from .dto_region import DtoRegion
from app.app import db


class ControllerRegion(Controller):
    """
    Controller to manage all actions to region.
    """

    def create(self, data):
        region = self._parse_region(data=data, region=None)
        db.session.add(region)
        db.session.commit()
        return send_result(data=marshal(region, DtoRegion.model))

    def get(self):
        regions = Region.query.all()
        return send_result(data=marshal(regions, DtoRegion.model))

    def get_by_id(self, object_id):
        try:
            region = Region.query.filter_by(region_id=object_id).first()
            return send_result(data=marshal(region, DtoRegion.model))
        except Exception as e:
            print(e.__str__())
            return send_error(message="Could not find any result.")

    def get_by_name(self, region_name):
        if region_name is None or str(region_name).strip().__eq__(''):
            return send_error(message="Region name cannot be null or empty")
        regions = Region.query.filter_by(name=region_name).all()
        if regions is None:
            return send_error(message="Not found anything")
        return send_result(data=marshal(regions, DtoRegion.model))

    def get_by_acronym(self, acronym):
        if acronym is None or str(acronym).strip().__eq__(''):
            return send_error(message="Acronym cannot be null or empty")
        regions = Region.query.filter_by(acronym=acronym).all()
        if regions is None:
            return send_error(message="Not found anything")
        return send_result(data=marshal(regions, DtoRegion.model))

    def update(self, object_id, data):
        region = Region.query.filter_by(region_id=object_id)
        if region is None:
            return send_error(message="Region not found")
        else:
            region = self._parse_region(data=data, region=region)
            db.session.commit()
            return send_result(data=marshal(region, DtoRegion.model))

    def delete(self, object_id):
        try:
            region = Region.query.filter_by(region_id=object_id).first()
            if region is None:
                return send_error(message='Region not found')
            db.session.delete(region)
            db.session.commit()
            return send_result(message='Region ware deleted')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not delete region.')

    def search(self, args):
        if not isinstance(args, dict):
            return send_error(message="Please give the params to search")
        name, acronym = None, None
        if 'name' in args:
            name = args['name']
        if 'acronym' in args:
            acronym = args['acronym']
        query = db.session.query(Region)
        is_filter = False
        if name is not None and not str(name).strip().__eq__(''):
            query = query.filter(Region.name == name)
            is_filter = True
        if acronym is not None and not str(acronym).strip().__eq__(''):
            query = query.filter(Region.acronym == acronym)
            is_filter = True
        if is_filter:
            try:
                vessels = query.all()
                data = marshal(vessels, DtoRegion.model)
                return send_result(data=data)
            except Exception as e:
                print(e.__str__())
                return send_result(message="Could not find any result.")
        else:
            return send_result(message="Could not find any result.")

    def _parse_region(self, data, region=None):
        name, type, description, date_created = None, None, None, None
        if 'name' in data:
            name = data['name']
        if 'type' in data:
            type = data['type']
        if 'description' in data:
            description = data['description']
        if 'date_created' in data:
            try:
                date_created = datetime.datetime.fromisoformat(data['date_created'])
            except Exception as e:
                print(e.__str__())
                date_created = datetime.datetime.now()

        if region is None:
            region = Region(name=name, type=type, description=description, date_created=date_created)
        else:
            region.name = name
            region.type = type
            region.description = description
            region.date_created = date_created
        return region
