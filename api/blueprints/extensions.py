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

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Template API V4",
        "description": "Template for creating Flask APIs.",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "email": "lyceokoth@gmail.com",
            "url": "www.twitter.com/lylethedesigner",
        },
        "termsOfService": "www.twitter.com/deve",
        "version": "1.0"
    },
    "host": LazyString(lambda: request.host),
    "basePath": "/",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "APIKeyHeader": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example:\"Authorization: Bearer {token}\""
        }
    },
}


swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(template=swagger_template,
                  config=swagger_config)
