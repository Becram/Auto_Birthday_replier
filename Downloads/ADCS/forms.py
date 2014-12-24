from flask.ext.wtf import Form
from flask.ext.wtf.file import FileField, FileRequired
from wtforms import TextField, TextAreaField, SubmitField, validators, PasswordField,IntegerField,BooleanField,SelectField
from models import User,Organization
from flask import session

class ContactForm(Form):
  name = TextField("Name",  [validators.Required("Please enter your name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
  message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
  submit = SubmitField("Send")


class SignupForm(Form):
  firstname = TextField("First name",  [validators.Required("Please enter your first name.")])
  lastname = TextField("Last name",  [validators.Required("Please enter your last name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  code = IntegerField('Admin Call Code',  [validators.required()])
  password = PasswordField('Admin Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Create account")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    code = User.query.filter_by(code = self.code.data).first()
    if code:
      self.code.errors.append("That Admin Call code is already taken")
      return False
    else:
      return True

# signin form using organizations table
class SigninForm(Form):
  admin_call_code = TextField("Admin Call Code",[validators.Required("Please enter your Admin Call Code.")])
  password = PasswordField('Admin Password', [validators.Required("Please enter Admin Password.")])
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    admin_call_code = Organization.query.filter_by(admin_call_code=self.admin_call_code.data).first()

    		
   
    if str(admin_call_code.password) == str(self.password.data):
      session['name'] = admin_call_code.name
      session['id']  = admin_call_code.id
      return True

    else:
    	self.admin_call_code.errors.append("Invalid Admin Code or Admin Password")
    	return False


      
#add projects form
class AddprojecForm(Form):
  project_title = TextField("Project Title",[validators.Required("Please enter Project Title")])
  user_call_code = TextField("Enter User Call Code",[validators.Required("Please enter User Call Code")])
  start_info = BooleanField("Upload start up information")
  start_info_file = FileField("Upload start up information file")
  concluding_info= BooleanField("Upload conclude information")
  concluding_info_file= FileField("Upload conclude information file")
  submit = SubmitField("Add Project")


  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False



# Add Question Form
class AddquestionForm(Form):
  question = FileField("Your question",validators=[FileRequired('no file'),
    ])
  question_type = SelectField("Question Type",choices=[(1,'audio'),(2,'dial')])
  submit = SubmitField("Upload")


  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False  

class EditquestionForm(Form):
  question = FileField("Edit question")
  question_type =  TextField("Enter Question type")
  submit = SubmitField("Upload")


  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False        
