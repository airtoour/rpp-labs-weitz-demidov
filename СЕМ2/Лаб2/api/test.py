from flask import Blueprint

test = Blueprint('test', __name__)


@test.route('add')
def add():
    return "okay"
