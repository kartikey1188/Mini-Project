from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique = True, nullable = False)
    username = db.Column(db.String, nullable = False)
    image = db.Column(db.Text, unique = True)
    # flask-security specific columns:
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False) # Unique identifier used by Flask-Security to handle token invalidation after password changes.
    active = db.Column(db.Boolean, default=True) # Boolean value indicating if the user's account is active.
    roles = db.relationship('Role', backref='rbacmagic', secondary='user_roles') # Many-to-many relationship with the Role model via the user_roles association table.

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)

class UserRoles(db.Model): # Implements the many-to-many relationship between User and Role.
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
