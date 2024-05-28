#!/usr/bin/env python3
"""
This module creates a model User
"""
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Create a base class for declarative database objects
Base = declarative_base()

# Define a User class/table


class User(Base):
    """
    This is a SQLAlchemy declarative model for a 'users' table.

    Attributes:
        id (int): The primary key.
        email (str): The user's email.
        hashed_password (str): The user's password.
        session_id (str): The user's session ID.
        reset_token (str): The user's  token.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
