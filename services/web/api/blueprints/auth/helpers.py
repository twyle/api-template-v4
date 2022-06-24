# -*- coding: utf-8 -*-
"""This module has methods that are used in the other modules in this package."""
import re

from flask import jsonify

from ..constants import (
    EMAIL_MAX_LENGTH,
    NAME_MAX_LENGTH,
    NAME_MIN_LENGTH,
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
)
from ..exceptions import (
    AdminDoesNotExists,
    AdminExists,
    AdminNameTooLong,
    AdminNameTooShort,
    AdminPasswordNotAlphaNumeric,
    AdminPasswordTooLong,
    AdminPaswordTooShort,
    EmailAddressTooLong,
    EmptyAdminData,
    InvalidEmailAddressFormat,
    MissingEmailData,
    MissingEmailKey,
    MissingNameData,
    MissingNameKey,
    MissingPasswordData,
    MissingPasswordKey,
    NonDictionaryAdminData,
    NonStringData,
)
from ..extensions import app_logger, db
from .models import Admin


def check_if_admin_exists_with_id(admin_id: int) -> bool:
    """Check if the admin with the given admin_id exists."""
    if not admin_id:
        msg = 'When checking if admin exists using their id, the admin_id was null.'
        app_logger.exception(msg)
        raise ValueError('The admin_id has to be provided.')

    if not isinstance(admin_id, int):
        msg = 'When checking if admin exists using their id, the admin_id was not an integer.'
        app_logger.exception(msg)
        raise ValueError('The admin_id has to be an integer')

    admin = Admin.query.filter_by(id=admin_id).first()

    if admin:
        return True

    return False


def check_if_admin_exists(admin_email: str) -> bool:
    """Check if the admin with the given admin_email exists."""
    if not admin_email:
        msg = 'When checking if admin exists using their email, the admin_email was null.'
        app_logger.exception(msg)
        raise ValueError('The admin_email has to be provided.')

    if not isinstance(admin_email, str):
        msg = 'When checking if admin exists using their email, the admin_email was not a string.'
        app_logger.exception(msg)
        raise ValueError('The admin_email has to be an integer')

    admin = Admin.query.filter_by(email=admin_email).first()

    if admin:
        return True

    return False


def check_if_admin_with_name_exists(admin_name: str) -> bool:
    """Check if the admin with the given admin_name exists."""
    if not admin_name:
        msg = 'When checking if admin exists using their name, the admin_name was null.'
        app_logger.exception(msg)
        raise ValueError('The admin_name has to be provided.')

    if not isinstance(admin_name, str):
        msg = 'When checking if admin exists using their name, the admin_name was not a string.'
        app_logger.exception(msg)
        raise ValueError('The admin_name has to be string')

    admin = Admin.query.filter_by(name=admin_name).first()

    if admin:
        return True

    return False


def is_email_address_format_valid(email_address: str) -> bool:
    """Check that the email address format is valid."""
    if not email_address:
        msg = 'When checking if an email address format is valid, the admin_email was null.'
        app_logger.exception(msg)
        raise ValueError('The email_address cannot be an empty value')

    if not isinstance(email_address, str):
        msg = 'When checking if an email address format is valid, the admin_email was not a string.'
        app_logger.exception(msg)
        raise ValueError('The email_address must be a string')

    #  Regular expression for validating an Email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if re.fullmatch(regex, email_address):
        return True

    return False


def is_admin_name_valid(admin_name: str) -> bool:
    """Check if the admin name is valid."""
    if not admin_name:
        msg = 'When checking if admin_name is valid, the admin_name was null.'
        app_logger.exception(msg)
        raise ValueError('The admin_name has to be provided.')

    if not isinstance(admin_name, str):
        msg = 'When checking if admin_name is valid, the admin_name was not a string.'
        app_logger.exception(msg)
        raise ValueError('The admin_name has to be string')

    if len(admin_name) >= NAME_MAX_LENGTH:
        msg = 'When checking if admin_name is valid, the admin_name was too long.'
        app_logger.exception(msg)
        raise AdminNameTooLong(f'The admin_name has to be less than {NAME_MAX_LENGTH}')

    if len(admin_name) <= NAME_MIN_LENGTH:
        msg = 'When checking if admin_name is valid, the admin_name was too short.'
        app_logger.exception(msg)
        raise AdminNameTooShort(f'The admin_name has to be more than {NAME_MIN_LENGTH}')

    if not admin_name.isalnum():
        msg = 'When checking if admin_name is valid, he admin_name was not alphanumeric.'
        app_logger.exception(msg)
        raise ValueError('The admin_name has to be alphanumeric.')

    return True


