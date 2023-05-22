##create python virtual environment
* ->pip install virtualenv
* ->go to project path using cd in terminal
* ->python<version> -m venv <virtual-environment-name>
* ->source environment-name/bin/activate

* #install project requirements dependencies
* ->pip install -r requirements.txt

##mysql localhost setup
* ->for windows
* https://www.sqlshack.com/how-to-install-mysql-database-server-8-0-19-on-windows-10/
* ->for macOS
* https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/macos-installation-pkg.html

##populate world.sql file in database
//from workbench
* ->open workbench connect database with credentials
* ->click on Data Import/Restore > Import from Self-Contained file > choose world.sql file > Start Import

//from terminal
* ->mysql -u root -p
* ->enter root password
* ->create database world;
* ->mysql -u root -p world
* ->source world.sql  
* ->quit

 
##setup database
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

##setupt smtp mail sending
* ->open PanorbitBackendAssignment > settings.py
* EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
* EMAIL_HOST = 'smtp.gmail.com'
* EMAIL_HOST_USER = ''
* EMAIL_HOST_PASSWORD = ''
* EMAIL_PORT = 587
* EMAIL_USE_TLS = True
* DEFAULT_FROM_EMAIL = ''

##migrate models
* ->python manage.py makemigrations
* ->python manage.py migrate

##run project
* ->python manage.py runserver

* Note: Project path is mandatory to open in terminal to execute all commands

##api endpoints

//signup
* ->http://127.0.0.1:8000/api/signup
* ->method- POST
* -> request body
* {
*     "first_name":"",
*     "last_name":"",
*     "email":"",
*     "gender":"M", //('M', 'Male'),('F', 'Female'),('O', 'Other')
*     "phone_number":""
* }

//login
* ->http://127.0.0.1:8000/api/login
* ->method- POST
* {
*     "mobile":""
* }

//otp verify
* ->http://127.0.0.1:8000/api/otp_verify/{phone_number}
* ->method- POST
* {
*     "otp":""
* }

//re send otp
* ->http://127.0.0.1:8000/api/re_send_otp/{phone_number}
* ->method- GET

//logout
* ->http://127.0.0.1:8000/api/logout
* ->method- DELETE