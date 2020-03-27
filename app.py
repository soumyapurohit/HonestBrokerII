from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from flask_bootstrap import Bootstrap
from math import log, exp, floor
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, RadioField, SelectField
from wtforms.validators import InputRequired, Email, Length
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy.engine import Engine
from sqlalchemy import event
import os
import psycopg2

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
conn = psycopg2.connect("host=hbcdm.cdm9kks3s0wa.us-east-1.rds.amazonaws.com dbname=hbcdm user=hbadmin password=hbaccess")
cur = conn.cursor()
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
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

class TrustChoice(UserMixin, db.Model):
    trustchoiceid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    decision = db.Column(db.String(40))
    #trustchoices = db.relationship('TrustCalcForm', backref = 'trust_choice', lazy = 'dynamic')

class TrustCalcForm(UserMixin, db.Model):
    trustid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    staffread_policies = db.Column(db.String(40))
    doc_attest = db.Column(db.String(40))
    doc_review = db.Column(db.String(40))
    staff_training = db.Column(db.String(40))
    doc_training = db.Column(db.String(40))
    desig_staff = db.Column(db.String(40))
    assoc_receive = db.Column(db.String(40))
    business = db.Column(db.String(40))
    audit = db.Column(db.String(40))
    written_report = db.Column(db.String(40))
    sys_in = db.Column(db.String(40))
    demonstrate = db.Column(db.String(40))
    report = db.Column(db.String(40))
    anonymous = db.Column(db.String(40))
    match = db.Column(db.String(10))
    mismatch = db.Column(db.String(10))
    undecided = db.Column(db.String(10))
    beta = db.Column(db.String(10))
    dirichlet = db.Column(db.String(10))
    ownerid= db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
   # trustchoiceid = db.Column(db.Integer, db.ForeignKey('trust_choice.trustchoiceid'), nullable=False)



#class SelectFieldtypedata(db.Model):
#    datatype = db.Column(db.String(40))

#class ChoiceOpts(FlaskForm):
#    opts = QuerySelectField(query_factory = choice_dataset, allow_blank =True)
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
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length( max=45)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
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

class CreateTrustCalcForm(FlaskForm):
    #CaStatus = QuerySelectField('Enter your choice', choices=[('Yes', 'Yes'), ('No', 'No'), ('Uncertain', 'Uncertain')])
     staffread_policies = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     doc_attest = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     doc_review = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     staff_training = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     doc_training = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     desig_staff = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     assoc_receive = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     business = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     audit  = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     written_report = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     sys_in = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     demonstrate = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     report = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     anonymous = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')

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
    

    pending_req = RequestForm.query.filter_by(status= 'pending').all()
    approvedreq_info = RequestForm.query.filter_by(status= 'approved').all()
    denyreq_info = RequestForm.query.filter_by(status= 'denied').all()
    for i in pending_req:
        print("pending request id is",i.requestid)

    
    if(current_user.username == 'Admin'):
        return render_template('dashboard_admin.html', name = current_user.username, pending_req= pending_req, approvedreq_info= approvedreq_info, denyreq_info=denyreq_info, resultset=resultset)
    elif(current_user.username == 'internaluser'):
        print('internal user dashboard')
        apprInternal_info = RequestForm.query.filter_by(ownerid=current_user.id ,status = 'approved').all()
        request_info = RequestForm.query.filter_by(ownerid=current_user.id ,status = 'pending').all()
        deniedInternal_info = RequestForm.query.filter_by(ownerid=current_user.id ,status = 'denied').all()
        for i in apprInternal_info:
            print("Internal user approved request is ",i.requestname)
        return render_template('dashboard.html', name = current_user.username, apprInternal_info= apprInternal_info, request_info=request_info, deniedInternal_info = deniedInternal_info, resultset = resultset)
    else:
        print('external user dashboard')
        apprInternal_info = RequestForm.query.filter_by(ownerid=current_user.id ,status = 'approved').all()
        print('Id for external user is Hi',current_user.id)
        request_info = RequestForm.query.filter_by(ownerid=current_user.id ,status = 'pending').all()
        deniedInternal_info = RequestForm.query.filter_by(ownerid=current_user.id ,status = 'denied').all()
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