def is_admin_password_valid(admin_password: str):
    """Check if the admin_password is valid."""
    if not admin_password:
        msg = 'When checking if admin_password is valid, the admin_password was null.'
        app_logger.exception(msg)
        raise MissingPasswordData('The admin_password has to be provided.')

    if not isinstance(admin_password, str):
        msg = 'When checking if admin_password is valid, the admin_password was not a string.'
        app_logger.exception(msg)
        raise NonStringData('The admin_password has to be string')

    if len(admin_password) >= PASSWORD_MAX_LENGTH:
        msg = 'When checking if admin_password is valid, the admin_password was too long.'
        app_logger.exception(msg)
        raise AdminPasswordTooLong(f'The admin_password has to be less than {PASSWORD_MAX_LENGTH}')

    if len(admin_password) <= PASSWORD_MIN_LENGTH:
        msg = 'When checking if admin_password is valid, the admin_password was too short.'
        app_logger.exception(msg)
        raise AdminPaswordTooShort(f'The admin_password has to be more than {PASSWORD_MIN_LENGTH}')

    if admin_password.isalnum():
        msg = 'When checking if admin_password is valid, he admin_password was not alphanumeric.'
        app_logger.exception(msg)
        raise AdminPasswordNotAlphaNumeric('The admin_password has to be alphanumeric.')

    return True


def create_new_admin(admin_data: dict) -> dict:  # pylint: disable=R0912
    """Create a new admin."""
    if not admin_data:
        app_logger.exception('When creating a new admin, the admin_data was empty.')
        raise EmptyAdminData('The admin data cannot be empty.')

    if not isinstance(admin_data, dict):
        app_logger.exception('When creating a new admin, the admin_data was nota dictionary.')
        raise NonDictionaryAdminData('admin_data must be a dict')

    if 'email' not in admin_data.keys():
        app_logger.exception('When creating a new admin, the email key was missing from the admin_data.')
        raise MissingEmailKey('The email is missing from the admin data')

    if not admin_data['email']:
        app_logger.exception('When creating a new admin, the email data was missing from the admin_data.')
        raise MissingEmailData('The email data is missing')

    if len(admin_data['email']) >= EMAIL_MAX_LENGTH:
        app_logger.exception(f'When creating a new admin, the email key was longer than {EMAIL_MAX_LENGTH}.')
        raise EmailAddressTooLong(f'The email address should be less than {EMAIL_MAX_LENGTH} characters!')

    if not is_email_address_format_valid(admin_data['email']):
        app_logger.exception('When creating a new admin, the email address format was invalid.')
        raise InvalidEmailAddressFormat('The email address is invalid')

    if 'name' not in admin_data.keys():
        app_logger.exception('When creating a new admin, the name key was missing from the admin_data.')
        raise MissingNameKey('The name is missing from the admin data')

    if not admin_data['name']:
        app_logger.exception('When creating a new admin, the name data was missing from the admin_data.')
        raise MissingNameData('The name data is missing')

    if 'password' not in admin_data.keys():
        app_logger.exception('When creating a new admin, the password key was missing from the admin_data.')
        raise MissingPasswordKey('The password is missing from the admin data')

    if not admin_data['password']:
        app_logger.exception('When creating a new admin, the password data was missing from the admin_data.')
        raise MissingPasswordData('The password data is missing')

    is_admin_name_valid(admin_data['name'])

    try:
        is_admin_password_valid(admin_data['password'])
    except ValueError as e:
        raise e

    if check_if_admin_exists(admin_data['email']):
        app_logger.exception('When creating a new admin, the admin was found to already exist.')
        raise AdminExists(f'The email adress {admin_data["email"]} is already in use.')

    if check_if_admin_with_name_exists(admin_data['name']):
        app_logger.exception('When creating a new admin, the admin was found to already exist.')
        raise AdminExists(f'The name {admin_data["name"]} is already in use.')

    admin = Admin(email=admin_data['email'], name=admin_data['name'],
                  password=admin_data['password'])

    db.session.add(admin)
    db.session.commit()

    return admin.get_admin()


