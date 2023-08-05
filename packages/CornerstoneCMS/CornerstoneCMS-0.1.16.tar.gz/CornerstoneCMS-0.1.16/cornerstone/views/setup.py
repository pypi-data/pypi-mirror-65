from flask import Blueprint, current_app, redirect

from cornerstone.db.setup import setup_app

setup = Blueprint('setup', __name__)


@setup.route('/', methods=['GET'])
def index():
    setup_app(current_app)
    redirect('/')
