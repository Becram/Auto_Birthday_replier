from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug import generate_password_hash, check_password_hash
 
db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:yipl123@localhost/adcstest'
db = SQLAlchemy(app)
db.create_all()
 
class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  code = db.Column(db.Integer,unique=True)
  pwdhash = db.Column(db.String(54))
   
  def __init__(self, firstname, lastname, email, code,password):
    self.firstname = firstname
    self.lastname = lastname
    self.email = email.lower()
    self.code = code
    print self.code
    self.set_password(password)
     
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)
   
  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

class Organization(db.Model):
  __tablename__ = 'organizations'
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(255))
  created_time = db.Column(db.DateTime(), default=datetime.utcnow)
  admin_call_code = db.Column(db.String(255))
  password = db.Column(db.Integer)
  projects = db.relationship('Project',backref='organizations',lazy='dynamic')


  def __init__(self,name,admin_call_code,password):
    self.name = name 
    self.admin_call_code = admin_call_code
    self.password = password
   



class Project(db.Model):
  __tablename__ = 'projects'
  id = db.Column(db.Integer, primary_key = True)
  org_id = db.Column(db.Integer,db.ForeignKey('organizations.id'))
  project_title = db.Column(db.String(70))
  created_time = db.Column(db.DateTime(), default=datetime.utcnow)
  user_call_code = db.Column(db.String(40),unique=True)
  start_info = db.Column(db.String(50)) 
  start_info_file = db.Column(db.String(255))
  concluding_info = db.Column(db.String(255))
  concluding_info_file = db.Column(db.String(255))
  total_response = db.Column(db.Integer)
  questions = db.relationship('Question',backref='projects',lazy='dynamic')
  answers = db.relationship('Answer',backref='projects',lazy='dynamic')


  def __init__(self,org_id,project_title,user_call_code,start_info,total_response,start_info_file,concluding_info_file,concluding_info):
    self.org_id = org_id
    self.project_title = project_title
    self.user_call_code = user_call_code
    self.start_info = start_info
    self.total_response = total_response
    self.start_info_file = start_info_file
    self.concluding_info_file = concluding_info_file
    self.concluding_info = concluding_info
  
  


    def __repr__(self):
      return 'project_title' % self.project_title

class Question_Type(db.Model):
  __tablename__ = 'question_types'
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(50))

  def __init__(self,name):
    self.name = name

  def __repr__(self):
    return 'Name' % self.name

class Question(db.Model):
  __tablename__ = 'questions'
  id = db.Column(db.Integer, primary_key = True)
  project_id = db.Column(db.Integer,db.ForeignKey('projects.id'))
  question = db.Column(db.String(255))
  question_type = db.Column(db.String(50))
  answers = db.relationship('Answer',backref='questions',lazy='dynamic')
 

  def __init__(self,project_id,question,question_type):
    self.project_id = project_id
    self.question = question
    self.question_type = question_type
    


  def __repr__(self):
    return 'Question' % self.question

class Answer(db.Model):
  __tablename__ = 'answers'
  id = db.Column(db.Integer, primary_key = True)
  time = db.Column(db.DateTime(), default=datetime.utcnow)
  project_id = db.Column(db.Integer,db.ForeignKey('projects.id'))
  question_id = db.Column(db.Integer,db.ForeignKey('questions.id'))
  phone_number = db.Column(db.String(100))
  answer = db.Column(db.String(255))


  def __init__(self,phone_number,answer):
    self.phone_number = phone_number
    self.answer = answer
    
    



 






