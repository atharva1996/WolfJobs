from datetime import datetime, timedelta
from types import MethodDescriptorType
from bson.objectid import ObjectId

from flask_wtf import form
from utilities import Utilities
from flask import app, render_template, session, url_for, flash, redirect, request, Response
from flask import json
from flask.helpers import make_response
from flask.json import jsonify
from flask_mail import Mail, Message
import jwt
from forms import ForgotPasswordForm, RegistrationForm, LoginForm, ResetPasswordForm, PostingForm, ApplyForm
import bcrypt
from apps import App
from flask_login import LoginManager, login_required
from bson.objectid import ObjectId

app_object = App()
app = app_object.app
mongo = app_object.mongo
mail = app_object.mail


@app.route("/")
@app.route("/home")
def home():
############################ 
# home() function displays the homepage of our website.
# route "/home" will redirect to home() function. 
# input: The function takes session as the input 
# Output: Out function will redirect to the login page
# ########################## 
    if session.get('email'):
        return render_template('home.html')
    else:
        return redirect(url_for('login'))


@app.route("/about")
def about():
# ############################ 
# about() function displays About Us page (about.html) template
# route "/about" will redirect to home() function. 
# ########################## 
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
# ############################ 
# register() function displays the Registration portal (register.html) template
# route "/register" will redirect to register() function.
# RegistrationForm() called and if the form is submitted then various values are fetched and updated into database
# Input: Username, Email, Password, Confirm Password
# Output: Value update in database and redirected to home login page
# ########################## 
    if not session.get('email'):
        form = RegistrationForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                username = request.form.get('username')
                email = request.form.get('email')
                password = request.form.get('password')
                id = mongo.db.ath.insert({'name': username, 'email': email, 'pwd': bcrypt.hashpw(
                    password.encode("utf-8"), bcrypt.gensalt()), 'temp': None})
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
# ############################ 
# login() function displays the Login form (login.html) template
# route "/login" will redirect to login() function.
# LoginForm() called and if the form is submitted then various values are fetched and verified from the database entries
# Input: Email, Password, Login Type 
# Output: Account Authentication and redirecting to Dashboard
# ########################## 
    if not session.get('email'):
        form = LoginForm()
        if form.validate_on_submit():
            temp = mongo.db.ath.find_one({'email': form.email.data}, {
                                         'email', 'pwd', 'temp'})
            if temp is not None and temp['email'] == form.email.data and (
                bcrypt.checkpw(
                    form.password.data.encode("utf-8"),
                    temp['pwd']) or temp['temp'] == form.password.data):
                flash('You have been logged in!', 'success')
                session['email'] = temp['email']
                session['login_type'] = form.type.data
                return redirect(url_for('dashboard'))
            else:
                flash(
                    'Login Unsuccessful. Please check username and password',
                    'danger')
    else:
        return redirect(url_for('home'))
    return render_template(
        'login.html',
        title='Login',
        form=form,
        type=form.type.data)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
# ############################ 
# logout() function just clears out the session and returns success
# route "/logout" will redirect to logout() function.
# Output: session clear 
# ########################## 
    session.clear()
    return "success"


@app.route("/forgotpassword", methods=['POST', 'GET'])
def forgotPassword():
# ############################ 
# forgotpassword() function displays the Forgot Password form (forgotpassword.html) template
# route "/forgotpassword" will redirect to forgotpassword() function.
# ForgotPasswordForm() called and if the form is submitted then email is fetched and verified from the database entries
# if authenticated then a mail with new pasword is sent
# Input: Email
# Output: Account Authentication, Email sent to user and redirecting to Login Page
# ########################## 
    if not session.get('email'):
        form = ForgotPasswordForm()
        if form.validate_on_submit():
            temp = mongo.db.ath.find_one({'email': form.email.data}, {
                                         'email', 'pwd', 'temp'})
            if temp is None:
                flash('Incorrect Email Id', 'danger')
                f = ForgotPasswordForm()
                return render_template('forgotpassword.html', form=f)
            if temp['email'] == form.email.data:
                util = Utilities()
                if not util.send_email(form.email.data) == "success":
                    flash('Email has been sent successfully!', 'success')
                    return redirect(url_for("login"))
                return "Failed"
            else:
                flash('Incorrect email id', 'danger')

        return render_template("forgotpassword.html", form=form)

    else:
        return redirect(url_for('home'))


