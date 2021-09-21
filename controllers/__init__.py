from flask import Blueprint
controllers = Blueprint('controllers', __name__)

from .authController import *
from .dummy import *
