from flask import Blueprint,request,jsonify
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity,get_jwt
from werkzeug.security import generate_password_hash,check_password_hash
from api.schema import UserData,LoginData
from api.model import db, User,BlockedTokens
from pydantic import ValidationError
auth_bp = Blueprint('auth',__name__,url_prefix='/api/auth')

@auth_bp.post('/register')
def register():
    rawData = request.get_json()
    try:
        validData = UserData(username=rawData['username'],
                            email=rawData['email'],
                            password=rawData['password'])
    except ValidationError as e:
        return jsonify({'request data validation error':str(e)})
    
    user = User(username=validData.username,
                email=validData.email,
                password=generate_password_hash(validData.password)
                )
    
    db.session.add(user)
    db.session.commit()

    return jsonify({'username':user.username,
                    'email':user.email})

@auth_bp.post('/login')
def login():
    rawData = request.get_json()
    try:
        validData = LoginData(email=rawData['email'],password=rawData['password'])
    except ValidationError as e:
        return jsonify({"msg":str(e)})
    
    user = User.query.filter_by(email = validData.email).first()
    if user and check_password_hash(user.password,validData.password):
        
        access_token=create_access_token(identity=user.id)
        refresh_token=create_refresh_token(identity=user.id)

        return jsonify(
                {"access_token":access_token,
                 "refresh_token":refresh_token,
                 "username":user.username,
                 "email":user.email,
                 "id":user.id}
            )
    else:
        return jsonify({"mesdage":"Invalid login credentials"})

@auth_bp.get('/refresh')
@jwt_required(refresh=True)
def refresh_token():
    identity=get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({'access_token':access_token})



@auth_bp.post('/logout')
@jwt_required()
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
        return jsonify({'msg':'user logged out'})    
    






   

    

    
    