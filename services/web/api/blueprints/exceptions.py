# -*- coding: utf-8 -*-
"""This module has exceptions that are used in the other modules in this package."""


class EmptyUserData(Exception):
    """Raised when no user data is provided."""


class NonStringData(Exception):
    """Raised when the data provided is not string."""


class EmptyAdminData(Exception):
    """Raised when no admin data is provided."""


class NonDictionaryUserData(Exception):
    """Raised when the user data is not provided in a dictionary."""


class NonDictionaryAdminData(Exception):
    """Raised when the admin data is not provided in a dictionary."""


class MissingEmailKey(Exception):
    """Raised when the 'email' key is missing in user data."""


class MissingNameKey(Exception):
    """Raised when the 'name' key is missing in user data."""


class MissingPasswordKey(Exception):
    """Raised when the 'password' key is missing in user data."""


class MissingEmailData(Exception):
    """Raised when the email is empty in user data."""


class MissingNameData(Exception):
    """Raised when the name is empty in user data."""


class MissingPasswordData(Exception):
    """Raised when the password is empty in user data."""


class EmailAddressTooLong(Exception):
    """Raised when the provided email address is too long."""


class InvalidEmailAddressFormat(Exception):
    """Raised when the email address format is invalid."""


class UserExists(Exception):
    """Raised when the given user exists."""


class AdminExists(Exception):
    """Raised when the given admin exists."""


class UserDoesNotExists(Exception):
    """Raised when the given user does not exist."""


class AdminDoesNotExists(Exception):
    """Raised when the given admin does not exist."""


class AdminNameTooShort(Exception):
    """Raised when the given admin name is too short."""


class AdminNameTooLong(Exception):
    """Raised when the given admin name is too long."""


class AdminPaswordTooShort(Exception):
    """Raised when the given admin password is too short."""


class AdminPasswordTooLong(Exception):
    """Raised when the given admin password is too long."""


class AdminPasswordNotAlphaNumeric(Exception):
    """Raised when the given admin password is not alphanumeric."""


class InvalidAdminPassword(Exception):
    """Raised when an invalid admin password is given."""
