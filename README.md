# SANscript

An application for SAN monitoring written in Python using Django, supports HP EVA, HP 3PAR, HDS AMS storages and Brocade FC switches.

### Installation on Debian 8

Install python3 and git
```bash
apt-get install python3 python3-pip
apt-get install git
```
Install application
```bash
mkdir /home/django/
cd /home/django/
git clone https://github.com/tulsluper/sanscript.git
cd sanscript
pip3 install -r requirements.txt
./manage.py migrate
./manage.py createsuperuser
chown -R www-data:www-data ../sanscript
```
Install uwsgi and nginx
```bash
apt-get install uwsgi uwsgi-plugin-python3
apt-get install nginx
```
Copy uwsgi and nginx configs:
```bash
cp /home/django/sanscript/configs/uwsgi/sanscript.ini /etc/uwsgi/apps-available/
cp /home/django/sanscript/configs/nginx/sanscript.conf /etc/nginx/sites-available/
```
Enable configs:
```bash
ln -s /etc/uwsgi/apps-{available,enabled}/sanscript.ini
ln -s /etc/nginx/sites-{available,enabled/sanscript.conf 
```
Disable default nginx config:
```bash
rm /etc/nginx/sites-enabled/default
```
Restart uwsgi and nginx:
```bash
service uwsgi restart
service nginx restart
```
Now application should be available in browser on http://domain_name/ or http://ip_address/
