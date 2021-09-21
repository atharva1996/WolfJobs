from flask import Flask,jsonify
from werkzeug.wrappers import request
from passlib.hash import pbkdf2_sha256
import uuid

class authModel:
    def signup(self):
        print(request.form)
        user = {
            "_id":uuid.uuid4().hex,
            "name":request.form.get('name'),
            "email":request.form.get('email'),
            "password":request.form.get('password')
        }
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        return jsonify(user),200
        
