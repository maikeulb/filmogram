from flask import Blueprint

github = Blueprint('github', __name__)

from app.account import views
