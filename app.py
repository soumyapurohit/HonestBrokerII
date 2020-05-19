from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from flask_bootstrap import Bootstrap
from math import log, exp, floor
from decimal import *
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, RadioField, SelectField, HiddenField
from wtforms.validators import InputRequired, Email, Length
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy.engine import Engine
from sqlalchemy import event, Sequence
import os
import psycopg2
from datetime import datetime
from wtforms_sqlalchemy.fields import QuerySelectField
#from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:////flask-application/building_user_login_system/start/database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
#conn = psycopg2.connect("host=hbcdm.ce9qkwq3sggt.us-east-1.rds.amazonaws.com dbname=hbcdm user=hbadmin password=hbaccess")
#cur = conn.cursor()
conn = psycopg2.connect("host=hbcdm.cpnsaiphh4ed.us-east-1.rds.amazonaws.com dbname=hbcdm user=hbadmin password=hbaccess")
cur = conn.cursor()
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    requests = db.relationship('RequestForm', backref = 'user', lazy = 'dynamic')

class Dataset(UserMixin, db.Model):
    datasetid = db.Column(db.Integer, primary_key=True)
    nameset = db.Column(db.String(40))
    dataset_risk = db.Column(db.Integer)
    accept_risk = db.Column(db.Integer)
    datasets = db.relationship('RequestForm', backref = 'dataset', lazy = 'dynamic')

class RequestForm(UserMixin, db.Model):
    requestid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    requestname = db.Column(db.String(40))
    requestDescription = db.Column(db.String(40))
    use = db.Column(db.String(40))
    store = db.Column(db.String(40))
    longdata = db.Column(db.String(40))
    soondata = db.Column(db.String(40))
    typeofdata = db.Column(db.String(40))
    status = db.Column(db.String(40))
    risk_level = db.Column(db.String(40))
    ownerid= db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False) 
    datasetid =db.Column(db.Integer, db.ForeignKey('dataset.datasetid'), nullable=False)
    #requests = db.relationship('RequestForm', backref = 'user', lazy = True)
    #datasets = db.relationship('RequestForm', backref = 'dataset', lazy = True)
class IrbInfo(UserMixin, db.Model):
    irbunique = db.Column(db.Integer, primary_key = True, autoincrement = True)
    irb_id = db.Column(db.String(10))

class ItemInfo(UserMixin, db.Model):
    itemid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    itemname = db.Column(db.String(40))
    itemunique = db.Column(db.String(10))

# Minh's note: Yes, No, and Uncertain.
class TrustChoice(UserMixin, db.Model):
    trustchoiceid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    decision = db.Column(db.String(40))
    #trustchoices = db.relationship('TrustCalcForm', backref = 'trust_choice', lazy = 'dynamic')

class IdentifierChoice(UserMixin, db.Model):
    identifierchoiceid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    decision = db.Column(db.String(40))
	
# Minh's note: Old trust calculation form - commented.
'''
class TrustCalcForm(UserMixin, db.Model):
    trustid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    radiology_images = db.Column(db.String(10))
    radiology_imaging_reports = db.Column(db.String(10))
    ekg = db.Column(db.String(10))
    progress_notes = db.Column(db.String(10))
    history_phy = db.Column(db.String(10))
    oper_report = db.Column(db.String(10))
    path_report = db.Column(db.String(10))
    lab_report = db.Column(db.String(10))
    photographs = db.Column(db.String(10))
    #ssn = db.Column(db.String(10))
    discharge_summaries = db.Column(db.String(10))
    health_care_billing = db.Column(db.String(10))
    consult = db.Column(db.String(10))
    medication = db.Column(db.String(10))
    emergency = db.Column(db.String(10))
    dental = db.Column(db.String(10))
    demographic = db.Column(db.String(10))
    question = db.Column(db.String(10))
    audiotape = db.Column(db.String(10))
    #other = db.Column(db.String(10))
    match = db.Column(db.String(10))
    mismatch = db.Column(db.String(10))
    undecided = db.Column(db.String(10))
    beta = db.Column(db.String(10))
    dirichlet = db.Column(db.String(10))
    status = db.Column(db.String(10))
    ownerid= db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
   # trustchoiceid = db.Column(db.Integer, db.ForeignKey('trust_choice.trustchoiceid'), nullable=False)
'''
   
