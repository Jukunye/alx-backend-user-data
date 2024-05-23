#!/usr/bin/env python3
""" Module of Session authentication views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
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

    user = None

    try:
        users = User.search({'email': email})

        for user in users:
            if user.is_valid_password(password):
                from api.v1.app import auth
                auth.create_session(user.id)
                return jsonify(user.to_json())
        return jsonify({"error": "wrong password"}), 401

    except Exception:
        pass

    if user is None:
        return jsonify({"error": "no user found for this email"}), 404
