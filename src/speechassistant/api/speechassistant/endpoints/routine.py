from flask import request, Response
from flask_restx import Resource

from src.speechassistant.api.myapi import api
from src.speechassistant.api.speechassistant.logic.routine import *
from src.speechassistant.api.speechassistant.parser import routine_parser as parser

namespace = api.namespace('routine')


@namespace.route('/')
class RoutineConnection(Resource):

    def get(self) -> Response:
        data: dict = parser.parse_args(request)
        if 'name' not in data.keys():
            data = request.get_json()
        if 'name' not in data.keys():
            data['name'] = None
        return read_routine(data.get('name'))

    def post(self) -> Response:
        data: dict = request.get_json()
        print(data)
        return create_routine(data)

    def put(self) -> Response:
        data: dict = request.get_json()
        return update_routine(data)

    def delete(self) -> Response:
        data: dict = parser.parse_args(request)
        if 'name' not in data.keys():
            data = request.get_json()
        return delete_routine(data.get('name'))


@namespace.route('/onCommand')
class OnCommandConnection(Resource):
    def get(self) -> Response:
        data: dict = parser.parse_args(request)
        if 'id' not in data.keys():
            data = request.get_json()
        if 'name' not in data.keys():
            return Response('Missing argument "id"', status=500)
        read_on_command(data.get('id'))

    def post(self) -> Response:
        data: dict = request.get_json()
        if 'routine_name' not in data.keys() or 'on_command' not in data.keys():
            return Response('Missing argument "routine_name" or "on_command"', status=500)
        create_on_command(data.get('routine_name'), data.get('on_command'))

    def put(self) -> Response:
        data: dict = parser.parse_args(request)
        if 'id' not in data.keys():
            data = request.get_json()
        if 'id' not in data.keys():
            return Response('Missing argument "id"', status=500)
        return update_on_command(data.get('id'), data.get('on_command'))

    def delete(self) -> Response:
        data: dict = parser.parse_args(request)
        if 'id' not in data.keys():
            data = request.get_json()
        if 'id' not in data.keys():
            return Response('Missing argument "id"', status=500)
        return delete_on_command(data.get('id'))


@namespace.route('/commands')
class CommandsConnection(Resource):
    def get(self) -> Response:
        data: dict = parser.parse_args(request)
        if 'id' not in data.keys():
            data = request.get_json()
        if 'id' not in data.keys():
            data['id'] = None
        return read_routine_command(data.get('id'))

    def post(self) -> Response:
        data: dict = request.get_json()
        if 'routine_name' not in data.keys() or 'module_name' not in data.keys():
            return Response('Missing argument "routine_name" or "module_name"', status=500)
        if 'commands' not in data.keys():
            data['commands'] = None
        return create_routine_command(data.get('routine_name'), data.get('module_name'), data.get('commands'))

    def put(self) -> Response:
        data: dict = request.get_json()
        if 'routine_name' not in data.keys():
            return Response('Missing ID', status=500)
        return update_routine_command(data['id'], data['name'], data['commands'])

    def delete(self) -> Response:
        data: dict = parser.parse_args(request)
        if 'name' not in data.keys():
            data = request.get_json()
        return delete_routine_command(data.get('id'))


@namespace.route('/routineDates')
class RoutineDatesConnection(Resource):
    def get(self) -> Response:
        pass

    def post(self) -> Response:
        pass

    def put(self) -> Response:
        pass

    def delete(self) -> Response:
        pass


@namespace.route('/routineTimes')
class RoutineTimesConnection(Resource):
    def get(self) -> Response:
        pass

    def post(self) -> Response:
        pass

    def put(self) -> Response:
        pass

    def delete(self) -> Response:
        pass
