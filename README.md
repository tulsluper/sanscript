# SANscript

An application for SAN monitoring written in Python using Django, supports HP EVA, HP 3PAR, HDS AMS storages and Brocade FC switches.

### Installation on Debian 8

Install python3 and other packages
```bash
apt-get install python3 python3-dev python3-pip
apt-get install git
apt-get install libldap2-dev libsasl2-dev
```
Download application and install requirements
```bash
mkdir /home/django/
cd /home/django/
git clone https://github.com/tulsluper/sanscript.git
cd sanscript
pip3 install -r requirements.txt
```
Configure database

If you use SQLite:

no actions needed

If you use PostgreSQL:
```
apt-get install postgresql
apt-get install python3-psycopg2
```
```
su - postgres
psql -f /home/django/sanscript/configs/db_init_postgres.sql
exit
```
Change database config in /home/django/sanscript/sanscript/settings.py
```
DATABASES = {
    'default': {

        # comment out lines below for sqlite3
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

        # comment out lines below for postgresql
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sanscriptdb',
        'USER': 'sanscriptdbuser',
        'PASSWORD': 'sanscriptdbpass',
        'HOST':'localhost',
        'PORT':'',
    }
}
```
Init application
```bash
./manage.py migrate auth
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
ln -s /etc/nginx/sites-{available,enabled}/sanscript.conf 
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