# Minh's note: New trust calculation form.
class TrustCalcForm(UserMixin, db.Model):
    trustid = db.Column(db.Integer, primary_key = True, autoincrement = True)
	
    # Identifier cartegories.
    personal_id = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    race = db.Column(db.String(10))
    birth_year = db.Column(db.String(10))
    birth_month = db.Column(db.String(10))
    birth_day = db.Column(db.String(10))
    birth_time = db.Column(db.String(10))
    location = db.Column(db.String(10))
    provider = db.Column(db.String(10))
    care_site = db.Column(db.String(10))
    ethnicity = db.Column(db.String(10))
	
    # Domain cartegories.
    condition = db.Column(db.String(10))
    device_condition = db.Column(db.String(10))
    drug_condition = db.Column(db.String(10))
    measurement_condition = db.Column(db.String(10))
    observation_condition = db.Column(db.String(10))
    procedure_condition = db.Column(db.String(10))
	
    device = db.Column(db.String(10))
    drug_device = db.Column(db.String(10))
    observation_device = db.Column(db.String(10))
    procedure_device = db.Column(db.String(10))
	
    drug = db.Column(db.String(10))
    measurement_drug = db.Column(db.String(10))
    observation_drug = db.Column(db.String(10))
    procedure_drug = db.Column(db.String(10))
	
    measurement = db.Column(db.String(10))
    observation_measurement = db.Column(db.String(10))
    procedure_measurement = db.Column(db.String(10))
	
    observation = db.Column(db.String(10))
    procedure_observation = db.Column(db.String(10))
	
    procedure = db.Column(db.String(10))
	
    visit = db.Column(db.String(10))
	
    specimen = db.Column(db.String(10))
	
    # Trust calc.
    match = db.Column(db.String(10))
    mismatch = db.Column(db.String(10))
    undecided = db.Column(db.String(10))
    beta = db.Column(db.String(10))
    dirichlet = db.Column(db.String(10))
    status = db.Column(db.String(10))
    ownerid= db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
   # trustchoiceid = db.Column(db.Integer, db.ForeignKey('trust_choice.trustchoiceid'), nullable=False)

class IdentifierCalcForm(UserMixin, db.Model):
    identifier_id = db.Column(db.Integer, Sequence('IRB'), primary_key = True, autoincrement = True)
    irb_description = db.Column(db.String(40))
    person_id = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    race = db.Column(db.String(10))
    year_of_birth = db.Column(db.String(10))
    month_of_birth = db.Column(db.String(10))
    day_of_birth = db.Column(db.String(10))
    time_of_birth = db.Column(db.String(10))
    location = db.Column(db.String(10))
    provider = db.Column(db.String(10))
    care_site =  db.Column(db.String(10))
    ethnicity = db.Column(db.String(10))
    ownerid= db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    

#class SelectFieldtypedata(db.Model):
#    datatype = db.Column(db.String(40))

#class ChoiceOpts(FlaskForm):
#    opts = QuerySelectField(query_factory = choice_dataset, allow_blank =True)
def choice_identifier():
    return IdentifierChoice.query

def choice_irb():
    return IrbInfo.query

def choice_trustcalc():
    return TrustChoice.query

def choice_dataset():
    return Dataset.query


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()



#def choice_typeofdata():
#    return SelectFieldtypedata.query

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length( max=45)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])

class CreateRequestForm(FlaskForm):
    requestname = StringField('Title', validators=[InputRequired(), Length(min=4, max=15)])
    requestDescription =  StringField('Description', validators=[InputRequired(), Length(min=4, max=40)])
    #datasetname =StringField('Which dataset are you trying to access', validators=[InputRequired(), Length(min=4, max=60)]) 
    datasetname = QuerySelectField(query_factory=choice_dataset, allow_blank=True, get_label = 'nameset')
    use =StringField('How will you use the data', validators=[InputRequired(), Length(min=4, max=40)])
    store=StringField('How will you store data', validators=[InputRequired(), Length(min=4, max=40)])
    longdata=StringField('How long data needs to be accessible', validators=[InputRequired(), Length(min=4, max=40)])
    soondata=StringField('How soon data needs to be accessible', validators=[InputRequired(), Length(min=4, max=40)])
    #dstype = QuerySelectField(query_factory=choice_typeofdata, allow_blank=True)
    typeofdata=StringField('What type of data would you like to receive', validators=[InputRequired(), Length(min=4, max=40)])

# Minh's note: Old class.
'''
class CreateTrustCalcForm(FlaskForm):
    #CaStatus = QuerySelectField('Enter your choice', choices=[('Yes', 'Yes'), ('No', 'No'), ('Uncertain', 'Uncertain')])
   
     irb_id = QuerySelectField(query_factory=choice_irb, allow_blank=True, get_label = 'irb_id')
     radiology_images = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     radiology_imaging_reports = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     ekg = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     progress_notes = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     history_phy = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     oper_report = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     path_report = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     lab_report = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     photographs  = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     #ssn = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     discharge_summaries = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     health_care_billing = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     consult = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     medication = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     emergency = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     dental = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     demographic = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     question = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     audiotape = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     #other = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
'''

# Minh's note: new class.
class CreateTrustCalcForm(FlaskForm):
     #CaStatus = QuerySelectField('Enter your choice', choices=[('Yes', 'Yes'), ('No', 'No'), ('Uncertain', 'Uncertain')])
     irb_id = QuerySelectField(query_factory=choice_irb, allow_blank=True, get_label = 'irb_id')
	 
     # Identifier cartegories.
     personal_id = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     gender = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     race = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     birth_year = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     birth_month = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     birth_day = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     birth_time = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     location = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     provider = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     care_site  = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     ethnicity = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
	 
     # Domain cartegories.
     condition = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     device_condition = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     drug_condition = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     measurement_condition = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     observation_condition = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     procedure_condition = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
	 
     device = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     drug_device = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     observation_device = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     procedure_device = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
	 
     drug = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     measurement_drug = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     observation_drug = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     procedure_drug = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
	 
     measurement = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     observation_measurement = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     procedure_measurement = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
	 
     observation = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     procedure_observation = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
	 
     procedure = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
	 
     visit = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
	 
     specimen = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')

