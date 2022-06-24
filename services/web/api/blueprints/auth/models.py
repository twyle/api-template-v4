# -*- coding: utf-8 -*-
"""This module contains the database models used by the auth blueprint."""
from dataclasses import dataclass

from ..constants import EMAIL_MAX_LENGTH, NAME_MAX_LENGTH, PASSWORD_MAX_LENGTH
from ..extensions import db


@dataclass
class Admin(db.Model):
    """A class that represents an admin.

    Attributes
    ----------
    id: int
        The unique user identifier
    email: str
        The user's email
    name: str
        The admin user's name.
    password: str
        The Admin user's password.

    """

    __tablename__ = 'admins'

    id: int = db.Column(db.Integer, primary_key=True)
    email: str = db.Column(db.String(EMAIL_MAX_LENGTH), unique=True, nullable=False)
    name: str = db.Column(db.String(NAME_MAX_LENGTH), unique=True, nullable=False)
    password: str = db.Column(db.String(PASSWORD_MAX_LENGTH), nullable=False)

    def __init__(self, email: str, name: str, password: str) -> None:
        """Create a new admin.

        Creates a new amin in the admin table with an increasing id, with the
        given email, name and password.

        Attributes
        ----------
        email: str
            The user's email
        """
        self.email = email
        self.name = name
        self.password = password

    def get_admin(self) -> dict:
        """Get user data."""
        user = dict(id=self.id, email=self.email, name=self.name)
        return user
