#!/usr/bin/env python3
"""
This module contains the flask app
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)

AUTH = Auth()


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register():
    """
    Register user end-point
    """
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"})


@app.route('/sessions', methods=['POST'])
def login():
    """
    Session login flask
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if (AUTH.valid_login(email, password)):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """
    Endpoint that destroys a session
    """

    session_id = request.cookies.get("session_id", None)
    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
