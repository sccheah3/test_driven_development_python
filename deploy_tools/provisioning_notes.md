Provisioning a new site 
= = = = = = = = = = = = = = = = = = = = = = = 
## Required packages: 

* nginx 
* Python 3.6 
* pipenv + pip 
* Git 

eg, on Ubuntu: 
	sudo add-apt-repository ppa:deadsnakes/ ppa 
	sudo apt update 
	sudo apt install nginx git python3.6 python3.6-venv -- get pip and pipenv instead

## Nginx Virtual Host config 
* see nginx.template.conf 
* replace DOMAIN with, e.g., staging.my-domain.com 

## Systemd service 
* see gunicorn-systemd.template.service 
* replace DOMAIN with, e.g., staging.my-domain.com 

## Folder structure: 
Assume we have a user account at /home/username
/home/username
└── sites     
	├── DOMAIN1     
	│ ├── .env     
	│ ├── db.sqlite3     
	│ ├── manage.py etc     
	│ ├── static     
	│ └── virtualenv     
	└── DOMAIN2     
		├── .env     
		├── db.sqlite3     
		├── etc

## Provisioning and Deployment Procedures:
# Provisioning
1. Assume we have a user account and home folder
2. $ add-apt-repository ppa:deadsnakes/ppa && apt update
3. apt install nginx git python3.6 python3.6-venv
4. Add Nginx config for virtual host
5. Add Systemd job for Gunicorn (including unique SECRET_KEY)

# Deployment
1. Create directory in ~/sites
2. Pull down source code
3. Start virtualenv in *virtualenv* 
4. $ pip install -r requirements.txt
5. $ python manage.py migrate [--noinput] --- for database
6. $ python manage.py collectstatic [--noinput] --- for staticfiles
7. Restart Gunicorn job
8. Run FTs to check everything works