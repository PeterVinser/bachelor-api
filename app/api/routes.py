from flask import Blueprint, request
from app.services.query import handle_query

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/query', methods=['POST'])
def query():
    return handle_query(request)