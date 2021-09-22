from flask import Flask
from flask_pymongo import PyMongo
import pickle

class App:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'secret'
        self.app.config['MONGO_URI'] = 'mongodb://localhost:27017/test'
        self.mongo = PyMongo(self.app)