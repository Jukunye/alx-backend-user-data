#!/usr/bin/env python3
""" This module contains the Auth class"""
from flask import request
from typing import List, TypeVar

User = TypeVar('User')


class Auth:
    """
    A class for handling user authentication and authorization.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Template for all authentication system you will implement.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Template for all authentication system you will implement.
        """
        return None

    def current_user(self, request=None) -> User:
        """ Template for all authentication system you will implement.
        """
        return None
