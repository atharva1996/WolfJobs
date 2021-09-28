from datetime import datetime, timedelta
from types import MethodDescriptorType
from bson.objectid import ObjectId

from flask_wtf import form
from utilities import Utilities
from flask import app, render_template, session, url_for, flash, redirect, request,Response
from flask import json
from flask.helpers import make_response
from flask.json import jsonify
from flask_mail import Mail, Message
import jwt
from forms import ForgotPasswordForm, RegistrationForm, LoginForm, ResetPasswordForm, PostingForm, ApplyForm
import bcrypt
from apps import App
from flask_login import LoginManager,login_required
from bson.objectid import ObjectId

app_object = App()
app = app_object.app
mongo = app_object.mongo
mail = app_object.mail

@app.route("/")
@app.route("/home")
def home():
    if session.get('email'):
        return render_template('home.html')
    else:
        return redirect(url_for('login'))


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if not session.get('email'):
        form = RegistrationForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                username = request.form.get('username')
                email = request.form.get('email')
                password = request.form.get('password')
                id = mongo.db.ath.insert({'name':username,'email':email,'pwd':bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()),'temp':None})
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if not session.get('email'):
        form = LoginForm()
        if form.validate_on_submit():
            temp = mongo.db.ath.find_one({'email':form.email.data},{'email','pwd','temp'})
            if temp!= None and temp['email'] == form.email.data and (bcrypt.checkpw(form.password.data.encode("utf-8"),temp['pwd']) or temp['temp']==form.password.data):
                flash('You have been logged in!', 'success')
                session['email'] = temp['email']
                session['login_type'] = form.type.data
                return redirect(url_for('dashboard'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
    else:
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form,type=form.type.data)

@app.route("/logout",methods=['GET','POST'])
def logout():
    session.clear()
    return "success"


@app.route("/forgotpassword",methods=['POST','GET'])
def forgotPassword():
    if not session.get('email'):
        form = ForgotPasswordForm()
        if form.validate_on_submit():
            temp = mongo.db.ath.find_one({'email':form.email.data},{'email','pwd','temp'})
            if temp == None:
                flash('Incorrect Email Id','danger')
                f = ForgotPasswordForm()
                return render_template('forgotpassword.html',form=f)
            if temp['email']==form.email.data:
                util = Utilities()
                if not util.send_email(form.email.data)=="success":
                    flash('Email has been sent successfully!','success')
                    return redirect(url_for("login"))
                return "Failed"
            else:
                flash('Incorrect email id','danger')

        return render_template("forgotpassword.html",form=form)     
            
    else:
        return redirect(url_for('home'))


@app.route("/posting", methods=['GET','POST'])
def posting():
    if session.get('email')!=None and session.get('email') and session.get('login_type')=='Manager':
        form = PostingForm()
        if form.validate_on_submit():
            now = datetime.now()

            now = now.strftime('%Y-%m-%d %H:%M')

            #name = form.name.data
            email = session['email']
            designation = form.designation.data
            job_title = form.job_title.data
            job_location = form.job_location.data
            job_description = form.job_description.data
            skills = form.skills.data
            schedule = form.schedule.data
            salary = form.salary.data
            rewards = form.rewards.data

            id = mongo.db.jobs.insert({'email':email,'designation':designation,'job_title':job_title,'job_description':job_description,'time_posted':now,'job_location':job_location,'skills':skills,'schedule':schedule,'salary':salary,'rewards':rewards,'Appliers':[]})
            flash("Job Created!",'success')
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))
    return render_template('job_post.html',form = form)


@app.route("/applying", methods=['GET','POST'])
def applying():
    if session.get('email')!=None and session.get('email') and session.get('login_type')=='Applicant':
        form = ApplyForm()
        if form.validate_on_submit():
            now = datetime.now()

            now = now.strftime('%Y-%m-%d %H:%M')

            name = form.apply_name.data
            email = session['email']
            phone = form.apply_phone.data
            apply_address = form.apply_address.data
            dob = form.dob.data
            skills = form.skills.data
            availability = form.availability.data
            schedule = form.schedule.data
            
            id = mongo.db.applier.insert({'name':name,'email':email,'phone':phone,'apply_address':apply_address,'dob':dob,'time_posted':now,'availability':availability,'schedule':schedule,'skills':skills})
            flash("Job Applied!",'success')
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))
    return render_template('job_post.html',form = form)



@app.route("/dashboard", methods=['GET','POST'])
def dashboard():
    login_type = session["login_type"]
    email = session['email']

    if login_type == 'Manager':
        if mongo.db.jobs.find_one({'email':email}) == None:
            return render_template('dashboard.html', jobs = None)
        else:
            cursor = mongo.db.jobs.find({'email':email})
            get_jobs = []
            for record in cursor:
                get_jobs.append(record)

            get_jobs = sorted(get_jobs, key = lambda i: i['time_posted'],reverse=True)
            if(len(get_jobs)>5):
                return render_template('dashboard.html',jobs = get_jobs[:5])
            else:
                return render_template('dashboard.html',jobs = get_jobs)
    else:
        cursor = mongo.db.jobs.find()
        get_jobs = []
        for record in cursor:
            get_jobs.append(record)

        get_jobs = sorted(get_jobs, key = lambda i: i['time_posted'],reverse=True)
        return render_template('dashboard.html',jobs = get_jobs)


'''
@app.route("/jobDetails", methods=['GET','POST'])
def jobDetails():
    form = ApplyForm()
    email = session['email']
    login_type = session["login_type"]
    job_id = request.args.get("job_id")
    if login_type=="Applicant":
        job = mongo.db.jobs.find_one({'_id':ObjectId(job_id)})
        applicant = mongo.db.ath.find_one({'email':email})
        return render_template('job_details.html',job = job, form=form, applicant=applicant)
    else:
        return "Hi"

'''
@app.route("/jobDetails", methods=['GET','POST'])
def jobDetails():
    form = ApplyForm()
    email = session['email']
    login_type = session["login_type"]
    job_id = request.args.get("job_id")
    job = mongo.db.jobs.find_one({'_id':ObjectId(job_id)})
    applicant = mongo.db.ath.find_one({'email':email})
        
    if form.validate_on_submit():
            if request.method == 'POST':
                apply_name = request.form.get('apply_name')
                email = session['email']
                apply_phone = request.form.get('apply_phone')
                apply_address = request.form.get('apply_address')
                dob = request.form.get('dob')
                skills = request.form.get('skills')
                availability = request.form.get('availability')
                schedule = request.form.get('schedule')
                id = mongo.db.applier.insert({'job_id':job_id,'email':email,'name':apply_name,'phone':apply_phone,'address':apply_address,'dob':dob,'skills':skills,'availability':availability,'schedule':schedule})
                mongo.db.jobs.update({'_id':ObjectId(job_id)},{'$push':{'Appliers':session['email']}},upsert=True)
            flash('Successfully Applied to the job!', 'success')
            return redirect(url_for('dashboard'))
    if login_type=="Applicant":
        return render_template('job_details.html',job = job, form=form, applicant=applicant)
    else:
        return "Hi"


@app.route("/dummy", methods=['GET'])
def dummy():
    response = make_response(
                redirect(url_for('home'),200),
            )
    response.headers["Content-Type"] = "application/json",
    response.headers["token"] = "123456"
    return response


if __name__ == '__main__':
    app.run(debug=True)