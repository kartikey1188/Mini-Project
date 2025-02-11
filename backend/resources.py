from datetime import datetime
import traceback
from flask_restful import Api, Resource, marshal_with, marshal, fields
from flask import request
from backend.models import db, User, YouTubeLink
from flask_security import auth_required, current_user, hash_password, verify_password
import os
from werkzeug.utils import secure_filename
import uuid # UUID = Universally Unique Identifier
from flask import current_app as app

marshal_user = {
    'password' : fields.String,
    'email' : fields.String,
    'username' : fields.String,
    'image' : fields.String,
    'active' : fields.Boolean
}

marshal_link = {
    "id": fields.Integer,
    "url": fields.String
}

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


class User_Resource(Resource):
    @auth_required('token')
    @marshal_with(marshal_user)
    def get(self, id):
        user = User.query.filter(User.id == id).first()
        if not user:
            return {'Error' : 'User with this ID does not exist'}, 404 
        else:
            return user, 200 
            

    def post(self):
        data = request.form
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')

        def add_sponsor(image_path):
            try:
                checkname = User.query.filter(User.username==username).first()
                if checkname:
                    return {'Error': 'A user with this username already exists.'}, 920
                else:
                    user = userdatastore.create_user(
                        email=email,
                        password=hash_password(password),
                        username = username,
                        roles=[userdatastore.find_role('user')],
                        fs_uniquifier=str(uuid.uuid4()),
                        image=image_path,
                    )
                    db.session.add(user)
                    db.session.commit()
                    return {'Message': 'User has been registered successfully.'}, 200

            except Exception as e:
                db.session.rollback()
                print(f"Exception occurred: {e}")
                app.logger.error(traceback.format_exc())
                return {'Error': 'User could not be registered.'}, 500

        if not userdatastore.find_user(email=email):
            file = request.files.get('image')
            if file:
                if allowed_file(file.filename):
                    app.logger.info('check0')
                    r = username + 'user' + '_'
                    filename = r + secure_filename(file.filename)
                    save_path = os.path.join(app.config['IMAGE_FOLDER'], filename)
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)  # Make the directory if it doesn't exist
                    file.save(save_path)
                    return add_sponsor(filename)
                else:
                    return {'Error': 'Invalid File Type; Allowed Types = [".jpg", ".jpeg", ".png"]'}, 919
            else:
                return add_sponsor(None)
        else:
            return {'Error': 'A User with this email already exists.'}, 400

    @auth_required('token')
    def put(self, id):
        user = User.query.filter(User.id == id).first()
        if not user:
            return {"Error": "User with this ID does not exist"}, 404

        data = request.form

        if "username" in data and data["username"]:
            count = User.query.filter(User.username == data["username"]).count()
            if count != 0:
                return {"Error": "User with this username already exists"}, 400


        if "email" in data and data["email"]:
            existing_user = User.query.filter(User.email == data["email"]).first()
            if not existing_user:
                user.email = data["email"]
            else:
                return {"Error": "User with this email already exists."}, 400


        if "password" in data and data["password"]:
            user.password = hash_password(data["password"])

        file = request.files.get("image")
        if file:
            if allowed_file(file.filename):
                filename = user.username + "_" + secure_filename(file.filename)
                save_path = os.path.join(app.config["IMAGE_FOLDER"], filename)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                file.save(save_path)
                user.image = filename
            else:
                return {"Error": "Invalid File Type; Allowed Types = ['.jpg', '.jpeg', '.png']"}, 919

        try:
            db.session.commit()
            return {"Message": "User successfully updated"}, 200
        except:
            db.session.rollback()
            return {"Error": "Failed to update user"}, 500
        

class YouTubeLinkResource(Resource):
    @auth_required("token")
    @marshal_with(marshal_link)
    def get(self):
        """Fetches all YouTube links of the current user."""
        try:
            links = YouTubeLink.query.filter_by(user_id=current_user.id).all()
            return links, 200
        except Exception as e:
            app.logger.error(traceback.format_exc())
            return {"Error": "Failed to fetch links"}, 500

    @auth_required("token")
    def post(self):
        """Adds a YouTube link for the current user."""
        data = request.get_json()
        url = data.get("url")

        if not url:
            return {"Error": "No URL provided"}, 400

        try:
            link = YouTubeLink(url=url, user_id=current_user.id)
            db.session.add(link)
            db.session.commit()
            return {"Message": "Link added successfully", "id": link.id}, 200
        except Exception as e:
            db.session.rollback()
            app.logger.error(traceback.format_exc())
            return {"Error": "Failed to add link"}, 500

class DeleteYouTubeLink(Resource):
    @auth_required("token")
    def delete(self, id):
        """Deletes a YouTube link by ID (only if it belongs to the current user)."""
        link = YouTubeLink.query.filter_by(id=id, user_id=current_user.id).first()

        if not link:
            return {"Error": "Link not found"}, 404

        try:
            db.session.delete(link)
            db.session.commit()
            return {"Message": "Link deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            app.logger.error(traceback.format_exc())
            return {"Error": "Failed to delete link"}, 500

class SummarizeYouTubeLinks(Resource):
    @auth_required("token")
    def get(self):
        """Generates a summary based on the user's saved YouTube links."""
        try:
            links = YouTubeLink.query.filter_by(user_id=current_user.id).all()
            if not links:
                return {"Error": "No links found"}, 404

            # Dummy summary generation (replace this with actual summarization logic)
            summary = "Summary for {} videos.".format(len(links))

            return {"summary": summary}, 200
        except Exception as e:
            app.logger.error(traceback.format_exc())
            return {"Error": "Failed to generate summary"}, 500

api.add_resource(YouTubeLinkResource, "/youtube_links")
api.add_resource(DeleteYouTubeLink, "/youtube_links/<int:id>")
api.add_resource(SummarizeYouTubeLinks, "/summarize")
api.add_resource(Login, '/login') 
api.add_resource(User_Resource, '/user', '/user/<int:id>')




