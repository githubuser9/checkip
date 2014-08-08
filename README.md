CHECKIP
=======

Installation on Ubuntu 12.04

Install Apache2
--------------

	$ apt-get install apache2


Install mod-wsgi
--------------

	$ apt-get install libapache2-mod-wsgi 
	$ a2enmod wsgi 


Install MySQL
--------------

	$ apt-get install mysql-server libapache2-mod-auth-mysql
	$ apt-get install libmysqlclient-dev
	$ mysql_install_db
	$ /usr/bin/mysql_secure_installation

Create database:

	$ mysql -u root -p
	mysql> create database checkip;

View data in database:

	mysql> use checkip;
	mysql> select * from log_table;


Install pip and virtualenv
--------------

	$ apt-get install python-pip python-dev build-essential 
	$ pip install --upgrade pip 
	$ pip install --upgrade virtualenv

Load project to /var/www/checkip/ directory or another, setup virtualenv and pip packages:

	$ cd /var/www/checkip/
	$ virtualenv venv
	$ . venv/bin/activate
	$ pip install -r requirements.txt


Make apache config
--------------

	$ nano /etc/apache2/sites-available/checkip.conf

Input:

	<VirtualHost *:80>
					ServerName 188.226.243.110  # Your domain or server ip address
					ServerAdmin admin@localhost
					WSGIScriptAlias / /var/www/checkip.wsgi
					<Directory /var/www/checkip/>
							Order allow,deny
							Allow from all
					</Directory>
					Alias /static /var/www/checkip/application/static
					<Directory /var/www/checkip/application/static/>
							Order allow,deny
							Allow from all
					</Directory>
					ErrorLog ${APACHE_LOG_DIR}/error.log
					LogLevel warn
					CustomLog ${APACHE_LOG_DIR}/access.log combined
	</VirtualHost>


Enable virtualhost:

	$ a2ensite checkip


**Create the .wsgi File**

	$ cd /var/www/
	$ nano checkip.wsgi 
	
Input:

	import sys
	import os
	import logging
	logging.basicConfig(stream=sys.stderr)


	activate_env=os.path.expanduser("/var/www/checkip/venv/bin/activate_this.py")
	execfile(activate_env, dict(__file__=activate_env))

	sys.path.insert(0,"/var/www/checkip/")

	from application.core import app as application
	application.secret_key = 'Qdas34!@3FEwf3.#4Rqfew'  # Change to your random secret key

	if __name__ == '__main__':
		application.run()


Restart apache:

	$ service apache2 restart
	

Run tests
--------------

	$ python tests.py

	Successful result:
	
	......
	----------------------------------------------------------------------
	Ran 6 tests in 0.059s

	OK