def handle_create_admin(request_data: dict):  # pylint: disable=R0911, R0912, R0915
    """Handle the POST request to the /admin route."""
    try:
        new_admin = create_new_admin(request_data)
    except EmptyAdminData as e:
        app_logger.error("When handling a get request to create a new admin, the admin passed in no data.")
        app_logger.exception(e)
        return jsonify({'error': str(e)}), 400
    except NonDictionaryAdminData as e:
        app_logger.error("When handling a get request to create a new admin, the admin passed in non-dictionary data.")
        app_logger.exception(e)
        return jsonify({'error': str(e)}), 400
    except MissingEmailKey as e:
        msg = "When handling a get request to create a new admin, the admin passed in data with no email key."
        app_logger.error(msg)
        app_logger.exception(e)
        return jsonify({'error': str(e)}), 400
    except MissingNameKey as e:
        msg = "When handling a get request to create a new admin, the admin passed in data with no name key."
        app_logger.error(msg)
        app_logger.exception(e)
        return jsonify({'error': str(e)}), 400
    except MissingPasswordKey as e:
        msg = "When handling a get request to create a new admin, the admin passed in data with no password key."
        app_logger.error(msg)
        app_logger.exception(e)
        return jsonify({'error': str(e)}), 400
    except EmailAddressTooLong as e:
        app_logger.error("When handling a get request to create a new admin, the email was too long.")
        app_logger.exception(e)
        return jsonify({'error': str(e)}), 400
    except InvalidEmailAddressFormat as e:
        app_logger.error("When handling a get request to create a new admin, the email address was invalid.")
        app_logger.exception(e)
        return jsonify({'error': str(e)}), 400
    except AdminExists as e:
        app_logger.error("When handling a get request to create a new admin, the admin alredy exists.")
        app_logger.exception(e)
        return jsonify({'error': str(e)}), 409
    except MissingEmailData as e:
        app_logger.error("When handling a get request to create a new admin, the email data was missing.")
        app_logger.exception(e)
        return jsonify({'error': str(e)}), 400
    except MissingNameData as e:
        app_logger.error("When handling a get request to create a new admin, the name data was missing.")
        app_logger.exception(e)
        return jsonify({'error': str(e)}), 400
    except MissingPasswordData as e:
        app_logger.error("When handling a get request to create a new admin, the password data was missing.")
        app_logger.exception(e)
        return jsonify({'error': str(e)}), 400
    except AdminNameTooLong as e:
        app_logger.error("When handling a get request to create a new admin, the name was too long.")
        app_logger.exception(e)
        return jsonify({'error': str(e)}), 400
    except AdminNameTooShort as e:
        app_logger.error("When handling a get request to create a new admin, the name was too short.")
        app_logger.exception(e)
        return jsonify({'error': str(e)}), 400
    except AdminPaswordTooShort as e:
        app_logger.error("When handling a get request to create a new admin, the password was too short.")
        app_logger.exception(e)
        return jsonify({'error': str(e)}), 400
    except AdminPasswordTooLong as e:
        app_logger.error("When handling a get request to create a new admin, the password was too long.")
        app_logger.exception(e)
        return jsonify({'error': str(e)}), 400
    except AdminPasswordNotAlphaNumeric as e:
        app_logger.error("When handling a get request to create a new admin, the password was not alphanumeric.")
        app_logger.exception(e)
        return jsonify({'error': str(e)}), 400
    else:
        return new_admin, 201


def get_admin(admin_id: int) -> dict:
    """Get the admin with the given id."""
    if not admin_id:
        raise EmptyAdminData('The admin_id has to be provided.')

    if not isinstance(admin_id, int):
        raise ValueError('The admin_id has to be an integer.')

    if not check_if_admin_exists_with_id(admin_id):
        raise AdminDoesNotExists(f'The admin with id {admin_id} does not exist.')

    admin = Admin.query.filter_by(id=admin_id).first()

    return admin.get_admin()


def handle_get_admin(admin_id: int):
    """Handle the GET request to the /admin route."""
    try:
        admin = get_admin(admin_id)
    except AdminDoesNotExists as e:
        print(e)
        return str(e), 404
    except EmptyAdminData as e:
        print(e)
        return str(e), 400
    except ValueError as e:
        print(e)
        return str(e), 400
    else:
        return admin, 200


