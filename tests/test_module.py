from flask import app
from flask.app import Flask
import pytest
from ..apps import App

def test_routes():
    app_object = App()
    app = app_object.app
    return app
    
    