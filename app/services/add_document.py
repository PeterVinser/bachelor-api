from flask import jsonify

def handle_add_document(request):
    document_name = request.json['documentName']
    
    return jsonify({"result": f"document {document_name} added"})