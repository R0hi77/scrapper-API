# SCRAPPER API

## OVERVIEW
This API scrapes jobs from ``https://www.ghanajobs.com`` into main database and allows users to access the scrapped jobs by registering an account. User can save their prefered jobs for future reference and and manage thier saved jobs.An admininistrator account manages scrapping and all the data in the database.User registration data is validated with Pydantic library and scrapping is handled with the Beautifulsoup library.

## DOCUMENTATION
API uses HTTP methods to interract with resources. It supports the following endpoints.

### Authentication
1. #### Registration
- `POST api/auth/register` -create account

- Requires the data below 
```json
{
    "username":"johndoe123",
    "email":"johndoe@email.com",
    "password":"password12345"
}

```
2. #### Login
- `POST api/auth/login` - Log into account

- Requires the data below
```json
{
    "email":"johndoe@email.com",
    "password":"password12345"
}

```
3. #### view user profile information
- `GET api/auth/me` 
This endpoint handles display user profile information 

4.  #### Refresh Access token
- `GET api/auth/refresh` -refresh access token
- This enpoint handles token refreshing upon expiry

5. #### Log out
- `POST api/auth/logout` -Logging out
- This endpoint revokes token issued upon  user log in.

### Administration
This blueprint handles all admin operations such as scrapping and regulating data  in main database, User account monitoring 

1. #### Scrape into main database
- `GET api/admin/scrape`
- Requires particular job and page number in request url
request url should be as follows `api/admin/scrape/?role=Backend%20eveloper&page=1`


2. #### View all scraped data
- `GET api/admin/`
- Returns all scraped data from main database

3. #### Filter through scraped data
- `GET api/admin/`
- This endpoint filters through scrapped data based on request query, search query  can be particular job role or job skill requirement .
Rquest url should have format `GET api/admin/?q=DevOps`

4. #### Edit data in the main database
- `PUT api/admin/<int:id>`
- This endpoint allows admin to modify database content by a specified id
- Requires the data below:
```json
{
    "role":"frontend engineer",
    "description":"string",
    "location":"Central Region",
    "company":"Amanda Inc.",
    "requirements":"HTML,CSS,Javascript,React",
    "posted":"3 weeks ago"
}

```

5. #### Delete job from database
- `DELETE api/admin/<int:id>`
- This endpoint deletes saved jobs from main database by specified job id


6. #### Scrape history
- `GET api/admin/history`
- This endpoint tracks all scrape history it stores particular jobs scraped and its corresponding page number

### Migration
 This blueprint allows user to save jobs into accouts 
1. #### Query main database
- `GET api/job`
user can get all data in the database or filter through the data by keywords as follows : `GET/api/job?q=Mobile application development`

2. #### Save into user account
- `GET api/job/save/<int:id>`
- Users can save particular job preferences by provide the job id.

### User operations
This blueprint handles all user account operations. View all saved data, delete saved data and filter through saved data

1.  #### Get all saved jobs
- `GET api/mysaves/`
- returns all saved jobs

2.  #### filter through saved jobs
- `GET api/mysaves/?q=keyword`
Returns search results from search by keyword provided.

3. #### Get single job
- `GET api/mysaves/<int:id>`
Returns job with id provided

4. #### Delete job
- `DELETE api/mysaves/<int:id>`
- Deletes job with the id provided



