from flask import Blueprint, request, jsonify
from app.services.suggestions_service import SuggestionsService
from app.core.security import Security



suggestions_bp = Blueprint('suggestions_api', __name__, url_prefix='/suggestions')

@suggestions_bp.route('/', methods=['GET'])
@Security.auth_guard()
def getSuggestions():
    try :
        filter = request.args.get('filter')
        sort = request.args.get('sort')

        if filter not in ["age", "fame", "location", "tags"] :
            filter = "default"

        if sort not in ["age", "fame", "location", "tags"] :
            sort = "default"

        return jsonify({"data": SuggestionsService.get_suggestions(request.user_id, filter, sort)})
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

        sort_by = request.args.get('sort_by')
        page = request.args.get('page')

        if not any([age_min, age_max, fame_min, location, tags, sort_by, page]):
            return jsonify({"data": SuggestionsService.get_emptyResearch(request.user_id)})
        else :
            return jsonify({"data": SuggestionsService.get_Research(request.user_id, request.args, sort_by)})
    except Exception as e:
        return jsonify({"error": str(e)}), 404