class CreateIdentifierForm(FlaskForm):
    #person_id = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    #identifier_id = HiddenField("Field1")
    irb_description = StringField('Description', validators=[InputRequired(), Length(min=4, max=40)])
    person_id = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    gender = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    race = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    year_of_birth = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    month_of_birth = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    day_of_birth = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    time_of_birth = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    location = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    provider = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    care_site = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    ethnicity = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    #irb_id = QuerySelectField(query_factory=choice_irb, allow_blank=True, get_label = 'irb_id')
    condition = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    condition_device = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    condition_drug = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    condition_measurement = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    condition_observation = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    condition_procedure = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    device  = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    device_drug = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    device_observation = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    device_procedure = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    drug = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    drug_measurement = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    drug_observation = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    drug_procedure = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    measurement = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    measurement_procedure = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    measurement_observation = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    observation = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    observation_procedure=QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    procedure = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    visit = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')
    specimen = QuerySelectField(query_factory=choice_identifier, allow_blank=True, get_label = 'decision')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
        return '<h1> Invalid Username or password </h1>'

        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        flash("Registration successful!", "success")
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return '<h1> New user has been registered</h1>'

        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    #conn = psycopg2.connect("host=hbcdm.ce9qkwq3sggt.us-east-1.rds.amazonaws.com dbname=hbcdm user=hbadmin password=hbaccess")
    #cur = conn.cursor()
    
    #result =cur.execute("SELECT dataset_risk FROM data_catalog where 'dataset_name' = %s", [datasetname])
    #stmt = "SELECT * FROM data_catalog WHERE dataset_name = %s"
   # cur.execute('SELECT * FROM data_catalog where "dataset_name" = %s', [datasetname])
    #resulset = cur.fetchone()
    #cur.execute('SELECT * FROM data_catalog where data_catalog.dataset_name = "datasetname" ')
    #resulset = cur.fetchall()
    cur.execute('SELECT * FROM data_catalog')
    resultset = cur.fetchall()


    #rows = cur.rowcount
    #query = cur.query

    #print('Rows: ', rows)
    #print('Query: ', query)

    #cur.close()


    #conn.close()
    

    pending_req = TrustCalcForm.query.filter_by(status= 'pending').all()
    approvedreq_info = TrustCalcForm.query.filter_by(status= 'approved').all()
    denyreq_info = TrustCalcForm.query.filter_by(status= 'denied').all()
    for i in pending_req:
        print("pending request id is",i.trustid)

    
    if(current_user.username == 'Admin'):
        return render_template('dashboard_admin.html', name = current_user.username, pending_req= pending_req, approvedreq_info= approvedreq_info, denyreq_info=denyreq_info, resultset=resultset)
    elif(current_user.username == 'internaluser'):
        print('internal user dashboard')
        apprInternal_info = TrustCalcForm.query.filter_by(ownerid=current_user.id ,status = 'approved').all()
        request_info = TrustCalcForm.query.filter_by(ownerid=current_user.id ,status = 'pending').all()
        deniedInternal_info = TrustCalcForm.query.filter_by(ownerid=current_user.id ,status = 'denied').all()
        for i in apprInternal_info:
            print("Internal user approved HIPAA request is ",i.trustid)
        return render_template('dashboard.html', name = current_user.username, apprInternal_info= apprInternal_info, request_info=request_info, deniedInternal_info = deniedInternal_info, resultset = resultset)
    else:
        print('external user dashboard')
        apprInternal_info = TrustCalcForm.query.filter_by(ownerid=current_user.id ,status = 'approved').all()
        print('Id for external user is Hi',current_user.id)
        request_info = TrustCalcForm.query.filter_by(ownerid=current_user.id ,status = 'pending').all()
        deniedInternal_info = TrustCalcForm.query.filter_by(ownerid=current_user.id ,status = 'denied').all()
        for i in apprInternal_info:
            print("Internal user approved request is ",i.requestname)
        return render_template('dashboard_external.html', name = current_user.username, apprInternal_info= apprInternal_info, request_info=request_info, deniedInternal_info = deniedInternal_info, resultset = resultset)
#@app.route('/dashboard_admin')
#@login_required
#def dashboad_admin():
 #   return render_template('dashboard_admin.html', name = current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/hipaaform', methods=['GET','POST'])
def hipaaform():
    print('in trust form')
    form = CreateTrustCalcForm()
    if form.validate_on_submit():
        print('Form validated')
    else:
        print(form.errors)
    return render_template('example2.html',form=form)

@app.route('/pendrequest', methods=['GET','POST'])
def pendrequest():
    print('in trust form')
    form = CreateTrustCalcForm()
    if form.validate_on_submit():
        print('Form validated')
    else:
        print(form.errors)
    return render_template('example2.html',form=form)

