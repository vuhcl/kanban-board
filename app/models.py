# Database

from sqlalchemy import Column, String, Integer, Enum, ForeignKey
from app import db

class User(db.Model):
    """User class
    Attributes:
        username (str): unique username, primary key.
        password (str): user's password.
    """
    __tablename__ = 'users'
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)

class Task(db.Model):
    """Task class
    Attributes:
        id (int): Unique id, primary key, auto increment.
        username (str): Foreign key referencing Users table.
        task (str): Details of the task.
        status (enum): Status of the task, with the following values
            - 'to_do'
            - 'doing'
            - 'done'
    """
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey('users.username'))
    task = db.Column(db.String, nullable=False)
    status = db.Column(Enum('to_do', 'doing', 'done'))

# Initialize database
db.create_all()
db.session.commit()