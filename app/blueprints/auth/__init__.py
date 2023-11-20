from flask import Blueprint, render_template

auth = Blueprint('auth', __name__, template_folder='auth_templates')

from . import routes

