#!/usr/bin/env python3
""" This module contains the BasicAuth class"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import TypeVar, Optional
from models.user import User as usr

User = TypeVar('User')


class BasicAuth(Auth):
    """ class BasicAuth that inherits from Auth """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ returns the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if authorization_header.startswith('Basic '):
            return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes Base64 authorization header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            return b64decode(base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extracts the user email and password from the Base64 decoded value
        """
        if not decoded_base64_authorization_header:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        try:
            email, password = decoded_base64_authorization_header.split(':', 1)
            return email, password
        except ValueError:
            return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> Optional[User]:
        """Returns the User instance based on the provided email and password
        """

        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        try:
            users = usr.search({'email': user_email})

            for user in users:
                if user.is_valid_password(user_pwd):
                    return user

        except Exception:
            pass

        return None

    def current_user(self, request=None) -> User:
        """Retrieves the User instance for a request using Basic Authentication
        """

        if request is None:
            return None

        auth_header = self.authorization_header(request)

        base64_auth_header = \
            self.extract_base64_authorization_header(auth_header)

        decoded_auth_header = \
            self.decode_base64_authorization_header(base64_auth_header)

        user_email, user_pwd = \
            self.extract_user_credentials(decoded_auth_header)

        user = self.user_object_from_credentials(user_email, user_pwd)

        return user
