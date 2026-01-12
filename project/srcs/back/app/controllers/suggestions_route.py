from flask import Blueprint, request, jsonify
from app.services.suggestions_service import SuggestionsService
from app.core.security import Security



suggestions_bp = Blueprint('suggestions_api', __name__, url_prefix='/suggestions')

@suggestions_bp.route('/', methods=['GET'])
@Security.auth_guard()
def getSuggestions():
    try :
        return jsonify({"data": SuggestionsService.get_suggestions(request.user_id)})
    except Exception as e:
        return jsonify({"error": str(e)}), 404