# Minh's note: old function.
'''
@app.route('/submithipaaform', methods=['GET','POST'])
def submithipaa():
     print(current_user.username)
     form = CreateTrustCalcForm() 
     irb_id = form.irb_id.data.irb_id

     radiology_images = form.radiology_images.data.decision
     radiology_imaging_reports = form.radiology_imaging_reports.data.decision
     ekg = form.ekg.data.decision
     progress_notes = form.progress_notes.data.decision
     history_phy = form.history_phy.data.decision
     oper_report = form.oper_report.data.decision
     path_report = form.path_report.data.decision
     lab_report = form.lab_report.data.decision
     photographs = form.photographs.data.decision
     #ssn = form.ssn.data.decision
     discharge_summaries = form.discharge_summaries.data.decision
     health_care_billing = form.health_care_billing.data.decision
     consult = form.consult.data.decision
     medication = form.medication.data.decision
     emergency  = form.emergency.data.decision
     dental = form.dental.data.decision
     demographic = form.demographic.data.decision
     question = form.question.data.decision
     audiotape = form.audiotape.data.decision
     #other = form.other.data.decision
     
     
     templist = [radiology_images, radiology_imaging_reports, ekg, progress_notes, history_phy, oper_report, path_report, lab_report, photographs, discharge_summaries, health_care_billing, consult, medication, emergency, dental, demographic, question, audiotape]
     if (current_user.username == 'internaluser'):
         userrole = 'internal_user'
     elif (current_user.username == 'externaluser'):
         userrole = 'external_user'

     
     #item_select_query = "select itemunique from item_info  where itemname = radiology_images";
     #item_info = ItemInfo.query.filter_by(itemname=radiology_images).all()

     #print('after item info')
     #print(item_info)
     #for i in item_info:
     #    print('item details',i)

     postgreSQL_select_Query = "select * from data_policy_domain  where data_policy_domain.irb_number = %s"
     cur.execute(postgreSQL_select_Query, [irb_id])
     resultset = cur.fetchone()
     print('resultset is',resultset)
     d = resultset[1:]
     
            
     countmismatch = 0
     countundecided = 0
     countmatch = 0
     for a,b in zip(templist, d):
         if (a == 'Yes' and (b == '1' or b  == None)):
             countmatch += 1
         elif (a == 'No' and b == '1'):
             countmismatch += 1
         elif (a == 'No' and b == None):
             countmatch += 1
         elif (a == 'Uncertain' and b == '1'):
             countundecided += 1
         elif (a == 'Uncertain' and b == None):
             countmatch += 1
     N = 18
     # beta model trust calculation
     alpha_c = floor(countmatch + ((countundecided*countmatch)/(countmatch+countmismatch)));
     beta_c = N - alpha_c;
     Ei = float(alpha_c + 1)/float(alpha_c + beta_c + 2);
     Ei = format(Ei, '.2f')
     print('Beta model is',Ei)
    
     
     # Formula 7 of trust model
     a = 0.7
     Eb = float(countmatch+1.0) / float(countmatch+countmismatch+countundecided+3.0)
     Eu = float(countundecided+1.0) / float(countmatch+countmismatch+countundecided+3.0)
     Ew = (Eb + a*Eu)
     
     rEw = log(Ew)/log((1-Ew))
     print('rEw',rEw)
     #rEw = log(c)
     if rEw > 0:
         wi = 1 - exp(-abs(rEw))
     elif rEw < 0:
         wi = -(1 - exp(-abs(rEw)))
     else:
         wi = 0
     wi = format(wi, '.2f')
     print('dirichlet model is', wi)
    
     status = 'pending'
     new_hipaa_request = TrustCalcForm(ownerid =  current_user.id, radiology_images = radiology_images, radiology_imaging_reports = radiology_imaging_reports, ekg = ekg, progress_notes = progress_notes, history_phy = history_phy, oper_report = oper_report, path_report = path_report, lab_report = lab_report, photographs = photographs, discharge_summaries = discharge_summaries,  health_care_billing= health_care_billing, consult = consult, medication = medication, emergency = emergency, dental  = dental, demographic = demographic,question = question, audiotape = audiotape, beta = Ei, dirichlet = wi, status = status)
     db.session.add(new_hipaa_request)
     db.session.commit()

     request_info = TrustCalcForm.query.filter_by(ownerid=current_user.id, status = 'pending').all()
     for i in request_info:
         print("the trust id is", i.trustid)
     apprInternal_info = TrustCalcForm.query.filter_by(ownerid=current_user.id, status = 'approved').all()
     deniedInternal_info = TrustCalcForm.query.filter_by(ownerid=current_user.id, status= 'denied').all()

     if(current_user.username == 'internaluser'):
         return render_template('dashboard.html', form=form, request_info=request_info, apprInternal_info=apprInternal_info, deniedInternal_info=deniedInternal_info)
     elif(current_user.username == 'externaluser'):
         return render_template('dashboard.html', form=form, request_info=request_info, apprInternal_info=apprInternal_info, deniedInternal_info=deniedInternal_info)
'''

