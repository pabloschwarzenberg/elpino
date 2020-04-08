#!/bin/bash
adduser elpino
git clone https://github.com/pabloschwarzenberg/elpino.git
apt-get update
apt-get install python3-pip
apt-get install mysql-server
apt-get install libmysqlclient-dev
mysql_secure_installation
apt-get install python-dev
apt-get install libpq-dev
apt-get update
apt-get -y install apache2
a2enmod proxy
a2enmod proxy_http
a2enmod ssl
a2enmod headers
systemctl restart apache2
rm /etc/apache2/sites-enabled/*
cp servicio.conf /etc/apache2/sites-enabled
python3 secret.py >> ~/.bashrc
mysql < elpino.sql
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
service apache2 restart
apt-get install supervisor
cp elpino.conf /etc/supervisor/conf.d/
service supervisor stop
service supervisor start
