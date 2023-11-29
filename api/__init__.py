from flask import Flask,Blueprint
#import os
from .model import db
from .auth import auth_bp
from .scrape import scrape_bp
from flask_jwt_extended import JWTManager


def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)
    # connect to database
    
    if test_config is None:
        app.config.from_mapping(
            SERCRET_KEY ='dev',
            SQLALCHEMY_DATABASE_URI='sqlite:///tempdatabase.db',
            JWT_SECRET_KEY='key'
        )
            
    else: 
        app.config.from_mapping(test_config)
        
    db.init_app(app)
    JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(scrape_bp)


    
    return app