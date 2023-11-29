# import requests
# from requests.auth import HTTPBasicAuth
# from bs4 import BeautifulSoup



# def get_url():
#     template = 'https://www.ghanajob.com/job-vacancies-search-ghana/Software%20Engineer?f%5B0%5D=im_field_offre_metiers%3A31&page=1'
#     return template

# response =requests.get(get_url())
# print(response.status_code)
# soup = BeautifulSoup(response.content,'html.parser')
# jobs = soup.find_all('div', class_='col-lg-5 col-md-5 col-sm-5 col-xs-12 job-title')


# job_list =[]
# count =0
# for job in jobs:
#     count=count+1
#     role = job.find('a').text.strip()
#     try:
#         description = job.find('div',class_='search-description').text.strip()
#     except:
#         description=''
#     #print(description)

#     posted = job.find('p',class_='job-recruiter').text.strip()
#     #print(posted)

#     company = job.find('a',class_='company-name').text.strip()
#     #print(company)

#     skills = job.find('div',class_= 'job-tags').text.strip()
#     #print(skills)

#     locations = job.find('p', class_=None).text.strip()
#     #print(locations)

#     job= {
#         "id":count,
#         "role":role,
#         "company":company,
#         "location":locations,
#         "required skills":skills,
#         "posted":posted
#     }

#     job_list.append(job)

# print(job_list)







