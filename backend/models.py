from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, nullable=False)
    image = db.Column(db.Text, unique=True)

    youtube_links = db.relationship('YouTubeLink', back_populates='user', cascade="all, delete-orphan")
    text_files = db.relationship('TextFile', back_populates='user', cascade="all, delete-orphan")

    # flask-security specific columns:
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)  # Used by Flask-Security for token invalidation
    active = db.Column(db.Boolean, default=True)  # Indicates if the user is active
    roles = db.relationship('Role', backref='rbacmagic', secondary='user_roles')

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

class YouTubeLink(db.Model):
    __tablename__ = 'youtube_links'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='youtube_links')

class TextFile(db.Model):
    __tablename__ = 'text_files'
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String, nullable=False)
    file_name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='text_files')
