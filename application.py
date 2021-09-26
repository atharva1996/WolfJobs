from datetime import datetime, timedelta
from types import MethodDescriptorType
from utilities import Utilities
from flask import app, render_template, session, url_for, flash, redirect, request,Response
from flask import json
from flask.helpers import make_response
from flask.json import jsonify
from flask_mail import Mail, Message
import jwt
from forms import ForgotPasswordForm, RegistrationForm, LoginForm, ResetPasswordForm
import bcrypt
from apps import App
from flask_login import LoginManager,login_required

app_object = App()
app = app_object.app
mongo = app_object.mongo
mail = app_object.mail

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    if session.get('email'):
        return render_template('home.html', posts=posts)
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
            if temp['email'] == form.email.data and (bcrypt.checkpw(form.password.data.encode("utf-8"),temp['pwd']) or temp['temp']==form.password.data):
                flash('You have been logged in!', 'success')
                session['email'] = temp['email']
                print(form.type.data)
                session['login_type'] = form.type.data
                return redirect(url_for('home'))
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
            print(temp)
            if temp == None:
                flash('Incorrect Email Id')
                f = ForgotPasswordForm()
                return render_template('forgotpassword.html',form=f)
            if temp['email']==form.email.data:
                util = Utilities()
                if not util.send_email(form.email.data)=="success":
                    flash(f'Email has been sent successfully!')
                    return redirect(url_for("login"))
                return "Failed"
            else:
                flash('Incorrect email id')

        return render_template("forgotpassword.html",form=form)     
            
    else:
        return redirect(url_for('home'))


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