from flask import Blueprint,request,jsonify
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity,get_jwt,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from api.schema import UserData,LoginData
from api.model import db, User,BlockedTokens
from pydantic import ValidationError

"""
Handles all authentications and registrations
"""
auth_bp = Blueprint('auth',__name__,url_prefix='/api/auth')

#create an account
@auth_bp.post('/register')
def register():
    rawData = request.get_json()
    try:
        validData = UserData(username=rawData['username'],
                            email=rawData['email'],
                            password=rawData['password'])
    except ValidationError as e:
        return jsonify({'request data validation error':str(e)})
    
    test=User.query.filter_by(email=validData.email).first()
    if test is not None:
        return jsonify({'msg':'email already exists'})
           
    user = User(username=validData.username,
                    email=validData.email,
                    password=generate_password_hash(validData.password)
                    ) 
    db.session.add(user)
    db.session.commit()
    return jsonify({'username':user.username,
                        'email':user.email})

#login into account
@auth_bp.post('/login')
def login():
    rawData = request.get_json()
    try:
        valid = LoginData(email=rawData['email'])
    except:
        return jsonify({'msg':'Enter a valid email'})
    user = User.query.filter_by(email = valid.email).first()
    if user and check_password_hash(user.password,rawData['password']):
        access_token=create_access_token(identity=user.username)
        refresh_token=create_refresh_token(identity=user.username)
        return jsonify(
                    {"access_token":access_token,
                    "refresh_token":refresh_token,
                    "username":user.username,
                    "email":user.email,
                    "id":user.id}
              )
    return jsonify({"message":"Invalid login credentials"})
    

 #view user profile   
@auth_bp.get('/me')
@jwt_required()
def me():
    identity = get_jwt_identity()
    claims = get_jwt()
    me = User.query.filter_by(username=identity).first()
    return jsonify(
        {
            'username':current_user.username,
            'email':me.email,
            'role':claims['role']
        }
    )

#refresh access token
@auth_bp.get('/refresh')
@jwt_required()
def refresh_token():
    identity=get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({'access_token':access_token})


#log out
@auth_bp.post('/logout')
@jwt_required(verify_type=False)
def logout():
    jwt=get_jwt()
    jti=jwt['jti']

    token = BlockedTokens.query.filter_by(token=jti).first()
    if token:
        return jsonify({"message":"Token already blocked"})
    else:
        token = BlockedTokens(token=jti)
        db.session.add(token)
        db.session.commit()
        return jsonify({'msg': 'log out successful'})    
    






   

    

    
    