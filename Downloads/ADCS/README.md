
## Audio Data Collection System
Welcome to our system.Audio Data System is the fully dynamic IVR system powered by Asterisk. Where you can make your own sets of IVR by telephone as well as web interface,select your own project short code number,view response,add more and more project.

## Installation
Clone the repository

     $ git@gitlab.yipl.com.np:system/asterisk-system.git 

Chane into the directory and create a virtual environment ('mkvirtualenv')

     $ cd asterisk-system
     $ mkvirtualenv 'virtualenv_name'

Install dependencies:

    $ pip install -r requirement.txt

Edit the configuration files(models.py) and make sure that you have set a valid database URL. 

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/databasename'

Then run the application.in a local instance you can just do:

    $ cd asterisk-system
    $ python runserver.py


## Troubleshooting:
  * Make sure you have given permission to the upload folder to the server user.    


## License     
        
