#!/usr/bin/env python3
"""
This module contains _hash_password method
"""
import uuid
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


def _generate_uuid() -> str:
    """
    Generate a Universal Unique Identifier
    """
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """
        Handle login attempts
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except Exception as e:
            pass

        return False

    def create_session(self, email: str) -> str:
        """
        Creating a new session for a user logging into the system
        """
        session_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = session_id
            self._db._session.commit()
            return session_id
        except Exception as e:
            pass

    def get_user_from_session_id(self, session_id: str) -> str:
        """
        Retrieving user information based on a provided session ID
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: str) -> None:
        """
        Logging out a user by destroying their session
        """

        if user_id is None:
            return None

        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """method to generate a reset password token for user
        Args:  email address of the user
        Returns: generated reset password token."""

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None

        if user is None:
            raise ValueError()

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates user password corresponding to reset token
        """
        if reset_token is None or password is None:
            return None

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_password = _hash_password(password)
        self._db.update_user(user.id,
                             hashed_password=hashed_password, reset_token=None)
