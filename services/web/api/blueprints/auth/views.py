# -*- coding: utf-8 -*-
"""This module contains the routes associated with the auth Blueprint."""
from json import JSONDecodeError

from api.blueprints.auth.models import Admin
from flasgger import swag_from
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from ..extensions import app_logger
from .helpers import handle_create_admin, handle_get_admin, handle_log_in_admin, handle_update_admin

auth = Blueprint('auth', __name__, template_folder='templates',
                 static_folder='static', url_prefix='/auth')


@auth.route('/register', methods=['POST'])
@swag_from("./docs/register_admin.yml", endpoint='auth.register', methods=['POST'])
def register():
    """Create a new Admin User."""
    try:
        data = request.json
    except JSONDecodeError as e:
        print(e)
        return str(e), 400
    else:
        return handle_create_admin(data)


@auth.route('/login', methods=['POST'])
@swag_from("./docs/login_admin.yml", endpoint='auth.login', methods=['POST'])
def login():
    """Log in a registered Admin."""
    try:
        data = request.json
    except JSONDecodeError as e:
        print(e)
        return str(e), 400
    else:
        return handle_log_in_admin(data)


@auth.route("/refresh", methods=["GET"])
@jwt_required(refresh=True)
@swag_from("./docs/refresh_token.yml", endpoint='auth.refresh', methods=['GET'])
def refresh():
    """Generate a refresh token."""
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token), 200


@auth.route('/me', methods=['GET'])
@jwt_required()
@swag_from("./docs/get_admin.yml", endpoint='auth.get_admin', methods=['GET'])
def get_admin():
    """Get admin details."""
    app_logger.info("Handling a GET request to '/auth/me' route.")
    admin_id = get_jwt_identity()
    app_logger.info(f"GET request succeessful. Returning user with id {admin_id}.")
    return handle_get_admin(admin_id)


@auth.route('/me', methods=['PUT'])
@jwt_required()
@swag_from("./docs/update_admin.yml", endpoint='auth.update_admin', methods=['PUT'])
def update_admin():
    """Update admin details."""
    try:
        data = request.json
        admin_id = get_jwt_identity()
    except JSONDecodeError as e:
        print(e)
        return str(e), 400
    else:
        return handle_update_admin(admin_id, data)


@auth.route('/me', methods=['DELETE'])
@jwt_required()
@swag_from("./docs/delete_admin.yml", endpoint='auth.delete_admin', methods=['DELETE'])
def delete_admin():
    """Delete admin details."""
    app_logger.info("Successfully deleted the admin data.")
    return jsonify({'hello': 'from template api'}), 200


@auth.route('/admins', methods=['GET'])
@swag_from("./docs/get_all_admins.yml", endpoint='auth.get_all_admins', methods=['GET'])
def get_all_admins():
    """Get all admins."""
    admins = Admin.query.all(), 200
    app_logger.info("Successfully handled a GET request to the '/admins' route. Returning all the admins.")
    return jsonify(admins), 200
