#!/usr/bin/env python3
"""
This module contains _hash_password method
"""
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Securely hashing a user's password

    Returns:
        salted hash of the input password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register new users

        Args:
            email (str): user's email
            password (str): user's password

        Returns:
            User object
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
