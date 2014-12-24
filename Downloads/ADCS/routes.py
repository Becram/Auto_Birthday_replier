import os
from flask import render_template, request, flash,session, url_for, redirect
from forms import ContactForm,SignupForm,SigninForm,AddprojecForm,AddquestionForm,EditquestionForm
from flask.ext.mail import Message, Mail
from models import db,app
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from models import User,Organization,Project,Question,Answer
from werkzeug import secure_filename
mail = Mail()


UPLOAD_FOLDER = 'static/audio/'
ALLOWED_EXTENSIONS = set(['wav'])

app.secret_key = 'development key'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'contact@example.com'
app.config["MAIL_PASSWORD"] = 'your-password'

mail.init_app(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# flask-migrate 
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def authenticate():
  if 'name' in session:
    return True
  else:
    return False


# test MySql DataBase setting
@app.route('/testdb')
def testdb():
  if db.session.query("1").from_statement("SELECT 1").all():
    return 'It works.'
  else:
    return 'Something is broken.'


# Home page
@app.route('/')
def home():
  return render_template('home.html')


# About page
@app.route('/about')
def about():
  return render_template('about.html')



# Contact Page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()

  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender='contact@example.com', recipients=['your_email@example.com'])
      msg.body = """
      From: %s <%s>
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)

      return render_template('contact.html', success=True)

  elif request.method == 'GET':
    return render_template('contact.html', form=form)



# SignUp page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.firstname.data,form.lastname.data,form.email.data,form.code.data,form.password.data)
      db.session.add(newuser)
      db.session.commit()
      
      session['code'] = newuser.code
      return redirect(url_for('profile'))

  elif request.method == 'GET':
    return render_template('signup.html', form=form)  



# Project page
@app.route('/project')
def profile():
  if authenticate()==False:
    return redirect(url_for('signin'))
 
  if 'admin_call_code' not in session:
    return redirect(url_for('signin'))
 
  admin_call_code = Organization.query.filter_by(admin_call_code = session['admin_call_code']).first()
  project = Project.query.filter_by(org_id=admin_call_code.id).all()

 
  if admin_call_code is None:
    return redirect(url_for('signin'))
  else:
    return render_template('profile.html', project=project) 


# SignIn Page
@app.route('/signin', methods=['GET', 'POST'])
def signin():

  form = SigninForm()
  if authenticate():
    return redirect(url_for('profile'))

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['admin_call_code'] = form.admin_call_code.data
      # print session['admin_call_code']
      return redirect(url_for('profile'))
                 
  elif request.method == 'GET':
    return render_template('signin.html', form=form)  



# SignOut Page
@app.route('/signout')
def signout():
 
  if 'name' not in session:
    return redirect(url_for('signin'))
     
  session.pop('name', None)
  return redirect(url_for('home'))  


# Add Project Page
@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
  form = AddprojecForm()
  if authenticate()==False:
    return redirect(url_for('signin'))
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('add_project.html', form=form)
    else:
      file = request.files['start_info_file']
      start_file_exist = 0
      filename = ''
      if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if filename:
          file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
          start_file_exist = 1


      file = request.files['concluding_info_file'] 
      conclude_file_exist = 0
      conclude_filename = ''
      if file and allowed_file(file.filename):
        conclude_filename = secure_filename(file.filename)
        if conclude_filename:
          file.save(os.path.join(app.config['UPLOAD_FOLDER'], conclude_filename))
          conclude_file_exist = 1

      newproject = Project(session['id'],form.project_title.data,form.user_call_code.data,start_file_exist,0,filename,conclude_filename,conclude_file_exist)
      db.session.add(newproject)
      db.session.commit()


      return redirect(url_for('profile'))

  elif request.method == 'GET':
    return render_template('add_project.html', form=form)

# Project Page
@app.route('/project_page/<int:id>')   
def project_page(id):
  project_page = Project.query.get(id)
  organizations = Organization.query.join(Project,Project.org_id==Organization.id)
  for organization in organizations:
    question = db.session.query(Question).filter(Question.project_id==id,organization.admin_call_code==session['admin_call_code'])
    print question

  return render_template('project_page.html',project_page=project_page,question=question)

@app.route('/project_page/add_question/<int:id>',methods=['GET','POST'])
def add_question(id):
  form = AddquestionForm()
  project_page = Project.query.get(id)
  if request.method == 'POST':
    file = request.files['question']
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER']+project_page.user_call_code+'/question/', filename))
      question = Question(project_page.id,filename,form.question_type.data)
      db.session.add(question)
      db.session.commit()


      return redirect(url_for('project_page',
                                    id=project_page.id))

  elif request.method == 'GET':
    return render_template('add_question.html', form=form,project_page=project_page)




# Edit question Page
@app.route('/project_page/edit_question/<int:id>',methods=['GET','POST'])
def edit_question(id):
  edit_question = Question.query.get(id)
  project=Project.query.get(edit_question.project_id)
  form = EditquestionForm(obj=edit_question)
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('edit_question.html',form=form,edit_question=edit_question)
    else:
      file = request.files['question']
      filename = secure_filename(file.filename)
      if filename:
        file.save(os.path.join(app.config['UPLOAD_FOLDER']+project.user_call_code+'/question/', filename))
        edit_question.question = filename
        edit_question.question_type = form.question_type.data
        db.session.add(edit_question)
        db.session.commit()
        print "edit change"
        return redirect(url_for('project_page',id=edit_question.project_id))
      else:
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # edit_question.question = filename
        edit_question.question_type = form.question_type.data
        db.session.add(edit_question)
        db.session.commit()
        print "edit change"
        return redirect(url_for('project_page',id=edit_question.project_id))


  elif request.method == 'GET':
    return render_template('edit_question.html',form=form,edit_question=edit_question)


# Delete project 
@app.route('/project_page/delete/<int:id>', methods=['GET'])
def delete(id):
    """Delete an uploaded file."""
    delete_question = Question.query.get_or_404(id)
    project=Project.query.get(delete_question.project_id)
    project_id=delete_question.project_id
    os.remove(os.path.join(app.config['UPLOAD_FOLDER']+project.user_call_code+'/question/',delete_question.question))
    # print upload.id
    db.session.delete(delete_question)
    db.session.commit()
    
    return redirect(url_for('project_page',id=project_id))


# View Response
@app.route('/question/view_response/<int:id>', methods=['GET'])
def view_response(id):
    project = Project.query.get(id)
    answers = Answer.query.with_entities(Answer.time,Answer.phone_number,Answer.question_id,Answer.project_id).\
              group_by(Answer.time,Answer.phone_number).filter(Answer.project_id==id).all()         
    return render_template('view_response.html',answers=answers,project=project)   

# View Detail
@app.route('/question/view_response/detail/<int:id>/<phone_number>/<time>',methods=['GET'])
def view_detail(id,phone_number,time):
    project= Project.query.get(id)
    answers = Answer.query.join(Question,Question.id==Answer.question_id).\
               filter(Answer.phone_number==phone_number,Answer.time==time)  
  

    return render_template('view_detail.html',project=project,phone_number=phone_number,time=time,answers=answers)  

 
@app.after_request
def remove_if_invalid(response):
    if "__invalidate__" in session:
        response.delete_cookie(app.session_cookie_name)
    return response

# 404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404    

# Logout
@app.route("/logout")
def logout():
    session["__invalidate__"] = True
    return redirect(url_for("home"))    

if __name__ == '__main__':
  manager.run()

