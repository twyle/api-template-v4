# -*- coding: utf-8 -*-
"""This module contains the routes associated with the default Blueprint."""
from json import JSONDecodeError

from flasgger import swag_from
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..auth.helpers import get_admin
from ..extensions import app_logger
from .helpers import handle_create_user, handle_delete_user, handle_get_user, handle_update_user
from .models import User

default = Blueprint('default', __name__, template_folder='templates', static_folder='static')


@default.route('/', methods=['GET'])
@swag_from("./docs/home.yml", endpoint='default.home', methods=['GET'])
def home():
    """Confirm that the application is working."""
    app_logger.info("Successfully handled a GET request to the '/' route. Returning the default message.")
    return jsonify({'hello': 'from template api'}), 200


@default.route('/user', methods=['POST'])
@jwt_required()
@swag_from("./docs/create_user.yml", endpoint='default.create_user', methods=['POST'])
def create_user():
    """Create a new user."""
    try:
        data = request.json
        admin_id = get_jwt_identity()
        admin = get_admin(admin_id)
    except JSONDecodeError as e:
        print(e)
        return str(e), 400
    else:
        app_logger.info(f'The admin {admin["name"]} created a new user with email {data["email"]}.')
        return handle_create_user(data)


@default.route('/user', methods=['GET'])
@jwt_required()
@swag_from("./docs/get_user.yml", endpoint='default.get_user', methods=['GET'])
def get_user():
    """Get a user with the given id."""
    app_logger.info("Handling a GET request to '/user' route.")
    try:
        user_id = int(request.args.get('id'))
        admin_id = get_jwt_identity()
        admin = get_admin(admin_id)
    except TypeError as e:
        app_logger.exception(e)
        app_logger.error('GET request unsuccessful. This error is cause by not supplying the user id')
        return 'The user id was not provided or the id is invalid type.', 400
    except ValueError as e:
        app_logger.exception(e)
        app_logger.error('GET request unsuccessful. This error is cause by not supplying the user id')
        return 'The user id was not provided or the id is invalid.', 400
    else:
        app_logger.info(f"The admin {admin['name']} retrieved a user with id {user_id}.")
        return handle_get_user(user_id)


@default.route('/user', methods=['PUT'])
@jwt_required()
@swag_from("./docs/update_user.yml", endpoint='default.update_user', methods=['PUT'])
def update_user():
    """Update user details."""
    try:
        data = request.json
        user_id = int(request.args.get('id'))
        admin_id = get_jwt_identity()
        admin = get_admin(admin_id)
    except JSONDecodeError as e:
        print(e)
        return str(e), 400
    except ValueError as e:
        print(e)
        print('This error is cause by not supplying the user id')
        return 'The user id was not provided', 400
    else:
        app_logger.info(f"The admin {admin['name']} updated a user with id {user_id} with data: {data}.")
        return handle_update_user(user_id, data)


@default.route('/user', methods=['DELETE'])
@jwt_required()
@swag_from("./docs/delete_user.yml", endpoint='default.delete_user', methods=['DELETE'])
def delete_user():
    """Delete a user."""
    try:
        user_id = int(request.args.get('id'))
        admin_id = get_jwt_identity()
        admin = get_admin(admin_id)
    except ValueError as e:
        print(e)
        print('This error is cause by not supplying the user id')
        return 'The user id was not provided', 400
    else:
        app_logger.info(f"The admin {admin['name']} deleted a user with id {user_id}.")
        return handle_delete_user(user_id)


@default.route('/users', methods=['GET'])
@swag_from("./docs/get_all_users.yml", endpoint='default.all_users', methods=['GET'])
def all_users():
    """Get all the users."""
    app_logger.info("Handling a GET request to '/users' route.")
    users = User.query.all()
    app_logger.info("Successfully handled a GET request to the '/users' route. Returning all the users.")
    return jsonify(users), 200
