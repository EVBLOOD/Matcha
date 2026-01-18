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

@suggestions_bp.route('/research', methods=['GET'])
@Security.auth_guard()
def getExplore():
    try :
        age_min = request.args.get('age_min')
        age_max = request.args.get('age_max')
        fame_min = request.args.get('fame_min')
        location = request.args.get('location')
        tags = request.args.getlist('tags')

        if not any([age_min, age_max, fame_min, location, tags]):
            return jsonify({"data": SuggestionsService.get_emptyResearch(request.user_id)})
        else :
            return jsonify({"data": SuggestionsService.get_emptyResearch(request.user_id)})
            return jsonify({"data": SuggestionsService.get_emptyResearch(request.user_id)})
    except Exception as e:
        return jsonify({"error": str(e)}), 404