# Minh's note: new function.
@app.route('/submithipaaform', methods=['GET','POST'])
def submithipaa():
     print(current_user.username)
     form = CreateTrustCalcForm() 
     irb_id = form.irb_id.data.irb_id

     # Identifier 
     personal_id = form.personal_id.data.decision
     gender = form.gender.data.decision
     race = form.race.data.decision
     birth_year = form.birth_year.data.decision
     birth_month = form.birth_month.data.decision
     birth_day = form.birth_day.data.decision
     birth_time = form.birth_time.data.decision
     location = form.location.data.decision
     provider = form.provider.data.decision
     care_site = form.care_site.data.decision
     ethnicity = form.ethnicity.data.decision
	 
     # Domain
     condition = form.condition.data.decision
     device_condition = form.device_condition.data.decision
     drug_condition = form.drug_condition.data.decision
     measurement_condition = form.measurement_condition.data.decision
     observation_condition = form.observation_condition.data.decision
     procedure_condition = form.procedure_condition.data.decision
	 
     device = form.device.data.decision
     drug_device = form.drug_device.data.decision
     observation_device = form.observation_device.data.decision
     procedure_device = form.procedure_device.data.decision
	 
     drug = form.drug.data.decision
     measurement_drug = form.measurement_drug.data.decision
     observation_drug = form.observation_drug.data.decision
     procedure_drug = form.procedure_drug.data.decision
	 
     measurement = form.measurement.data.decision
     observation_measurement = form.observation_measurement.data.decision
     procedure_measurement = form.procedure_measurement.data.decision
	 
     observation = form.observation.data.decision
     procedure_observation = form.procedure_observation.data.decision
	 
     procedure = form.procedure.data.decision
	 
     visit = form.visit.data.decision
	 
     specimen = form.specimen.data.decision
     
     templist = [personal_id, gender, race, birth_year, birth_month, birth_day, birth_time, location, provider, care_site, ethnicity, 
				condition, device_condition, drug_condition, measurement_condition, observation_condition, procedure_condition, 
				device, drug_device, observation_device, procedure_device, drug, measurement_drug, observation_drug, procedure_drug, 
				measurement, observation_measurement, procedure_measurement, observation, procedure_observation,
				procedure, visit, specimen]
     if (current_user.username == 'internaluser'):
         userrole = 'internal_user'
     elif (current_user.username == 'externaluser'):
         userrole = 'external_user'

     postgreSQL_select_Query = "select * from data_policy_domain  where data_policy_domain.irb_number = %s"
     cur.execute(postgreSQL_select_Query, [irb_id])
     resultset = cur.fetchone()
     print('resultset is',resultset)
     d = resultset[1:]
            
     countmismatch = 0
     countundecided = 0
     countmatch = 0
     for a,b in zip(templist, d):
         if (a == 'Yes' and (b == '1' or b  == None)):
             countmatch += 1
         elif (a == 'No' and b == '1'):
             countmismatch += 1
         elif (a == 'No' and b == None):
             countmatch += 1
         elif (a == 'Uncertain' and b == '1'):
             countundecided += 1
         elif (a == 'Uncertain' and b == None):
             countmatch += 1
     N = 33
     # beta model trust calculation
     alpha_c = floor(countmatch + ((countundecided*countmatch)/(countmatch+countmismatch)));
     beta_c = N - alpha_c;
     Ei = float(alpha_c + 1)/float(alpha_c + beta_c + 2);
     Ei = format(Ei, '.2f')
     print('Beta model is',Ei)
    
     
     # Formula 7 of trust model
     a = 0.7
     Eb = float(countmatch+1.0) / float(countmatch+countmismatch+countundecided+3.0)
     Eu = float(countundecided+1.0) / float(countmatch+countmismatch+countundecided+3.0)
     Ew = (Eb + a*Eu)
     
     rEw = log(Ew)/log((1-Ew))
     print('rEw',rEw)
     #rEw = log(c)
     if rEw > 0:
         wi = 1 - exp(-abs(rEw))
     elif rEw < 0:
         wi = -(1 - exp(-abs(rEw)))
     else:
         wi = 0
     wi = format(wi, '.2f')
     print('dirichlet model is', wi)
    
     status = 'pending'
     new_hipaa_request = TrustCalcForm(ownerid =  current_user.id, personal_id = personal_id, gender = gender, race = race, 
                                                  birth_year = birth_year, birth_month = birth_month, birth_day = birth_day, birth_time = birth_time, 
                                                  location = location, provider = provider, care_site = care_site, ethnicity = ethnicity, 
                                                  condition = condition, device_condition = device_condition, drug_condition = drug_condition, 
                                                  measurement_condition = measurement_condition, observation_condition = observation_condition, procedure_condition = procedure_condition, 
                                                  device = device, drug_device = drug_device, observation_device = observation_device, procedure_device = procedure_device, 
                                                  drug = drug, measurement_drug = measurement_drug, observation_drug = observation_drug, 
                                                  procedure_drug = procedure_drug, procedure = procedure, visit = visit, specimen = specimen, 
                                                  beta = Ei, dirichlet = wi, status = status)
     db.session.add(new_hipaa_request)
     db.session.commit()

     request_info = TrustCalcForm.query.filter_by(ownerid=current_user.id, status = 'pending').all()
     for i in request_info:
         print("the trust id is", i.trustid)
     apprInternal_info = TrustCalcForm.query.filter_by(ownerid=current_user.id, status = 'approved').all()
     deniedInternal_info = TrustCalcForm.query.filter_by(ownerid=current_user.id, status= 'denied').all()

     if(current_user.username == 'internaluser'):
         return render_template('dashboard.html', form=form, request_info=request_info, apprInternal_info=apprInternal_info, deniedInternal_info=deniedInternal_info)
     elif(current_user.username == 'externaluser'):
         return render_template('dashboard.html', form=form, request_info=request_info, apprInternal_info=apprInternal_info, deniedInternal_info=deniedInternal_info)

@app.route('/identifierform', methods=['GET','POST'])
def identifierform():
    print('in trust form')
    form = CreateIdentifierForm()
    if form.validate_on_submit():
        print('Form validated')
    
    else:
        print(form.errors)
    return render_template('identifier_form.html',form=form)

