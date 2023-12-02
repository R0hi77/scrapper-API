from bs4 import BeautifulSoup
import requests

def get_url(role,page):
    url_template='https://www.ghanajob.com/job-vacancies-search-ghana/{}?f%5B0%5D=im_field_offre_metiers%3A31&page={}'
    url = url_template.format(role,page)
    return url

def raw_data(url):
    result=requests.get(url)
    soup=BeautifulSoup(result.content,'html.parser')
    jobs= soup.find_all('div', class_='col-lg-5 col-md-5 col-sm-5 col-xs-12 job-title')
    job_list =[]
    for job in jobs:
        role = job.find('a').text.strip()
        try:
            description = job.find('div',class_='search-description').text.strip()
            description = description.replace('\n','')
        except:
            description=''
                    
        posted = job.find('p',class_='job-recruiter').text.strip()
                    
        company = job.find('a',class_='company-name').text.strip()
                        
        skills = job.find('div',class_= 'job-tags').text.strip()
            
        locations = job.find('p', class_=None).text.strip()
                        
        job= {
            "role":role,
            "company":company,
            "location":locations,
            "required skills":skills,
            "description":description,
            "posted":posted
            }
        job_list.append(job)
    return job_list





