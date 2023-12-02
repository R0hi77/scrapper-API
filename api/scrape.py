from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt
from .model import Job,db,History
from raw import get_url,raw_data

"""
Blueprint to handle all admin operations; Scrape to main db, 
delete from main db, view scrape history
"""


admin_bp = Blueprint('admin',__name__,url_prefix='/api/admin')

#scrape data into main table
@admin_bp.get('/scrape')
@jwt_required()
def scrape():
    claims = get_jwt()
    if claims['role'] == 'admin':
        role = request.args.get('role')
        page = request.args.get('page')
        if page is None and role is None:
            return jsonify({"error":"request should have format: api/admin/scrape?role=software%20engineering&page=1"})
        else:
            url = get_url(role, page)
            jobs = raw_data(url)
            results = []
            for job in jobs:
                results.append({
                    "role": job['role'],
                    "company": job['company'],
                    "location": job['location'],
                    "required skills": job['required skills'],
                    "description": job['description'],
                    "posted": job['posted']
                })
                save=Job(role=job['role'],
                         company=job['company'],
                         location=job['location'],
                         requirements=job['required skills'],
                         description=job['description'],
                         posted=job['description'])
                db.session.add(save)
            db.session.commit()

            history=History(query_text=role,page=page)
            db.session.add(history)
            db.session.commit()

            return jsonify(results)
    return jsonify({'msg': "Access to this endpoint denied"})


#all data in main table        
@admin_bp.get('/')
@jwt_required()
def get_all_from_database():
    claims = get_jwt()
    if claims['role'] == 'admin':
        jobs=Job.query.all()
        if jobs:
            list = []
            for job in jobs:
                list.append({
                "id": job.id,
                "role": job.role,
                "company": job.company,
                "location": job.location,
                "required skills": job.requirements,
                "description": job.description,
                "posted": job.posted
                        })
            return jsonify(list)
        else:
            return jsonify({'msg': 'No jobs added yet'})
    return jsonify({'msg': "Access to this endpoint denied"})


#filter through all scraped data from main table
@admin_bp.get('/')
@jwt_required()
def search():
    claims = get_jwt()
    if claims['role'] == 'admin':
        q=request.args.get('q')
        query='%{}%'.format(q)

        jobs=Job.query.filter(Job.role.like(query)|Job.description.like(query)|Job.requirements.like(query)).all()
        if jobs:
            list = []
            for job in jobs:
                list.append({
                "id": job.id,
                "role": job.role,
                "company": job.company,
                "location": job.location,
                "required skills": job.requirements,
                "description": job.description,
                "posted": job.posted
                        })
            return jsonify(list)
        else:
            return jsonify({'msg': 'No jobs added yet'})
    return jsonify({'msg': "Access to this endpoint denied"})

#delete from main main
@admin_bp.delete('/<int:id>')
@jwt_required()
def delete(id):
    claims = get_jwt()
    if claims['role']=='admin':
        job=Job.query.filter_by(id=id).first()
        if job is not None:
            db.session.delete(job)
            db.session.commit()
            return jsonify(),204
        else:
            jsonify({'msg':f'Jobs with {id}  does not exist'})
    return jsonify({'msg':'Acces to this endpoint denied'})


#Retrieves all scrape history
@admin_bp.get('/history')
@jwt_required()
def get_scrape_history():
    claims=get_jwt()
    if claims['role']=='admin':
        history=History.query.all()
        if history:
            list=[]
            for i in history:
                list.append(
                    {
                        "id":i.id,
                        "query":i.query_text,
                        "page":i.page
                    }
                )
            return jsonify(list)
        else:
            return jsonify({'msg':'No history'})
    return jsonify({'msg':'Access to this endpoint denied'})

    
        






    
    
    


    