@app.route('/submitidentifierform', methods=['GET','POST'])
def submitidentifierform():
    formsubmit = IdentifierCalcForm()
    form = CreateIdentifierForm()
    person_id = form.person_id.data.decision
    irb_description = form.irb_description.data
    gender = form.gender.data.decision
    race = form.race.data.decision
    year_of_birth = form.year_of_birth.data.decision
    month_of_birth = form.month_of_birth.data.decision
    day_of_birth = form.day_of_birth.data.decision
    time_of_birth = form.time_of_birth.data.decision
    location = form.location.data.decision
    provider = form.provider.data.decision
    care_site = form.care_site.data.decision
    ethnicity = form.ethnicity.data.decision
    #irb_id = form.irb_id.data.irb_id
    '''
    condition = form.condition.data.decision
    condition_device = form.condition_device.data.decision
    condition_drug = form.condition_drug.data.decision
    condition_measurement = form.condition_measurement.data.decision
    condition_observation = form.condition_observation.data.decision
    condition_procedure = form.condition_procedure.data.decision
    device = form.device.data.decision
    device_drug = form.device_drug.data.decision
    device_observation = form.device_observation
    device_procedure = form.device_procedure.data.decision
    drug = form.drug.data.decision
    drug_measurement = form.drug_measurement.data.decision
    drug_observation = form.drug_observation.data.decision
    drug_procedure = form.drug_procedure.data.decision
    measurement = form.measurement.data.decision
    measurement_procedure = form.measurement_procedure.data.decision
    measurement_observation = form.measurement_observation.data.decision
    observation = form.observation.data.decision
    observation_procedure = form.observation_procedure.data.decision
    procedure = form.procedure.data.decision
    visit = form.visit.data.decision
    specimen = form.specimen.data.decision
'''
    new_irb_request = IdentifierCalcForm(ownerid =  current_user.id,person_id = person_id, irb_description = irb_description, gender = gender, race =race, year_of_birth = year_of_birth, month_of_birth = month_of_birth, day_of_birth = day_of_birth, time_of_birth = time_of_birth, location = location, provider = provider, care_site= care_site, ethnicity = ethnicity)

    db.session.add(new_irb_request)
    db.session.flush()
    t = datetime.time(datetime.now())
    print('current time is',t)
    now = datetime.now()
    date_time = now.strftime("%Y/%m/%d, %H:%M:%S")
    date_time = date_time.replace(",","")
    date_time = date_time.replace("/","")
    date_time = date_time.replace(":", "")
    date_time = date_time.replace(" ","")
    print("date and time:",date_time)
    print('Identifier id is',new_irb_request.identifier_id)
    templist = [person_id, gender, race, year_of_birth, month_of_birth, day_of_birth, time_of_birth, location, provider, care_site, ethnicity]
    '''
    domainlist = [condition, condition_device, condition_drug, condition_measurement, condition_observation, condition_procedure, device, device_drug, device_observation, device_procedure, drug, drug_measurement, drug_observation, drug_procedure, measurement, measurement_procedure, measurement_observation, observation, observation_procedure, procedure, visit, specimen]
'''
    if (person_id == 'Yes'):
        risk = "high"
    elif (person_id == 'No') and (gender == 'Yes') and (race == 'Yes'):
        risk = "high"
    elif (person_id == 'No') and (gender == 'No') and (race == 'No') and (year_of_birth == 'Yes') and (month_of_birth == 'Yes') and (day_of_birth == 'Yes'):
        risk = "high"
    elif (person_id == 'No') and (gender == 'No') and (race == 'No') and (year_of_birth == 'No'):
        risk = "medium"
    elif (person_id == 'No') and (gender == 'No') and (race == 'No') and (year_of_birth == 'Yes') and  (month_of_birth == 'No'):
        risk = "medium"
    elif (person_id == 'No') and (gender == 'No') and (race == 'No') and (year_of_birth == 'Yes') and  (month_of_birth == 'Yes') and (day_of_birth == 'No'):
        risk = "medium"
    else:
        risk = "low"
    
    print('the risk is',risk)
    templist = [1 if i== "Yes" else 0 for i in templist]
    print('The new templist is', templist)
    #domainlist = [1 if i== "Yes" else 0 for i in domainlist]  
    #print('The new domainlist is', domainlist) 
    postgres_insert_query = "INSERT INTO ui_irb_identifier(irb_id, irb_description, user_id, risk, id01, id02, id03, id04, id05, id06, id07, id08, id09, id10,id11) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    record_to_insert = (date_time, irb_description,current_user.id, risk, templist[0], templist[1], templist[2], templist[3], templist[4], templist[5], templist[6], templist[7], templist[8], templist[9], templist[10] )
    cur.execute(postgres_insert_query, record_to_insert)
    '''
    postgres_insert_query = "INSERT INTO ui_irb_domain(irb_id, dm01, dm02, dm03, dm04, dm05, dm06, dm07, dm08, dm09, dm10, dm11, dm12, dm13, dm14, dm15, dm16, dm17, dm18, dm19, dm20, dm21, dm22) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    record_to_insert = (date_time, domainlist[0], domainlist[1] , domainlist[2], domainlist[3], domainlist[4], domainlist[5], domainlist[6], domainlist[7], domainlist[8], domainlist[9], domainlist[10], domainlist[11], domainlist[12], domainlist[13], domainlist[14], domainlist[15] , domainlist[16], domainlist[17], domainlist[18], domainlist[19], domainlist[20], domainlist[21])
    cur.execute(postgres_insert_query, record_to_insert)
    '''
    conn.commit()
    postgreSQL_select_Query = "select * from ui_irb_identifier"
    cur.execute(postgreSQL_select_Query)
    resultset = cur.fetchall()
    for i in resultset:
        print('result fron identifier table is', i[0],i[1])
    print('resultset is',resultset)
    
    #print(formsubmit.identifier_id)
    if(current_user.username == 'Internal affiliated professor'):
        risk_user = "low"
    elif (current_user.username == 'Internal affiliated research assistant'):
        risk_user = "medium"
    elif (current_user.username == 'Internal affiliated student'):
        risk_user = "medium"
    elif (current_user.username == 'Internal non affiliated professor'):
        risk_user = "low"
    elif (current_user.username == 'Internal non affiliated research assistant'):
        risk_user = "medium"
    elif (current_user.username == 'Internal non affiliated student'):
        risk_user = "medium"
    elif (current_user.username == 'external'):
        risk_user = "high"


    return render_template('dashboard.html', resultset = resultset, name = current_user.username)

