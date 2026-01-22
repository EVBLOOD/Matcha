from flask import Blueprint, request, jsonify, send_from_directory
from app.services.profile_service import ProfileService
from app.core.security import Security
from PIL import Image
from app.core.schemas import ProfileSchema, UpdateProfileSchema
from app.core.config import Config
from app.services.report_service import ReportService
from app.core.sanitizer import sanitize_text



profile_bp = Blueprint('profile_api', __name__, url_prefix='/profile')

@profile_bp.route('/pictures/<string:filename>', methods=['GET'])
def serve_uploaded_image(filename):
    return send_from_directory(Config.UPLOAD_FOLDER, filename)

@profile_bp.route('/remove_picture', methods=['POST'])
@Security.auth_guard()
def remove_image():
    try :
        body = request.get_json()
        filename = body.get('filename', '').strip()
        result = ProfileService.remove_picture(request.user_id, filename)

        if not result :
            return jsonify({"error": "Operation couldn't be made."}), 404
        return jsonify({"data": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@profile_bp.route('/<int:user_id>', methods=['GET'])
@Security.auth_guard()
def get_profile(user_id) :
    try :
        return ProfileService.get_profile(request.user_id, user_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 404


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
                return jsonify({"errors": ["No attached files!"]}), 400
        except Exception as err:
            return jsonify({"errors": err.messages}), 400

        if request.headers.get('X-Forwarded-For'):
            ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
        else :
            ip = request.remote_addr

        try :
            was_added = ProfileService.create_profile(user_id=user_id, **validated_data, files_list=files, ip=ip)
        except Exception as e :
            return jsonify({"error": str(e)}), 422

        if was_added :
            return jsonify({"success": "profile created for user"}), 201
        else :
            return jsonify({"error": "server error"}), 409
    except ValueError as e :
        return jsonify({"error": str(e)}), 400

@profile_bp.route('/update_profile', methods=['POST'])
@Security.auth_guard()
def update_profile() :
    try :
        user_id = request.user_id
        body = request.form
        files = request.files
        schema = ProfileSchema()

        try:
            validated_data = schema.load(body)
        except Exception as err:
            return jsonify({"errors": err.messages}), 400

        if request.headers.get('X-Forwarded-For'):
            ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
        else :
            ip = request.remote_addr

        try :
            was_added = ProfileService.update_profile(user_id=user_id, **validated_data, files_list=files, ip=ip)
        except Exception as e :
            return jsonify({"error": str(e)}), 422

        if was_added :
            return jsonify({"success": "profile created for user"}), 201
        else :
            return jsonify({"error": "server error"}), 409
    except ValueError as e :
        return jsonify({"error": str(e)}), 400


@profile_bp.route('/report/<int:user_id>', methods=['POST'])
@Security.auth_guard()
def report_user(user_id):
    """Report a user as fake account"""
    try:
        body = request.get_json()
        reason = body.get('reason', '').strip()
        reason = sanitize_text(reason)
        if len(reason) > 500:
            return jsonify({"error": "Reason too long (max 500 chars)"}), 400
        
        ReportService.report_user(
            reporter_id=request.user_id,
            reported_id=user_id,
            reason=reason
        )
        
        return jsonify({"success": "User reported"}), 201
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400