def delete_admin(admin_id: int) -> dict:
    """Delete the admin with the given id."""
    if not admin_id:
        raise EmptyAdminData('The admin_id has to be provided.')

    if not isinstance(admin_id, int):
        raise ValueError('The admin_id has to be an integer.')

    if not check_if_admin_exists_with_id(admin_id):
        raise AdminDoesNotExists(f'The admin with id {admin_id} does not exist.')

    admin = Admin.query.filter_by(id=admin_id).first()
    db.session.delete(admin)
    db.session.commit()

    return admin.get_admin()


def handle_delete_admin(admin_id: int):
    """Handle the DELETE request to the /admin route."""
    try:
        admin = delete_admin(admin_id)
    except AdminDoesNotExists as e:
        print(e)
        return str(e), 404
    except EmptyAdminData as e:
        print(e)
        return str(e), 400
    except ValueError as e:
        print(e)
        return str(e), 400
    else:
        return admin, 200


def update_admin(admin_id: int, admin_data: dict) -> dict:  # pylint: disable=R0912
    """Update the admin with the given id."""
    if not admin_id:
        raise EmptyAdminData('The admin_id has to be provided.')

    if not isinstance(admin_id, int):
        raise ValueError('The admin_id has to be an integer.')

    if not check_if_admin_exists_with_id(admin_id):
        raise AdminDoesNotExists(f'The admin with id {admin_id} does not exist.')

    if not admin_data:
        raise EmptyAdminData('The admin data cannot be empty.')

    if not isinstance(admin_data, dict):
        raise NonDictionaryAdminData('admin_data must be a dict')

    for key in admin_data.keys():
        valid_keys = ['name', 'email', 'password']
        if key not in valid_keys:
            raise KeyError(f'Invalid key {key}. The valid keys are {valid_keys}.')

    if 'email' in admin_data.keys():
        is_email_address_format_valid(admin_data['email'])

        if len(admin_data['email']) >= EMAIL_MAX_LENGTH:
            raise EmailAddressTooLong('The email address is too long')

        if check_if_admin_exists(admin_data['email']):
            raise AdminExists(f'The email adress {admin_data["email"]} is already in use.')

    if 'password' in admin_data.keys():
        is_admin_password_valid(admin_data['password'])

    if 'name' in admin_data.keys():
        is_admin_name_valid(admin_data['name'])
        if check_if_admin_with_name_exists(admin_data['name']):
            raise AdminExists(f'The name {admin_data["name"]} is already in use.')

    admin = Admin.query.filter_by(id=admin_id).first()
    if 'email' in admin_data.keys():
        admin.email = admin_data['email']
    if 'password' in admin_data.keys():
        admin.password = admin_data['password']
    if 'name' in admin_data.keys():
        admin.name = admin_data['name']
    db.session.commit()

    return admin.get_admin()


def handle_update_admin(admin_id: int, admin_data: dict):  # pylint: disable=R0911,R0912
    """Handle the GET request to the /admin route."""
    try:
        admin = update_admin(admin_id, admin_data)
    except AdminDoesNotExists as e:
        print(e)
        return str(e), 404
    except EmptyAdminData as e:
        print(e)
        return str(e), 400
    except ValueError as e:
        print(e)
        return str(e), 400
    except NonDictionaryAdminData as e:
        print(e)
        return str(e), 400
    except MissingEmailKey as e:
        print(e)
        return str(e), 400
    except MissingNameKey as e:
        print(e)
        return str(e), 400
    except MissingPasswordKey as e:
        print(e)
        return str(e), 400
    except MissingEmailData as e:
        print(e)
        return str(e), 400
    except MissingNameData as e:
        print(e)
        return str(e), 400
    except MissingPasswordData as e:
        print(e)
        return str(e), 400
    except EmailAddressTooLong as e:
        print(e)
        return str(e), 400
    except AdminNameTooLong as e:
        print(e)
        return str(e), 400
    except AdminNameTooShort as e:
        print(e)
        return str(e), 400
    except InvalidEmailAddressFormat as e:
        print(e)
        return str(e), 400
    except AdminExists as e:
        print(e)
        return str(e), 400
    else:
        return admin, 200
