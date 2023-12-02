from flask import Blueprint,jsonify,request
from .model import Save,db,User
from flask_jwt_extended import jwt_required,get_jwt_identity

save_bp = Blueprint('user',__name__,url_prefix='/api/mysaves')


#get all user saved jobs
@save_bp.get('/')
@jwt_required()
def all_saved_jobs():
    identity=get_jwt_identity()
    results=Save.query.filter(Save.user_id==identity).all()
    if results:
            list=[]
            for result in results:
                list.append ({
                    "id":result.id,
                    "role":result.role,
                    "company":result.company,
                    "description":result.description,
                    "location":result.location,
                    "required skills":result.requirements,
                    "posted":result.posted,
                    "user_id":result.user_id})
            return jsonify(list)
    
    return jsonify({'msg':'No search results found'})


#filter through user saved data
@save_bp.get('/')
@jwt_required()
def search():
    identity = get_jwt_identity()
    q = request.args.get('q')
    user_saves = Save.query.filter(Save.user_id == identity).all()
    if user_saves:
        filtered = [save for save in user_saves if q in save.role or q in save.requirements]
        filtered_dicts=[save.__repr__() for save in filtered]
        return jsonify(filtered_dicts)
    
    return jsonify({'msg': "no search result found"})



#get single saved item by id
@save_bp.get('/<int:id>')
@jwt_required()
def get_one(id):
    identity=get_jwt_identity()
    job =Save.query.filter((Save.user_id==identity)&(Save.id==id)).one_or_none()
    if job is not None:
        return (
                {"id":job.id,
                "role":job.role,
                "company":job.company,
                "location":job.location,
                "required skills":job.requirements,
                "description":job.description,
                "posted":job.posted
                }
            )
    else:
        return jsonify({'msg':'No such job item exists'})


#delete saved item from user saves table  
@save_bp.delete('/<int:id>')
@jwt_required()
def delete(id):
    user_save_query=db.session.query(User,Save)
    user_save_query = user_save_query.join(Save,User.id==Save.user_id)
    job = user_save_query.filter(Save.id ==id).first()
    if job is not None:
        db.session.delete(job)
        db.session.commit()
        return jsonify(),204
    else:
        return jsonify({'msg':'No such  job item exists'})



    


        
