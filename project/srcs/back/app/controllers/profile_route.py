from flask import Blueprint, request, jsonify
from app.services.profile_service import ProfileService
# from app.services.picture_service import PictureService
from app.core.security import Security
from PIL import Image
from app.core.schemas import ProfileSchema, UpdateProfileSchema



profile_bp = Blueprint('profile_api', __name__, url_prefix='/profile')

@profile_bp.route('/create_profile', methods=['POST'])
@Security.auth_guard(check_profile=False)
def create_profile() :
    try :

        user_id = request.user_id
        body = request.form
        files = request.files
        schema = ProfileSchema()

        try:
            validated_data = schema.load(body)
            if not files :
                raise ValueError("Missing required files")
        except Exception as err:
            return jsonify({"errors": err.messages}), 400

        try :
            was_added = ProfileService.create_profile(user_id=user_id, **validated_data, files_list=files)
        except Exception as e :
            return jsonify({"error": str(e)}), 500

        if was_added :
            return jsonify({"success": "profile created for user"}), 201
        else :
            return jsonify({"error": "server error"}), 500
    except ValueError as e :
        return jsonify({"error": str(e)}), 400


@profile_bp.route('/update_profile', methods=['POST'])
@Security.auth_guard()
def update_profile() :
    try :
        body = request.get_json()
        user_id = request.user_id

        schema = UpdateProfileSchema()
        try:
            validated_data = schema.load(body)
        except Exception as err:
            return jsonify({"errors": err.messages}), 400

        was_added = ProfileService.update_profile(user_id=user_id, **validated_data)
        if was_added :
            return jsonify({"profile updated for user"}), 201
        else :
            return jsonify({"server error"}), 500
    except ValueError as e :
        return jsonify({"error": str(e)}), 400



