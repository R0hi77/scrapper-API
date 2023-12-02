from flask import Blueprint,request,jsonify
from .model import Job,db,Save
from flask_jwt_extended import get_jwt_identity,jwt_required

"""
Handles job migrations from main table to user table
"""

job_bp = Blueprint('operations',__name__,url_prefix='/api/job')

#get all data in main table
@job_bp.get('/')
@jwt_required()
def get_joblist():
    query=request.args.get('q')
    if query:
        query="%{}%".format(query)
        results = Job.query.filter(Job.role.like(query)|Job.description.like(query)|Job.location.like(query)|Job.requirements.like(query)).all()
        if results:
            list =[]
            for result in results:
                list.append({
                    "id":result.id,
                    "role":result.role,
                    "company":result.company,
                    "description":result.description,
                    "location":result.location,
                    "required skills":result.requirements,
                    "posted":result.posted})
            return jsonify(list)
        else:
            return jsonify({'msg':'No search results found'})
    else:
        jobs=Job.query.all()
        list=[]
        for job in jobs:
            list.append ({
            "id":job.id,
            "role":job.role,
            "company":job.company,
            "location":job.location,
            "required skills":job.requirements,
            "description":job.description,
            "posted":job.posted
            })
        return jsonify(list)

#save job item into user job table by id
@job_bp.get('save/<int:id>')
@jwt_required()
def save(id):
    job=Job.query.filter_by(id=id).first()
    identity =get_jwt_identity()
    if job:
        save=Save(
            role=job.role,
               description=job.description,
               location=job.location,
               company=job.company,
               requirements=job.requirements,
               posted=job.posted,
               user_id=identity)
        
        db.session.add(save)
        db.session.commit()

        return jsonify(
            {
            "id":save.id,
            "role":save.role,
            "company":save.company,
            "location":save.location,
            "required skills":save.requirements,
            "description":save.description,
            "posted":save.posted 
            }
        )
    return jsonify({'msg':f'Job item with id {id} does not exists'})
        

        

        

