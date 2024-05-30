#!/usr/bin/env python3
"""
This module contains _hash_password method
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Securely hashing a user's password

    Returns:
        salted hash of the input password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
