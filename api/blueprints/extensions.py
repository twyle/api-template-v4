# -*- coding: utf-8 -*-
"""This module creates the flask extensions that we will use."""
import logging
import os

from flasgger import LazyString, Swagger
from flask import request
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
jwt = JWTManager()


def create_logger():
    """Create the application logger."""
    BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir))
    LOG_FILE = os.getenv('LOG_FILE_PATH') or os.path.join(BASE_DIR, 'app.log')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    flask_env = os.getenv('FLASK_ENV', 'development')

    if flask_env == 'development':
        logger.addHandler(stream_handler)

    return logger


app_logger = create_logger()

swagger_template = dict(
    info = {  # noqa: E251
        'title': LazyString(lambda: 'Flask API v4 Template.'),
        'version': LazyString(lambda: '0.1'),
        'description': LazyString(lambda: 'This document depicts documentation for the API v4 template.'),
    },
    host = LazyString(lambda: request.host)  # noqa: E251
)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'hello_world',
            "route": '/hello_world.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(template=swagger_template,
                  config=swagger_config)
