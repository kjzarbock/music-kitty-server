# Music Kitty Server

## Overview

This is the server-side code for the Music Kitty project, built using Python and Django. Client-side code is available here: https://github.com/kjzarbock/music-kitty 

## Requirements

- Python 3.x
- Django 3.x
- Pipenv for managing virtual environments

## Installation

### Clone the Repository

git clone https://github.com/kjzarbock/music-kitty-server.git
cd music-kitty-server

### Set Up Virtual Environment

- We use Pipenv to manage dependencies and virtual environments. If you don't have Pipenv installed, you can install it using pip:

pip install pipenv

- Then, set up the virtual environment:

pipenv install

- This will install all the required packages listed in 'Pipfile'

### Activate Virtual Environment

- pipenv shell

### Run Migrations

- Before running the server, make sure to apply the database migrations:

python manage.py migrate

### Seed the Database

- To seed the database, first give execute permission to the seed script:

chmod u+x seed_database.sh

- Then run the script: 

./seed_database.sh

### Run the Server 

- To start the development server: 

python manage.py runserver

- Now, the server should be running at http://127.0.0.1:8000/.

### API Endpoints 

- /cats: List all cats
- /locations: List all locations
- /products: List all products
- /reservations: List all reservations
- /profiles: List all profiles
- /profile-adoptions: List all profile adoptions

Make sure that you grab a token for an authorized staff member or a user, depending on what you would like to do on the client-side.