@app.route('/submitrequest', methods=['GET','POST'])
def submitrequest():
     print(current_user.username)
     form = CreateRequestForm()
     print("user id is", current_user.id)
     #if form.validate_on_submit()

     datasetprint=form.datasetname.data.nameset
     postgreSQL_select_Query = "select * from data_catalog  where data_catalog.dataset_name = %s"
     cur.execute(postgreSQL_select_Query, [datasetprint])
     resultset = cur.fetchone()
     print('The rows of selected dataset are',resultset)
     print('datasetrisk',resultset[2])
     #print('User selected',datasetprint)

     input_risk = list([1,3,3]);
     if(current_user.username == 'internal'):
         input_risk[0] = 1
     elif(current_user.username== 'external'):
         input_risk[0] = 90
     

    #determining input_risk for data_type
     if(form.typeofdata.data == 'identified'):
         input_risk[1] = 95;
     elif(form.typeofdata.data == 'deidentified'):
         input_risk[1] = 30;

     elif(form.typeofdata.data== 'limited'):
         input_risk[1] = 45;
     elif(form.typeofdata.data == 'aggregated'):
         input_risk[1] = 3;
     dataset_risk = resultset[2];
     accept_risk = resultset[3];
     input_risk[2] = dataset_risk;
     total_risk = 0;
     data_risk = accept_risk;
     for i in input_risk:

         total_risk += log(i);


     risk_factor = exp(log(total_risk));
     risk_level = "low";

     if(risk_factor >= (1.25 * data_risk)):

         risk_level = "high";
     elif((risk_factor >= (0.75 * data_risk)) and (risk_factor <= (1.25 * data_risk))):

         risk_level = "medium";
     else:

         risk_level = "low";
    

     new_request = RequestForm(ownerid =  current_user.id, requestname=form.requestname.data,datasetid = form.datasetname.data.datasetid, requestDescription=form.requestDescription.data, use=form.use.data, store=form.store.data, longdata = form.longdata.data, soondata = form.soondata.data, typeofdata = form.typeofdata.data, status = 'pending', risk_level = risk_level)
     db.session.add(new_request)
     
     db.session.commit()

     #request_info = RequestForm.query.filter_by( ownerid = current_user.id).all()
     #for request in request_info:
      #   requestObject = { 'status'  : request.status,
       #                    'requestname' : request.requestname
        #         }
        
         #print("Here at 3",request.status)
     #print(requests.user.email)
     request_info = RequestForm.query.filter_by(ownerid=current_user.id, status = 'pending').all()
     apprInternal_info = RequestForm.query.filter_by(ownerid=current_user.id, status = 'approved').all()
     deniedInternal_info = RequestForm.query.filter_by(ownerid=current_user.id, status= 'denied').all() 
     datasetid = resultset[0]

     if(current_user.username == 'internaluser'):
         return render_template('dashboard.html', form=form, request_info=request_info, apprInternal_info=apprInternal_info, deniedInternal_info=deniedInternal_info, datasetid = datasetid)
     elif(current_user.username == 'externaluser'):
         return render_template('dashboard.html', form=form, request_info=request_info, apprInternal_info=apprInternal_info, deniedInternal_info=deniedInternal_info, datasetid = datasetid)


@app.route('/viewmyreq/<req_id>', methods = ['GET',' POST'])
@login_required
def viewmyreq(req_id):
    
    #searchword = request.args.get('req_id', '')
    print("req id for internal user is",req_id)
    #print(request.url)
    #print(request.__dict__.items())
    #number = request.args.get('req_id')
    #print("Here at 4",number)
    

    return render_template('viewRequests.html')
