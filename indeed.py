import requests
from bs4 import BeautifulSoup



def get_url(role:str):
     url =f'https://www.linkedin.com/jobs/search?keywords={role}&location=Ghana&geoId=105769538&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
     return url




headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0'}

response = requests.get(get_url("Software Engineering"),headers=headers) 
soup = BeautifulSoup(response.text,'html.parser')
jobs = soup.find_all('div', class_="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card")

count = 0
job_list =[]
for job in jobs:
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
     job_list.append(job)    

print(job_list)
        
    

     




#print(len(jobs))