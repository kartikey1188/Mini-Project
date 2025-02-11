from datetime import datetime
import traceback
from flask_restful import Api, Resource, marshal_with, marshal
from flask import request
from backend.models import db, User
from flask_security import auth_required, current_user, hash_password, verify_password
import os
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename
import uuid # UUID = Universally Unique Identifier
from flask import current_app as app

from flask_restful import fields

marshal_user = {
    'password' : fields.String,
    'email' : fields.String,
    'image' : fields.String,
    'appeal' : fields.String,
    'active' : fields.Boolean
}


cache = app.cache

api = Api(prefix='/api')
userdatastore = app.security.datastore


def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in app.config['ALLOWED_EXTENSIONS']  


class Login(Resource):
    
    def post(self):
        
        data = request.get_json()
        
        email = data.get('email') 
        password = data.get('password')

        user = userdatastore.find_user(email = email)

        if not user:
            return {"message" : "invalid email"}, 400
        
        if verify_password(password, user.password):
            return {"email" : user.email, 'role' :user.roles[0].name, 'id' : user.id, 'token' : user.get_auth_token()}, 200
        
        return {"Error" : "Invalid Password"}, 400


class Sponsor_Resource(Resource):
    @auth_required('token')
    @cache.memoize(timeout = 5) # memoize is used for functions which take an input, cached is used for functions which don't take an input
    @marshal_with(marshal_sponsor)
    def get(self, id):
        sponsor = Sponsor.query.filter(Sponsor.id == id).first()
        if not sponsor:
            return {'Error' : 'User with this ID does not exist'}, 404 # 404 = Not Found
        else:
            return sponsor, 200 # 200 = OK
            

    def post(self):
        data = request.form
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        industry = data.get('industry')
        expenditure = data.get('expenditure', 0)

        def add_sponsor(image_path):
            try:
                checkname = Sponsor.query.filter(Sponsor.username==username).first()
                if checkname:
                    return {'Error': 'A sponsor with this username already exists.'}, 920
                else:
                    user = userdatastore.create_user(
                        email=email,
                        password=hash_password(password),
                        roles=[userdatastore.find_role('sponsor')],
                        fs_uniquifier=str(uuid.uuid4()),
                        image=image_path,
                    )
                    app.logger.info('check3')
                    db.session.commit()
                    app.logger.info('check2')
                    
                    sponsor = Sponsor(
                        id=user.id,
                        user=user,
                        username=username,
                        industry=industry,
                        expenditure=int(expenditure)
                    )
                    db.session.add(sponsor)
                    db.session.commit()
                    cache.delete('/admin/statistics')
                    return {'Message': 'Sponsor has been registered successfully.'}, 200

            except Exception as e:
                db.session.rollback()
                print(f"Exception occurred: {e}")
                app.logger.error(traceback.format_exc())
                return {'Error': 'Sponsor could not be registered.'}, 500

        if not userdatastore.find_user(email=email):
            file = request.files.get('image')
            if file:
                if allowed_file(file.filename):
                    app.logger.info('check0')
                    r = username + 'sponsor'
                    filename = r + secure_filename(file.filename)
                    save_path = os.path.join(app.config['IMAGE_FOLDER'], filename)
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)  # Make the directory if it doesn't exist
                    file.save(save_path)
                    app.logger.info('check1')
                    return add_sponsor(filename)
                else:
                    return {'Error': 'Invalid File Type; Allowed Types = [".jpg", ".jpeg", ".png"]'}, 919
            else:
                return add_sponsor(None)
        else:
            return {'Error': 'A Sponsor with this email already exists.'}, 400

    @auth_required('token')
    def put(self, id):
        sponsor = Sponsor.query.filter(Sponsor.id == id).first()
        if not sponsor:
            return {"Error": "Sponsor with this ID does not exist"}, 404

        data = request.form

        if "username" in data and data["username"]:
            sponsor_campaigns = Campaign.query.filter(Campaign.parent==sponsor.username).all()
            count = Sponsor.query.filter(Sponsor.username == data["username"]).count()
            if count != 0:
                return {"Error": "Sponsor with this username already exists"}, 920
            
            old_username = sponsor.username
            
            sponsor.username = data["username"]


            for campaign in sponsor_campaigns:
                campaign.parent = data['username']

            ad_requests = Ad_Request.query.filter(Ad_Request.associated_sponsor==old_username).all()
            for request_ in ad_requests:
                request_.associated_sponsor = data['username']


        if "email" in data and data["email"]:
                user = User.query.filter(User.email==data["email"]).first()
                if not user:
                    sponsor_id = sponsor.id
                    parent_user = User.query.filter(User.id==sponsor_id).first()
                    parent_user.email = data["email"]
                else:
                    return {"Error":"User with this email already exists."}, 921

        if "password" in data and data["password"]:
            user = sponsor.user
            user.password = hash_password(data["password"])

        
        if "industry" in data and data["industry"]:
            industry = data["industry"]
            if industry == "other":
                undisclosed = data.get("undisclosed", "Undisclosed")
                sponsor.industry = undisclosed
            else:
                sponsor.industry = industry

        file = request.files.get("image")
        if file:
            if allowed_file(file.filename):
                filename = sponsor.username + "_sponsor_" + secure_filename(file.filename)
                save_path = os.path.join(app.config["IMAGE_FOLDER"], filename)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                file.save(save_path)
                sponsor.user.image = filename
            else:
                return {"Error": "Invalid File Type; Allowed Types = ['.jpg', '.jpeg', '.png']"}, 919

        try:
            db.session.commit()
            cache.delete_memoized(Sponsor_Resource.get, self, id)
            cache.delete('/admin/statistics')
            return {"Message": "Sponsor successfully updated"}, 200
        except:
            db.session.rollback()
            return {"Error": "Failed to update sponsor"}, 500

    
api.add_resource(Login, '/login') 




