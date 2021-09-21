from config import SECRET_KEY
import json
from flask import Flask, app, config,request,jsonify,make_response,render_template,session
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import Blueprint
from . import controllers
from models.authModel import authModel


def token_required(func):
    @wraps(func)
    def decorated(*args,**kwargs):
        token = request.args.get('token')
        print(token)
        if not token:
            return jsonify({'msg':'Alert!: Token is missing!'})
        try:
            payload = token.decode(token,app.config['SECRET_KEY'])
        except:
            return jsonify({'msg':'Alert! Invalid Token!'})
    return decorated

@controllers.route('/public')
def auth():
    return 'JWT verified! Welcome to WolfJobs!'


@controllers.route('/auth')
@token_required
def method_name():
    pass


@controllers.route('/', methods=['GET'])
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Logged in!'

@controllers.route('/user/register')
def register():
    
    return render_template('register.html')

        
@controllers.route('/login',methods=['POST'])
def login():
    if request.form['username'] and request.form['password']=='123456':
        session['logged_in'] = True
        token = jwt.encode({
            'user': request.form['username'],
            'expiration': str(datetime.utcnow()+timedelta(seconds=120))
        },
        '12345',
        algorithm="HS256"
        )
        return jsonify({'token':token})
        # the below line will give decoded token
        return jsonify({'token': jwt.decode(token,app.config['SECRET_KEY'],algorithms=["HS256"])})
    else:
        return make_response('Unable to verify',403,{'WWW-Authenticate':'Basic realm: Authentication Failed!'})




