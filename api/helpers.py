# -*- coding: utf-8 -*-
"""This module has methods that are used in the other modules in this package."""
import os

from sqlalchemy_utils import database_exists


def set_flask_environment(app) -> str:
    """Set the flask development environment.

    Parameters
    ----------
    app: flask.Flask
        The flask application object

    Raises
    ------
    KeyError
        If the FLASK_ENV environment variable is not set.

    Returns
    -------
    str:
        Flask operating environment i.e development

    """
    try:
        if os.environ['FLASK_ENV'] == 'production':  # pragma: no cover
            app.config.from_object('api.config.ProductionConfig')
        elif os.environ['FLASK_ENV'] == 'development':  # pragma: no cover
            app.config.from_object('api.config.DevelopmentConfig')
        elif os.environ['FLASK_ENV'] == 'test':
            app.config.from_object('api.config.TestingConfig')
        elif os.environ['FLASK_ENV'] == 'stage':
            app.config.from_object('api.config.StagingConfig')
    except KeyError:
        app.config.from_object('api.config.DevelopmentConfig')
        print('The FLASK_ENV is not set. Using development.')
        return 'development'

    return os.environ['FLASK_ENV']


def create_db_conn_string(flask_env: str) -> str:
    """Create the database connection string.

    Creates the database connection string for a given flask environment.

    Attributes
    ----------
    flask_env: str
        The Flask environment.

    Raises
    ------
    ValueError:
        If the flask_env is empty, is not a string or is any value apart from
        test, development, stage or production.

    Returns
    -------
    db_connection_string: str
        The database connection string
    """
    if not flask_env:
        raise ValueError('The flask_env cannot be a null value.')

    if not isinstance(flask_env, str):
        raise ValueError('The flask_env has to be string')

    if flask_env not in ['development', 'test', 'stage', 'production']:
        raise ValueError('The flask_env has to be test, development, stage or production.')

    POSTGRES_HOST = os.environ['POSTGRES_HOST']
    POSTGRES_PORT = os.environ['POSTGRES_PORT']
    POSTGRES_USER = os.environ['POSTGRES_USER']
    POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']

    if flask_env == 'development':
        POSTGRES_DB = f"{os.environ['POSTGRES_DB']}_dev"
    elif flask_env == 'test':
        POSTGRES_DB = f"{os.environ['POSTGRES_DB']}_test"
    elif flask_env == 'stage':
        POSTGRES_DB = f"{os.environ['POSTGRES_DB']}_stage"
    elif flask_env == 'production':
        POSTGRES_DB = f"{os.environ['POSTGRES_DB']}_prod"
    else:
        POSTGRES_DB = f"{os.environ['POSTGRES_DB']}_dev"

    return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


def check_if_database_exists(db_connection_string: str) -> bool:
    """Check if database exists.

    Ensures that the database exists before starting the application.

    Attributes
    ----------
    db_connection: str
        The database URL

    Raises
    ------
    ValueError:
        If the db_connection_string is empty or is not a string.

    Returns
    -------
    db_exists: bool
        True if database exists or False if it does not
    """
    if not db_connection_string:
        raise ValueError('The db_connection_string cannot be a null value.')

    if not isinstance(db_connection_string, str):
        raise ValueError('The db_connection_string has to be string')

    db_exists = database_exists(db_connection_string)

    return db_exists


def are_environment_variables_set() -> bool:  # pylint: disable=R0911, R0915
    """Check if all the environment variables are set.

    Raises
    ------
    KeyError
        If any of the environment variables are not set.

    Returns
    -------
    bool:
        True if all the environment variables are set else False if any is missing.

    """
    try:
        os.environ['FLASK_APP']  # pylint: disable=W0104
        print('The FLASK_APP is set')
    except KeyError:
        print('The FLASK_APP is not set')
        return False

    try:
        os.environ['FLASK_ENV']  # pylint: disable=W0104
        print('The FLASK_ENV is set')
    except KeyError:
        print('The FLASK_ENV is not set')
        return False

    try:
        os.environ['SECRET_KEY']  # pylint: disable=W0104
        print('The SECRET_KEY is set')
    except KeyError:
        print('The SECRET_KEY is not set')
        return False

    try:
        os.environ['POSTGRES_HOST']  # pylint: disable=W0104
        print('The POSTGRES_HOST is set')
    except KeyError:
        print('The POSTGRES_HOST is not set')
        return False

    try:
        os.environ['POSTGRES_DB']  # pylint: disable=W0104
        print('The POSTGRES_DB is set')
    except KeyError:
        print('The POSTGRES_DB is not set')
        return False

    try:
        os.environ['POSTGRES_PORT']  # pylint: disable=W0104
        print('The POSTGRES_PORT is set')
    except KeyError:
        print('The POSTGRES_PORT is not set')
        return False

    try:
        os.environ['POSTGRES_USER']  # pylint: disable=W0104
        print('The POSTGRES_USER is set')
    except KeyError:
        print('The POSTGRES_USER is not set')
        return False

    try:
        os.environ['POSTGRES_PASSWORD']  # pylint: disable=W0104
        print('The POSTGRES_PASSWORD is set')
    except KeyError:
        print('The POSTGRES_PASSWORD is not set')
        return False

    try:
        db_con_str = create_db_conn_string(os.environ['FLASK_ENV'])
        db_exists = check_if_database_exists(db_con_str)

        if db_exists:
            print(f'The database {db_con_str} exists.')
            return True

        print(f'The database {db_con_str} does not exist.')
        return False

    except ValueError as v:
        print(v)
        print('Unable to verify database existence...')
        return False
