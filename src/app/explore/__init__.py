from flask import Blueprint

explore = Blueprint('explore', __name__)

from app.explore import views
