from flask import Blueprint, request
from app.services.query import handle_query
from app.services.add_document import handle_add_document
from app.services.delete_document import handle_delete_document

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/query', methods=['POST'])
def query():
    return handle_query(request)

@api_blueprint.route('/add', methods=['POST'])
def add():
    return handle_add_document(request)

@api_blueprint.route('/delete', methods=['POST'])
def delete():
    return handle_delete_document(request)