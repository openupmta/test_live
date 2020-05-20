import datetime
from app.modules.common.controller import Controller
from .port import Port
from .dto_port import DtoPort
from app.app import db
from app.utils.response import send_result, send_error
from flask_restplus import marshal


class ControllerPort(Controller):

    def create(self, data):
        port = self._parse_port(data=data, port=None)
        db.session.add(port)
        db.session.commit()
        return send_result(data=marshal(port, DtoPort.model))

    def get(self):
        ports = Port.query.all()
        data = marshal(ports, DtoPort.model)
        return send_result(data=data)

    def get_by_id(self, object_id):
        port = Port.query.filter_by(port_id=object_id).first()
        return send_result(data=marshal(port, DtoPort.model))

    def update(self, object_id, data):
        port = Port.query.filter_by(port_id=object_id).first()
        if port is None:
            return send_error(message='Port not found')
        else:
            port = self._parse_port(data=data, port=port)
            db.session.commit()
            return send_result(data=marshal(port, DtoPort.model))

    def delete(self, object_id):
        try:
            port = Port.query.filter_by(port_id=object_id).first()
            if port is None:
                return send_error(message='Port not found')  # False  # send_error(message='User not found')
            else:
                db.session.delete(port)
                db.session.commit()
                return send_result(
                    message='Port was deleted')  # True  # send_result(message='Delete user successfully')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not delete port')  # False  # send_error(message=e)

    def get_port_by_name(self, name):
        if name is None or str(name).strip().__eq__(''):
            return send_error(message='Port name cannot be null or empty')
        port = Port.query.filter_by(name=name).first()
        if port is None:
            return send_error(message="Not found anything according to your request")
        return send_result(data=marshal(port, DtoPort.model))

    def search_port_by_name(self, name):
        if name is None or str(name).strip().__eq__(''):
            return None
        try:
            port = Port.query.filter_by(name=name).first()
            return port
        except Exception as e:
            print(e.__str__())
            return None

    def search(self, args):
        if not isinstance(args, dict):
            return send_error(message="Please enter the params")
        name, port_type = None, None
        if 'name' in args:
            name = args['name']
        if 'type' in args:
            port_type = args['type']
        query = db.session.query(Port)
        is_filter = False
        if name is not None and not str(name).strip().__eq__(''):
            query = query.filter(Port.name == name)
            is_filter = True
        if port_type is not None and not str(port_type).strip().__eq__(''):
            query = query.filter(Port.type == port_type)
            is_filter = True
        if is_filter:
            ports = query.all()
            data = marshal(ports, DtoPort.model)
            return send_result(data=data)
        else:
            return send_result(message='Could not find any result')

    def _parse_port(self, data, port=None):
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

        if port is None:
            port = Port(name=name, type=type, description=description, date_created=date_created)
        else:
            port.name = name
            port.type = type
            port.description = description
            port.date_created = date_created
        return port
