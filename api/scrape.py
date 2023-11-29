from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required
from bs4 import BeautifulSoup
import requests




scrape_bp = Blueprint('scrape',__name__,url_prefix='/api/scrape')

@scrape_bp.get('')
#@jwt_required()
def scrape():
    qrole=request.args.get('role')
    qlocation=request.args.get('location')
    qskills=request.args.get('skills')

    response1= requests.get('https://www.ghanajob.com/job-vacancies-search-ghana/Software%20Engineer?f%5B0%5D=im_field_offre_metiers%3A31&page=1')
    response2 = requests.get('https://www.linkedin.com/jobs/search?keywords=Software%20Engineering&location=Ghana&geoId=105769538&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0')
    soup1 = BeautifulSoup(response1.content,'html.parser')
    soup2 = BeautifulSoup(response2.content,'html.parser')
    jobs1 = soup1.find_all('div', class_='col-lg-5 col-md-5 col-sm-5 col-xs-12 job-title')
    jobs2 = soup2.find_all('div', class_="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card")

    count = 0
    job_list = []

    for job in jobs1:
        count=count+1
        role = job.find('a').text.strip()
        try:
            description = job.find('div',class_='search-description').text.strip()
            description = description.replace('\n','')
        except:
            description=''
        #print(description)
        posted = job.find('p',class_='job-recruiter').text.strip()
        #print(posted)
        company = job.find('a',class_='company-name').text.strip()
        #print(company)
        skills = job.find('div',class_= 'job-tags').text.strip()
        #print(skills)
        locations = job.find('p', class_=None).text.strip()
        #print(locations)
        job= {
            "role":role,
            "company":company,
            "location":locations,
            "required skills":skills,
            "description":description,
            "posted":posted
            }
        
        i={count:job}
        job_list.append(i)
        #print(len(job_list)
        

    for job in jobs2:
        count=count+1
        role =job.find("h3",class_="base-search-card__title").text.strip()
        company =job.find('a',class_="hidden-nested-link").text.strip()
        location = job.find('span',class_='job-search-card__location').text.strip()
        try:
            timestamp =job.find('time', class_='job-search-card__listdate').text.strip()
        except:
            timestamp = ''

        job={"role":role,
            "company":company,
            "location":location,
            "posted":timestamp
            }
        j={count:job}
        job_list.append(j)

    return jsonify({'jobs':job_list})

@scrape_bp.get('')
def save():
    pass


    