@app.route('/submithipaaform', methods=['GET','POST'])
def submithipaa():
     print(current_user.username)
     form = CreateTrustCalcForm()

     staffread_policiesprint = form.staffread_policies.data.decision
     doc_attestprint = form.doc_attest.data.decision
     doc_reviewprint = form.doc_review.data.decision
     staff_trainingprint = form.staff_training.data.decision
     doc_trainingprint = form.doc_training.data.decision
     desig_staffprint = form.desig_staff.data.decision
     assoc_reviewprint = form.assoc_receive.data.decision
     businessprint = form.business.data.decision
     auditprint = form.audit.data.decision
     written_reportprint = form.written_report.data.decision
     sys_inprint = form.sys_in.data.decision
     demonstrateprint = form.demonstrate.data.decision
     reportprint = form.report.data.decision
     anonymousprint = form.anonymous.data.decision
     
     
     templist = [staffread_policiesprint, doc_attestprint, doc_reviewprint, staff_trainingprint, doc_trainingprint, desig_staffprint, assoc_reviewprint, businessprint, auditprint, written_reportprint, sys_inprint, demonstrateprint, reportprint, anonymousprint]
     if (current_user.username == 'internaluser'):
         userrole = 'internal_user'
     elif (current_user.username == 'externaluser'):
         userrole = 'external_user'
     postgreSQL_select_Query = "select * from data_policy  where data_policy.user_role = %s"
     cur.execute(postgreSQL_select_Query, [userrole])
     resultset = cur.fetchone()
     d = (resultset[1:])
     print(d)         
     countmismatch = 0
     countundecided = 0
     countmatch = 0
     for a,b in zip(templist, d):
         if (a == 'Yes' and (b == 'R' or b  == None)):
             countmatch += 1
         elif (a == 'No' and b == 'R'):
             countmismatch += 1
         elif (a == 'No' and b == None):
             countmatch += 1
         elif (a == 'Uncertain' and b == 'R'):
             countundecided += 1
         elif (a == 'Uncertain' and b == None):
             countmatch += 1
     N = 14
     # beta model trust calculation
     alpha_c = floor(countmatch + ((countundecided*countmatch)/(countmatch+countmismatch)));
     beta_c = N - alpha_c;
     Ei = ((alpha_c + 1)/(alpha_c + beta_c + 2));
     print('Beta model is',Ei)
    
     '''
     # Formula 7 of trsut model
     a = 0.5
     Eb = (countmatch+1) / (countmatch+countmismatch+countundecided+3)
     Eu = (countundecided+1) / (countmatch+countmismatch+countundecided+3)
     Ew = Eb + a*Eu
     rEw = log(Ew/(1-Ew))
     if rEw > 0:
         wi = 1 - exp(-abs(rEw))
     elif rEw < 0:
         wi = -(1 - exp(-abs(rEw)))
     else:
         wi = 0
     print('dirichlet model is', wi)
     '''
     new_hipaa_request = TrustCalcForm(ownerid =  current_user.id,staffread_policies = staffread_policiesprint, doc_attest = doc_attestprint, doc_review = doc_reviewprint, staff_training = staff_trainingprint, doc_training = doc_trainingprint, desig_staff = desig_staffprint, assoc_receive = assoc_reviewprint, business = businessprint, audit = auditprint, written_report = written_reportprint, sys_in = sys_inprint, demonstrate = demonstrateprint, report = reportprint, anonymous = anonymousprint, match = countmatch, mismatch = countmismatch, undecided = countundecided, beta = Ei, dirichlet = 0.5)
     db.session.add(new_hipaa_request)
     db.session.commit()

     request_info = RequestForm.query.filter_by(ownerid=current_user.id, status = 'pending').all()
     apprInternal_info = RequestForm.query.filter_by(ownerid=current_user.id, status = 'approved').all()
     deniedInternal_info = RequestForm.query.filter_by(ownerid=current_user.id, status= 'denied').all()

     return render_template('dashboard.html',name = current_user.username, form=form, request_info=request_info, apprInternal_info=apprInternal_info, deniedInternal_info=deniedInternal_info)

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
    
    reqinfo = RequestForm.query.filter_by(requestid=req_id, status = 'pending').all()
    for i in reqinfo:
        print('The dataset id is',i.datasetid)
    #postgreSQL_select_Query = "select * from data_catalog  where data_catalog.dataset_name = %s"
    #cur.execute(postgreSQL_select_Query, [datasetprint])
    #resultset = cur.fetchone()
    pendingreq_info = RequestForm.query.filter_by(requestid=req_id).all()
    for i in pendingreq_info:
        datasetinfo = Dataset.query.filter_by(datasetid = i.datasetid).all()
    for j in datasetinfo:
        dataset_name = j.nameset
    pg_query = 'select * from data_catalog where dataset_name = %s'
    cur.execute(pg_query,[dataset_name])
    record = cur.fetchone()
    print("Result",record)

    
    
    approvedreq_info = RequestForm.query.filter_by(status= 'approved').all()
    denyreq_info = RequestForm.query.filter_by(status= 'denied').all()

    return render_template('viewpendingRequests.html', pendingreq_info = pendingreq_info, approvedreq_info=approvedreq_info, denyreq_info=denyreq_info, record =record)
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
    

    pendingreq_info = RequestForm.query.filter_by(requestid=req_id).all()
    for i in pendingreq_info:
        i.status = 'approved'
        db.session.commit()
    approvedreq_info = RequestForm.query.filter_by(status = 'approved').all()
    denyreq_info = RequestForm.query.filter_by(status= 'denied').all()
    pending_req = RequestForm.query.filter_by(status= 'pending').all()
    for j in approvedreq_info:
        print("Approved request is",j.requestname)
    
    for i in pendingreq_info:
        datasetinfo = Dataset.query.filter_by(datasetid = i.datasetid).all()
    for j in datasetinfo:
        dataset_name = j.nameset
    pg_query = 'select * from data_catalog where dataset_name = %s'
    cur.execute(pg_query,[dataset_name])
    record = cur.fetchone()
    print("Result",record)

    return render_template('dashboard_admin.html', pending_req=pending_req, record = record, denyreq_info =denyreq_info, approvedreq_info = approvedreq_info)

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

    pendingreq_info = RequestForm.query.filter_by(requestid=req_id).all()
    pending_req = RequestForm.query.filter_by(status= 'pending').all()
    approvedreq_info = RequestForm.query.filter_by(status= 'approved').all()
    for i in pendingreq_info:
        i.status = 'denied'
        db.session.commit()
    denyreq_info = RequestForm.query.filter_by(status = 'denied').all()


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
