from . import controllers

@controllers.route("/dummy")
def dummy():
    return "hello world"