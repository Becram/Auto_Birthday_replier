# project/__init__.py

from flask import Flask, render_template, request, session
from flask.ext.sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.config.update(
        DEBUG=True,
        SQLALCHEMY_DATABASE_URI='mysql://root:yipl123@localhost/adcs',
    )
db = SQLAlchemy(app)



UPLOAD_FOLDER = 'static/audio'
ALLOWED_EXTENSIONS = set(['wav'])
app = Flask(__name__)

app.secret_key = 'development key'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'contact@example.com'
app.config["MAIL_PASSWORD"] = 'your-password'



# Database setting for mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:yipl123@localhost/adcs'
# app.config['DEFAULT_FILE_STORAGE'] = 'filesystem'
# app.config['UPLOADS_FOLDER'] = os.path.realpath('.') + '/static/music/'
# app.config['FILE_SYSTEM_STORAGE_FILE_VIEW'] = 'static/music'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



