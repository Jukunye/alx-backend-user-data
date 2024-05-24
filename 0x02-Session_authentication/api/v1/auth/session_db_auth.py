#!/usr/bin/env python3
""" This module contains the SessionDBAuth """

from flask import request
from datetime import datetime, timedelta
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """class with authentication data stored in database"""

    def create_session(self, user_id=None) -> str:
        """ Creates and stores new instance of UserSession
        and returns the Session ID
        """
        session_id = super().create_session(user_id)
        if type(session_id) == str:
            kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the User ID by requesting UserSession in the database
        based on session_id"""
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None

        current = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        expire_time = sessions[0].created_at + time_span
        if expire_time < current:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """ Destroys the UserSession based on the Session ID
        from the request cookie """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
