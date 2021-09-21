import json
from flask import Flask,request,jsonify,make_response,render_template,session
import jwt
from datetime import datetime, timedelta
from functools import wraps
from controllers import *
from flask_mongoengine import MongoEngine


app = Flask(__name__)
app.config['SECRET_KEY']='1234234234324'
app.config['MONGODB_SETTINGS'] = {
    'db': 'WolfJobs',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)
app.register_blueprint(controllers)

if __name__=="__main__":
    app.run(debug=True)