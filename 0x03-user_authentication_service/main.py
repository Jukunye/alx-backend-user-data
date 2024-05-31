#!/usr/bin/env python3
"""
User authentication testing module.
"""

import requests

BASE_URL = 'http://localhost:5000'

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def log_in(email: str, password: str) -> str:
    """
    Log in with the provided email and password.

    Args:
        email (str): The email address of the user.
        password (str): The password of the user.

    Returns:
        str: The session ID if login is successful.

    Raises:
        AssertionError: If the server does not return a 200 status code.
    """
    url = f'{BASE_URL}/sessions'
    response = requests.post(url, data={'email': email, 'password': password})
    assert response.status_code == 200
    return response.json()['message']


def register_user(email: str, password: str) -> None:
    """
    Register a new user with the given email and password.

    Args:
        email (str): The email address of the new user.
        password (str): The password for the new user.

    Raises:
        AssertionError: If the server does not return a 200 status code
                        or the message is not 'user created'.
    """
    url = f'{BASE_URL}/users'
    response = requests.post(url, data={'email': email, 'password': password})
    assert response.status_code == 200
    assert response.json()['message'] == 'user created'


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Logging in with the provided email and wrong password.

    Args:
        email (str): The email address of the user.
        password (str): The incorrect password.

    Raises:
        AssertionError: If the server does not return a 401 status code.
    """
    url = f'{BASE_URL}/sessions'
    response = requests.post(url, data={'email': email, 'password': password})
    assert response.status_code == 401


def profile_unlogged() -> None:
    """
    Access the profile page without logging in.

    Raises:
        AssertionError: If the server does not return a 403 status code.
    """
    url = f'{BASE_URL}/profile'
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Access the profile page while logged in.

    Args:
        session_id (str): The session ID of the logged-in user.

    Raises:
        AssertionError: If the server does not return a 200 status code.
    """
    url = f'{BASE_URL}/profile'
    cookies = {'session_id': session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """
    Log out the user with the provided session ID.

    Args:
        session_id (str): The session ID of the logged-in user.

    Raises:
        AssertionError: If the server does not return a 200 status code.
    """
    url = f'{BASE_URL}/sessions'
    headers = {'session_id': session_id}
    response = requests.delete(url, headers=headers)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Generate a reset password token for the user with the provided email.

    Args:
        email (str): The email address of the user.

    Returns:
        str: The reset password token.

    Raises:
        AssertionError: If the server does not return a 200 status code.
    """
    url = f'{BASE_URL}/reset_password_token'
    response = requests.post(url, data={'email': email})
    assert response.status_code == 200
    return response.json()['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update the password for the user with the provided email and reset token.

    Args:
        email (str): The email address of the user.
        reset_token (str): The reset token.
        new_password (str): The new password.

    Raises:
        AssertionError: If the server does not return a 200 status code or the
                        message is not 'Password updated'.
    """
    url = f'{BASE_URL}/reset_password'
    response = requests.put(url, data={
                            'email': email,
                            'reset_token': reset_token,
                            'new_password': new_password})
    assert response.status_code == 200
    assert response.json()['message'] == 'Password updated'


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
