import os

class Config(): # This is a base class that other configuration classes can inherit from.
    DEBUG = False
    SQL_ALCHEMY_TRACK_MODIFICATIONS = False
    # SQLAlchemy can track changes to objects and emit signals. Setting SQLALCHEMY_TRACK_MODIFICATIONS to False disables this feature.
    # This reduces memory overhead because the application doesn't have to track modifications.


class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
    DEBUG = True # When DEBUG is True, Flask provides detailed error messages when something goes wrong.
    SECURITY_PASSWORD_HASH = 'bcrypt' # Specifies the hashing algorithm for passwords.
    SECURITY_PASSWORD_SALT = 'housecatboatcar' # Salt used in password hashing.
    SECRET_KEY = "catkittycatdogmousecat" # Used for session management and security features.
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token' # Header name for token-based authentication.

    WTF_CSRF_ENABLED = False #  CSRF = Cross-Site Request Forgery

    # image specific
    IMAGE_FOLDER = os.path.abspath('./backend/pictures')
    ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png']