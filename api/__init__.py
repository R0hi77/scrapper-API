from flask import Flask,Blueprint 
import os
from .model import db
from .auth import auth_bp
from .scrape import admin_bp
from flask_jwt_extended import JWTManager
from .model import User
from .user import save_bp
from .migrator import job_bp
import psycopg2

def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)

    #database creds
    host=os.environ.get('POSTGRES_HOST')
    port=os.environ.get('POSTGRES_PORT')
    user=os.environ.get('POSTGRES_USER')
    password=os.environ.get('POSTGRES_PASSWORD')
    database=os.environ.get('POSTGRES_DATABASE')

    #sqlite_uri='sqlite:///tempdatabase.db'
    DB_URL= 'postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}'.format(user=user,pw=password,host=host,port=port,db=database)
    if test_config is None:
        app.config.from_mapping(
            SERCRET_KEY =os.getenv('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('MYSQL_DATABASE'),
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY")
        )
            
    else: 
        app.config.from_mapping(test_config)
        
    db.init_app(app)
    jwt=JWTManager(app)

    #register blueprint
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(save_bp)
    app.register_blueprint(job_bp)


    #call back
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_headers, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(username=identity).one_or_none()
    

    #additional claims to jwt
    @jwt.additional_claims_loader
    def additonal_claims(identity):
        if identity == 'admin':
            return {'role':'admin'}
        else:
            return {'role':'user'}
    

    return app