# [Instagram]()
#### Web clone of the Instagram app
#### By **[Trevin Livele]**

## Description
This is a simple web clone of the instagram website. A user can create an account and sign into it. 
The site supports uploading images, and following other users. 
users can view photos uploaded by other users in the home page of app.

## Set Up and Installations

### Prerequisites
1. Ubuntu Software
2. Python3.8
3. [Postgres](https://www.postgresql.org/download/)
4. [python virtualenv](https://gist.github.com/Geoyi/d9fab4f609e9f75941946be45000632b)

### Clone the Repo
Run the following command on the terminal:
`git clone git@github.com:trevin-livele/django-insta-clone.git && cd Instagram`

### Activate virtual environment
Activate virtual environment using python3.8 as default handler
```bash
virtualenv -p /usr/bin/python3.8 venv && source venv/bin/activate
```

### Install dependancies
Install dependancies that will create an environment for the app to run
`pip3 install -r requirements.txt`

### Create the Database
```bash
psql
CREATE DATABASE instaclone;
```
### .env file
Create .env file and paste paste the following filling where appropriate:
```python
SECRET_KEY = '<Secret_key>'
DBNAME = 'instaclone'
USER = '<Username>'
PASSWORD = '<password>'
DEBUG = True

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = '<your-email>'
EMAIL_HOST_PASSWORD = '<your-password>'
```
### Run initial Migration
```bash
python3.8 manage.py makemigrations gram
python3.8 manage.py migrate
```

### Run the app
```bash
python3.8 manage.py runserver
```
Open terminal on `localhost:8000`

## Known bugs
Like and Follow functionality do not work as of yet

## Technologies used
    - Python 3.8.10
    - HTML
    - Bootstrap 
    - JavaScript
    - Heroku
    - Postgresql

## Support and contact details
Contact me on liveletrevin6@gmail.com for any comments, reviews or advice.

### License
Copyright (c) **Trevin Livele**
