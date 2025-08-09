from flask import Blueprint, request, jsonify
from app.services.profile_service import ProfileService
from app.core.security import Security
profile_bp = Blueprint('profile_api', __name__, url_prefix='/profile')


@profile_bp.route('/create_profile', methods=['POST'])
@Security.auth_guard()
def create_profile() :
    try :
        body = request.get_json()
        user_id = request.user_id
        if not body or not all(key in body for key in ['gender', 'sexual_preference', 'biography', 'location_set_by_user', 'latitude', 'longitude']):
            return jsonify({"error": "Missing required fields"}), 400

        was_added = ProfileService.create_profile(user_id=user_id, gender=body['gender'],\
                                                   sexual_preference=body['sexual_preference'], \
                                                    biography=body['biography'], \
                                                        location_set_by_user=body['location_set_by_user'], \
                                                            latitude=body['latitude'], longitude=body['longitude'])
        if was_added :
            return jsonify({"profile created for user"}), 201
        else :
            return jsonify({"server error"}), 500
    except ValueError as e :
        return jsonify({"error": str(e)}), 400


@profile_bp.route('/update_profile', methods=['POST'])
@Security.auth_guard()
def update_profile() :
    try :
        body = request.get_json()
        user_id = request.user_id
        if not body or not all(key in body for key in ['gender', 'sexual_preference', 'biography', 'location_set_by_user', 'latitude', 'longitude']):
            return jsonify({"error": "Missing required fields"}), 400

        was_added = ProfileService.update_profile(user_id=user_id, gender=body['gender'],\
                                                   sexual_preference=body['sexual_preference'], \
                                                    biography=body['biography'], \
                                                        location_set_by_user=body['location_set_by_user'], \
                                                            latitude=body['latitude'], longitude=body['longitude'])
        if was_added :
            return jsonify({"profile created for user"}), 201
        else :
            return jsonify({"server error"}), 500
    except ValueError as e :
        return jsonify({"error": str(e)}), 400
