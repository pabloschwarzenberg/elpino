#!/bin/bash
#como root
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
cp /home/elpino/elpino/hepapp.fundacionelpino.cl.conf /etc/apache2/sites-enabled/
systemctl restart apache2
mysql < /home/elpino/elpino/elpino.sql
pip3 install virtualenv
#como elpino
su - elpino
python3 elpino/secret.py >> ~/.bashrc
exit
su - elpino
virtualenv venv
source venv/bin/activate
cd elpino
pip3 install -r requirements.txt
cd elpino
#cambiar a mysql en settings.py
vi settings.py
cd ..
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
exit
#como root
service apache2 restart
apt-get install supervisor
cp /home/elpino/elpino/elpino.conf /etc/supervisor/conf.d/
service supervisor stop
service supervisor start

apt-get update
apt-get install software-properties-common
add-apt-repository universe
add-apt-repository ppa:certbot/certbot
apt-get update

apt-get install certbot python-certbot-apache
certbot --apache