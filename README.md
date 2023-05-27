# Self Finance Countiong "My-Money"

This is Web-Application for self finance counting. You can register user, create "bank" accounts and make transaction.

Technologies: Python-3.10, Django-4, Postgres, HTML/CSS/JS.  

## QUICK LOCAL START

All commands only for Linux (Debian) systems! If you want start this project local you need do this steps:

### STEP 1

Install packages

    sudo apt-get update
    sudo apt-get install -y python3-dev python3-venv python3-pip libpq-dev postgresql postgresql-contrib

### STEP 2

Clone this git project

    git clone https://github.com/tsyhanenkod/M-Money.git
    
And open project dir

    cd M-Money

### STEP 3

Create new database and user (Save the login, password and other important data for future connection in the .env file)

    sudo -u postgres psql
    
    CREATE DATABASE <dbname>;
    CREATE USER <username> WITH PASSWORD '<user_password>';
    ALTER ROLE <username> SET client_encoding TO 'utf8';
    ALTER ROLE <username> SET default_transaction_isolation TO 'read committed';
    ALTER ROLE <username> SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE <dbname> TO <username>;
    
    \q

### STEP 4

Expand data from backup file for test project with data

    psql -U <username> -d <dbname> -h 127.0.0.1 -p 5432 -f ./backup.sql

Now you have 2 users in Database 
Admin SumSU for login in Admin Panel and Test User for login in Web-Application user account

    Admin SumSU 
        login: sumdu@sumdu.sumdu 
        password: sumdu

    Test User 
        login: test@test.test
        password: test

### STEP 5

Create venv and activate it

    sudo python3 -m venv venv
    source venv/bin/activate  

### STEP 6

Install all pip pakages from requirements.txt file:

    sudo pip3 install -r requirements.txt
    
Also you can install environ for venv vars

    sudo apt-get install environ

### STEP 7

Create .env file or copy .env_template and set you data:

    less .env_temp > .env

### STEP 8 

Make migrations in django project:

    python manage.py makemigrations
    python manage.py migrate
    
Also you can create new superuser for login in admin panel (127.0.0.1:8000/admin)

    python manage.py createsuperuser

### STEP 9 

Run project local:

    python3 manage.py runserver

    