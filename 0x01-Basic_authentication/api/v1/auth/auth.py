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
        """ Determine whether the given request path requires authentication.
        """
        if path is None:
            return True
        if not excluded_paths:
            return True
        for pattern in excluded_paths:
            if pattern.endswith('*'):
                if path.startswith(pattern[:-1]):
                    return False
            elif pattern == path or pattern == f'{path}/':
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """  Validate all requests to secure the API
        """
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None
        return auth_header

    def current_user(self, request=None) -> User:
        """ Template for all authentication system you will implement.
        """
        return None
