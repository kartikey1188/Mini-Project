from flask import current_app as app
from backend.models import db
from flask_security import hash_password

def initialize_data():
    with app.app_context():
        db.create_all()

        datastore = app.security.datastore

        # What is a user datastore? 
        # It is an object that provides methods to create, retrieve, update, and delete users and roles. 
        # It saves us from writing custom code to handle these actions. 
        # datastore is specifically tied to the Flask-Security extension and relies on the Flask-Security framework to function as intended.

        datastore.find_or_create_role(name = 'user', description = 'just a regular user')


        if not datastore.find_user(email = 'user1@gmail.com'):
            datastore.create_user(email = 'user1@gmail.com', password = hash_password('user1'), roles = ['user'] )
       

        db.session.commit()