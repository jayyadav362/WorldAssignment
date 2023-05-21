* #create python virtual environment
* ->pip install virtualenv
* ->go to project path using cd in terminal
* ->python<version> -m venv <virtual-environment-name>
* ->source environment-name/bin/activate
* 
* #install project requirements dependencies
* ->pip install -r requirements.txt
* 
* #mysql localhost setup
* ->for windows
* https://www.sqlshack.com/how-to-install-mysql-database-server-8-0-19-on-windows-10/
* ->for macOS
* https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/macos-installation-pkg.html
* 
* #populate world.sql file in database
* //from workbench
* ->open workbench connect database with credentials
* ->click on Data Import/Restore > Import from Self-Contained file > choose world.sql file > Start Import
* 
* //from terminal
* ->mysql -u root -p
* ->enter root password
* ->create database world;
* ->mysql -u root -p world
* ->source world.sql  
* ->quit
* 
* 
* #setup database
* ->open PanorbitBackendAssignment > settings.py
* DATABASES = {
*     'default': {
*         'ENGINE': 'django.db.backends.mysql',
*         'NAME': 'world',
*         'USER': '',
*         'PASSWORD': ''
*         'HOST': '127.0.0.1',
*         'PORT': '3306',
*     }
* }
* 
* #migrate models
* ->python manage.py makemigrations
* ->python manage.py migrate
* 
* #run project
* ->python manage.py runserver
* 
* Note: Project path is mandatory to open in terminal to execute all commands