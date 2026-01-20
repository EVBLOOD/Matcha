from flask import Blueprint, request, jsonify
# from app.services.suggestions_service import SuggestionsService
from app.services.report_service import ReportService
from app.services.user_interactions_service import UserInteractionsService
from app.services.user_blocks_service import UserBlocksService
from app.services.profile_views_service import ProfileViewsService
from app.core.security import Security



inteructions_bp = Blueprint('inteructions_api', __name__, url_prefix='/inteructions')

@inteructions_bp.route('/blocks', methods=['GET'])
@Security.auth_guard()
def getBlockList():
    try :
        return jsonify({"data": UserBlocksService.get_all_ot_blocks_given(user_id=request.user_id)})
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@inteructions_bp.route('/likes', methods=['GET'])
@Security.auth_guard()
def getMyLikes():
    try :
        return jsonify({"data": UserInteractionsService.get_all_ot_likes_given(user_id=request.user_id)})
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@inteructions_bp.route('/views', methods=['GET'])
@Security.auth_guard()
def getMyViews():
    try :
        # get_all_likes_got
        return jsonify({"data": ProfileViewsService.get_all_likes_got(request.user_id)})
    except Exception as e:
        return jsonify({"error": str(e)}), 404

from app.core.schemas import SetReport

@inteructions_bp.route('/report', methods=['POST'])
@Security.auth_guard()
def reportUser():
    try:
        body = request.get_json()
        schema = SetReport()

        validated_data = schema.load(body)
        ReportService.report_user(request.user_id, **validated_data)
        return jsonify({"data": "reported"})
    except Exception as err:
        return jsonify({"errors": err.messages}), 400
   