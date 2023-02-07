<p align="center">
<h1>Go to <a href="https://www.tibiastats.online/">tibiastats.online</a></h1>


- [About](#about)
- [Features](#features)
- [Tech stack](#stack)
- [Structure](#structure)
- [Requirements](#requirements)
- [Installation](#installation)


# About
The Tibia game tracking application allows users to monitor their progress in the game, including
their character level, acquired experience and charm points. Users can also track boss information
such as respawn time on all game worlds. All this information is stored in a MySQL database 
and presented in a clear and easy to interpret manner using Charts.js data visualization library.
The application is built with a Python Django backend and a Bootstrap, HTML5, CSS3 
and JavaScript frontend, making it easy to use the tools and analyze their Tibia game results.

# Features

1. **Worlds informations.**
    - [x] Basic information.
    - [ ] Online time counter.
2. **Character information.**
    - [x] Basic information.
    - [x] World transfers.
    - [x] Name changes.
3. **Experience change list.**
    - [x] Mainland.
    - [x] Rookgaard.
4. **Charm change list.**
    - [x] Mainland.
    - [x] Rookgaard.
5. **Character bazaar statistics.**
    - [ ] Monitoring active auctions.
    - [ ] History of finished auctions.
    - [ ] Price statistics.
6. **Boss information.**
    - [ ] Boss list.
    - [ ] Boss statistics.
7. **Calculators.**
   - [ ] Training calculator.
   - [ ] Loot calculator.
   - [ ] Stamina calculator.

# Stack

**Back-end:** Django, Python

**Database:** MySQL

**Front-end:** HTML5, CSS3, Bootstrap, JavaScript

# Structure
```bash
tibia_stats
   |-- logs
   |-- main
   |   |-- migrations
   |   `-- templatetags
   |-- scripts
   |   |-- database
   |   |-- json_files
   |   |-- proxy_scrapper
   |   |-- tibiacom_scrapper
   |   `-- tibiadata_API
   |-- static
   |   `-- root
   |       |-- admin
   |       |-- css
   |       |-- django_extensions
   |       |-- js
   |       |-- lib
   |       `-- scss
   |-- tasks
   |-- temp
   |-- templates
   |   `-- sites
   |       |-- bazaar
   |       |-- bosses
   |       |-- calculators
   |       |-- characters
   |       |-- charms
   |       |-- experience
   |       `-- worlds
   |-- tibia_stats
```


# Requirements
- Sentry account
- MySQL server 8.0

```bash
beautifulsoup4==4.11.1
bs4==0.0.1
Django==4.1.3
django-extensions==3.2.1
idna==3.4
lxml==4.9.1
mysql-connector-python==8.0.31
mysqlclient==2.1.1
pandas==1.5.2
requests==2.28.1
urllib3==1.26.13
python-dotenv==0.21.0
sentry-sdk==1.14.0
psutil~=5.9.4
```

# Installation

The installation manual includes all the necessary steps, including configuring the MySQL database,
downloading all required libraries and modules and starting the application server.
After installation is complete and the server is up and running, the application will be available
for use via a web browser on your own computer.

Check your python version by typing
```python --version``` To run application you need python 3.10

<a href="https://github.com/jakubg89/tibia_stats/archive/refs/heads/main.zip">Download repository </a>
and extract files.

### .env
- Create .env file in directory ```tibia_stats```
- Paste following code with needed information:
```bash
DSN= your sentry information
SECRET_KEY= your secret key
DEBUG=False
ALLOWED_HOSTS=localhost 127.0.0.1
DB_NAME=tibia_stats
DB_USER= your db user name
DB_PASSWORD= password to your database
DB_HOST=127.0.0.1
DB_PORT=3306
```

### Prepare environment
- Update pip ```python -m pip install -U pip```
- Install virtual environment ```pip install virtualenv```
- Create your virtual environment ```python -m venv your_virtual_environment_name```
- Activate virtual environment ```source /path_to/your_virtual_environment/bin/activate```
- Install requirements from file ```pip install -r setup-requirements.txt```

### MySQL
- Create database ```tibia_stats```

### Django
Create demo project to obtain ```SECRET_KEY``` for your app

- Create project ```django-admin startproject demo```
- Navigate to ```settings.py``` of your demo project and copy your ```SECRET_KEY``` to
```.env``` file.
- Navigate to directory with ```manage.py```
- Make migrations ```python manage.py makemigrations```
- Migrate ```python manage.py migrate```
- Run server ```python manage.py runserver```

You can now access app by opening ```http://127.0.0.1:8000/``` in your browser.