@app.route('/viewpendingreq/<req_id>', methods = ['GET',' POST'])
@login_required
def viewpendingreq(req_id):
    
    #reqinfo = TrustCalcForm.query.filter_by(requestid=req_id, status = 'pending').all()
    #for i in reqinfo:
        #print('The dataset id is',i.datasetid)
    #postgreSQL_select_Query = "select * from data_catalog  where data_catalog.dataset_name = %s"
    #cur.execute(postgreSQL_select_Query, [datasetprint])
    #resultset = cur.fetchone()
    pendingreq_info = TrustCalcForm.query.filter_by(trustid=req_id).all()
    #for i in pendingreq_info:
    #    datasetinfo = Dataset.query.filter_by(datasetid = i.datasetid).all()
    #for j in datasetinfo:
    #    dataset_name = j.nameset
    #pg_query = 'select * from data_catalog where dataset_name = %s'
    #cur.execute(pg_query,[dataset_name])
    #record = cur.fetchone()
    #print("Result",record)

    
    
    approvedreq_info = RequestForm.query.filter_by(status= 'approved').all()
    denyreq_info = RequestForm.query.filter_by(status= 'denied').all()
    return render_template('viewpendingRequests.html', pendingreq_info = pendingreq_info, approvedreq_info=approvedreq_info, denyreq_info=denyreq_info)
    #return render_template('viewpendingRequests.html', pendingreq_info = pendingreq_info, approvedreq_info=approvedreq_info, denyreq_info=denyreq_info, record =record)
# have to modify
@app.route('/viewappInternal/<req_id>', methods = ['GET',' POST'])
@login_required
def viewappInternal(req_id):
    
    approvedreq_info = RequestForm.query.filter_by(status = 'approved').all()
    #denyreq_info = RequestForm.query.filter_by(status= 'denied').all()
    #pending_req = RequestForm.query.filter_by(status= 'pending').all()
    for j in approvedreq_info:
        print("Approved request is",j.requestname)

    for i in approvedreq_info:
        datasetinfo = Dataset.query.filter_by(datasetid = i.datasetid).all()
    for j in datasetinfo:
        dataset_name = j.nameset
    pg_query = 'select * from data_catalog where dataset_name = %s'
    cur.execute(pg_query,[dataset_name])
    record = cur.fetchone()
    print("Result",record)
    cur.execute(record[4])
    data = cur.fetchall() 
    rowcount = cur.rowcount
    print('row count', cur.rowcount)
    #for v in data:
        #for column, value in v.items():
            #print('{0}: {1}'.format(column, value))

    return render_template('viewdatauser.html',rowcount=rowcount, approvedreq_info = approvedreq_info, data = data)
# Have to modify
@app.route('/viewdenied/<req_id>', methods = ['GET',' POST'])
@login_required
def viewdenied(req_id):

    pendingreq_info = RequestForm.query.filter_by(requestid=req_id).all()
    for i in pendingreq_info:
        print(i.requestname)


    return render_template('viewRequests.html', pendingreq_info = pendingreq_info)


@app.route('/approvereq/<req_id>', methods = ['GET',' POST'])
@login_required
def approvereq(req_id):
    

    pendingreq_info = TrustCalcForm.query.filter_by(trustid=req_id).all()
    for i in pendingreq_info:
        i.status = 'approved'
        db.session.commit()
    approvedreq_info = TrustCalcForm.query.filter_by(status = 'approved').all()
    denyreq_info = TrustCalcForm.query.filter_by(status= 'denied').all()
    pending_req = TrustCalcForm.query.filter_by(status= 'pending').all()
    #for j in approvedreq_info:
        #print("Approved request is",j.requestname)
    
    #for i in pendingreq_info:
    #    datasetinfo = Dataset.query.filter_by(datasetid = i.datasetid).all()
    #for j in datasetinfo:
    #    dataset_name = j.nameset
    #pg_query = 'select * from data_catalog where dataset_name = %s'
    #cur.execute(pg_query,[dataset_name])
    #record = cur.fetchone()
    #print("Result",record)

    return render_template('dashboard_admin.html', pending_req=pending_req, denyreq_info =denyreq_info, approvedreq_info = approvedreq_info)

@app.route('/approvedadmin/<req_id>', methods = ['GET',' POST'])
@login_required
def approvedadmin(req_id):

    approvedreq_info = RequestForm.query.filter_by(status = 'approved').all()
    for i in approvedreq_info:
        datasetinfo = Dataset.query.filter_by(datasetid = i.datasetid).all()
    for j in datasetinfo:
        dataset_name = j.nameset
    print('Datasetname selected is',dataset_name)
    pg_query = 'select * from data_catalog where dataset_name = %s'
    cur.execute(pg_query,[dataset_name])
    record = cur.fetchone()
    print("Result",record)
    cur.execute(record[4])
    data = cur.fetchall()
    rowcount = cur.rowcount
    return render_template('viewdataadmin.html',rowcount=rowcount, data = data, approvedreq_info = approvedreq_info)

@app.route('/denyreq/<req_id>', methods = ['GET',' POST'])
@login_required
def denyreq(req_id):

    pendingreq_info = TrustCalcForm.query.filter_by(trustid=req_id).all()
    pending_req = TrustCalcForm.query.filter_by(status= 'pending').all()
    approvedreq_info = TrustCalcForm.query.filter_by(status= 'approved').all()
    for i in pendingreq_info:
        i.status = 'denied'
        db.session.commit()
    denyreq_info = TrustCalcForm.query.filter_by(status = 'denied').all()


    return render_template('dashboard_admin.html', pending_req= pending_req, approvedreq_info=approvedreq_info, denyreq_info = denyreq_info)

@app.route('/request',methods=['GET','POST'])
def request():
    form = CreateRequestForm()
    return render_template('request.html', form=form)
   # return render_template('bot/index_bot.html', form=form)

@app.route('/enter_request',methods=['GET','POST'])
def enter_request():
    form = CreateRequestForm()
    return render_template('request.html', form=form)


if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)