@app.route("/posting", methods=['GET', 'POST'])
def posting():
# ############################ 
# posting() function displays Job Posting form (job_post.html) template
# route "/posting" will redirect to posting() function.
# PostingForm() called and if the form is submitted then various input values are updated into database
# Input: Job Designation, Job Title, Job Location, Job Description, Skills required, Schedule of the job, Salary, Rewards
# Output: values updated in database and page redirected to dashboard 
# ########################## 
    if session.get('email') is not None and session.get(
            'email') and session.get('login_type') == 'Manager':
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

            id = mongo.db.jobs.insert({'email': email,
                                       'designation': designation,
                                       'job_title': job_title,
                                       'job_description': job_description,
                                       'time_posted': now,
                                       'job_location': job_location,
                                       'skills': skills,
                                       'schedule': schedule,
                                       'salary': salary,
                                       'rewards': rewards,
                                       'Appliers': [],
                                       'selected': None})
            flash("Job Created!", 'success')
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))
    return render_template('job_post.html', form=form)


@app.route("/applying", methods=['GET', 'POST'])
def applying():
# ############################ 
# applying() function displays Job application form (apply.html) template
# route "/applying" will redirect to applying() function.
# ApplyForm() called and if the form is submitted then various input values are updated into database
# Input: Name, Phone No., Address, date of birth, skills, Availability, schedule, Signature 
# Output: Values updated in database and page redirected to dashboard 
# ########################## 
    if session.get('email') is not None and session.get(
            'email') and session.get('login_type') == 'Applicant':
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

            id = mongo.db.applier.insert({'name': name,
                                          'email': email,
                                          'phone': phone,
                                          'apply_address': apply_address,
                                          'dob': dob,
                                          'time_posted': now,
                                          'availability': availability,
                                          'schedule': schedule,
                                          'skills': skills})
            flash("Job Applied!", 'success')
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))
    return render_template('job_post.html', form=form)


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
# ############################ 
# dashboard() function displays the main page of our website (dashboard.html) template. It shows jobs posted and available and applied jobs.
# route "/dashboard" will redirect to dashboard() function.
# Various details of postings and jobs are fetched from database and displayed
# Input: Login type, Email
# Output: various details of postings and jobs
# ########################## 
    login_type = session["login_type"]
    email = session['email']

    if login_type == 'Manager':
        if mongo.db.jobs.find_one({'email': email}) is None:
            return render_template('dashboard.html', jobs=None)
        else:
            cursor = mongo.db.jobs.find({'email': email})
            get_jobs = []
            for record in cursor:
                get_jobs.append(record)

            get_jobs = sorted(
                get_jobs,
                key=lambda i: i['time_posted'],
                reverse=True)
            if(len(get_jobs) > 5):
                return render_template('dashboard.html', jobs=get_jobs[:5])
            else:
                return render_template('dashboard.html', jobs=get_jobs)
    else:
        cursor = mongo.db.jobs.find({'email': {'$ne': email}})
        get_jobs = []
        for record in cursor:
            get_jobs.append(record)

        get_jobs = sorted(
            get_jobs,
            key=lambda i: i['time_posted'],
            reverse=True)
        return render_template('dashboard.html', jobs=get_jobs)


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


