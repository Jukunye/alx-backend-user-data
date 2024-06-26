#!/usr/bin/env python3
""" Module of Session authentication views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from os import getenv
from typing import Tuple


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """ POST /api/v1/users/
    reques body:
      - email
      - password
    Return:
      - User object JSON represented
      - 400 if missing User
    """

    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    users = None

    try:
        users = User.search({'email': email})

        for user in users:
            if user.is_valid_password(password):
                from api.v1.app import auth
                session_id = auth.create_session(user.id)
                response = jsonify(user.to_json())
                session_name = getenv('SESSION_NAME')
                response.set_cookie(session_name, session_id)
                return response
        return jsonify({"error": "wrong password"}), 401

    except Exception:
        pass

    if users is None or users == []:
        return jsonify({"error": "no user found for this email"}), 404


@app_views.route('aut_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """Handle user logout"""
    from api.v1.app import auth
    destroy = auth.destroy_session(request)
    if destroy is False:
        abort(404)

    return jsonify({}), 200