@app.route("/jobDetails", methods=['GET', 'POST'])
def jobDetails():
# ############################ 
# jobDetails() function displays the main page of our website (job_details.html) template. It shows jobs posted and available and applied jobs.
# route "/jobDetails" will redirect to jobDetails() function.
# ApplyForm() called and if the form is submitted then various input values are updated into database
# Input: Login type, Email, job_id
# Output: If applicant - job_details.html is displayed and if manager then all applicants data is displayed along with job details
# ########################## 
    form = ApplyForm()
    email = session['email']
    login_type = session["login_type"]
    job_id = request.args.get("job_id")
    job = mongo.db.jobs.find_one({'_id': ObjectId(job_id)})
    applicant = mongo.db.ath.find_one({'email': email})

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
            id = mongo.db.applier.insert(
                {
                    'job_id': ObjectId(job_id),
                    'email': email,
                    'name': apply_name,
                    'phone': apply_phone,
                    'address': apply_address,
                    'dob': dob,
                    'skills': skills,
                    'availability': availability,
                    'schedule': schedule})
            mongo.db.jobs.update({'_id': ObjectId(job_id)}, {
                                 '$push': {'Appliers': session['email']}})
        flash('Successfully Applied to the job!', 'success')
        return redirect(url_for('dashboard'))
    if login_type == "Applicant":
        return render_template(
            'job_details.html',
            job=job,
            form=form,
            applicant=applicant)
    else:
        applicant = []
        print(job_id)
        applicants = mongo.db.applier.find({'job_id': ObjectId(job_id)})
        for record in applicants:
            applicant.append(record)
        print(applicant)
        return render_template(
            'job_details.html',
            job=job,
            applicant=applicant)


@app.route("/deleteJob", methods=['GET', 'POST'])
def deleteJob():
# ############################ 
# deleteJob() function just clears out a particular job with job_id from the databse and returns back to dashboard
# route "/deleteJob" will redirect to deleteJob() function.
# Input: job_id
# Output: particular job with job_id removed and page redirected to dashboard
# ########################## 
    job_id = request.args.get("job_id")
    id = mongo.db.jobs.remove({'_id': ObjectId(job_id)})
    return redirect(url_for('dashboard'))


@app.route("/selectApplicant", methods=['GET', 'POST'])
def selectApplicant():
# ############################ 
# selectApplicant() function performs the functionality of seleting an applicant for a particular job.
# route "/selectApplicant" will redirect to selectApplicant() function.
# Input value are taken and corresponding to those values set attribute is update to selected in database
# Input: job_id, applicant_id
# Output: Applicant is selected (database updated) and page redirected to dashboard
# ########################## 
    job_id = request.args.get("job_id")
    applicant_id = request.args.get("applicant_id")
    print(job_id, applicant_id)
    mongo.db.jobs.update({'_id': ObjectId(job_id)}, {
                         '$set': {"selected": applicant_id}})
    return redirect(url_for('dashboard'))


@app.route("/jobsApplied", methods=['GET', 'POST'])
def jobsApplied():
# ############################ 
# jobsApplied() function performs the functionality displaying number of jobs an applicant applied to
# route "/jobsApplied" will redirect to jobsApplied() function.
# Input: email and Appliers
# Output: Display of Number of jobs an applicant applied to.
# ########################## 
    email = session['email']
    cursor = mongo.db.jobs.find({'Appliers': {'$in': [email]}})

    get_all_jobs = []
    for record in cursor:
        get_all_jobs.append(record)
    if get_all_jobs == []:
        return render_template('jobs_applied.html', status=False)
    else:
        return render_template('jobs_applied.html',
                               jobs=get_all_jobs, status=True)


@app.route("/dummy", methods=['GET'])
def dummy():
# ############################ 
# dummy() function performs the functionality displaying the message "feature will be added soon"
# route "/dummy" will redirect to dummy() function.
# Output: redirects to dummy.html
# ########################## 
    """response = make_response(
                redirect(url_for('home'),200),
            )
    response.headers["Content-Type"] = "application/json",
    response.headers["token"] = "123456"
    return response"""
    return render_template('dummy.html')


if __name__ == '__main__':
    app.run(debug=True)
