from flask import Blueprint, request, jsonify, redirect
from app.services.user_service import UserService
from app.services.profile_service import ProfileService
from app.core.security import Security
from app.core.schemas import UserRegisterSchema, UpdateGeneralUserSchema, ValidationError, UpdateUserPasswordSchema, UpdateLocation
import time

from app.core.config import Config
import logging
logger = logging.getLogger(__name__)

user_bp = Blueprint('user_api', __name__, url_prefix='/user')


@user_bp.route('/create_user', methods=['GET'])
def create_usergeg() :
    return jsonify({"msg":"LOL"}), 200

@user_bp.route('/create_user', methods=['POST'])
def create_user() :

    try:
        data = request.get_json()

        schema = UserRegisterSchema()

        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    try :
        user = UserService.create_user(**validated_data)
        return jsonify({"id": user}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400



@user_bp.route('/verify_account_retry', methods=["POST"])
@Security.auth_guard(require_verify_mail=False, check_profile=False)
def verify_account_retry() :
    try :
        value = UserService.resend_verify_token(request.user_id)
        if value :
            return jsonify({"success": "check your email please"}), 200
        else :
            return jsonify({"error": str(value)}), 400
    except ValueError as e :
        return jsonify({"error": str(e)}), 422

@user_bp.route('/verify_account', methods=["GET", "POST"])
def verify_account() :
    try :
        token_id = request.args.get('token_id')
        if not isinstance(token_id, str) :
            return jsonify({"error": "Missing required fields"}), 400
        value = UserService.verify_account(token=token_id)
        if value :
            return redirect(f"{Config.FRONT_LINK}/confirm-email", code=302)
        else :
            return jsonify({"error": str(value)}), 400
    except ValueError as e :
        return jsonify({"error": str(e)}), 400

@user_bp.route("/protected", methods=["GET", "POST"])
@Security.auth_guard()
def protected() :
    try :
        user_id = request.user_id
        full_name = UserService.get_user_full_name(user_id)

        return jsonify({"user_id": request.user_id, "full_name": full_name})
    except :
        return jsonify({"error": "unexpected error!"}), 400


@user_bp.route("/not_protected", methods=["GET", "POST"])
@Security.auth_guard(check_profile=False)
def not_protected() :
    try :
        user_id = request.user_id
        full_name = UserService.get_user_full_name(user_id)

        return jsonify({"user_id": request.user_id, "full_name": full_name})
    except :
        return jsonify({"error": "unexpected error!"}), 400



@user_bp.route('/change-general-infos', methods=['POST'])
@Security.auth_guard()
def change_general_infos() :
    try :
        body = request.get_json()
        user_id = request.user_id

        schema = UpdateGeneralUserSchema()
        try:
            logger.debug(f"change general infos body route: {body}")
            validated_data = schema.load(body)
        except Exception as err:
            return jsonify({"errors": err.messages}), 400
        was_updated = UserService.update_user_email_request_and_infos(user_id=user_id, **validated_data, session_id=request.session_id)
        if was_updated :
            return jsonify({"success": "profile updated for user"}), 201
        else :
            return jsonify({"error": "profile couldn't be updated for user"}), 409
    except ValueError as e :
        return jsonify({"error": str(e)}), 400
    
@user_bp.route('/verify_change_email', methods=['GET'])
def verify_change_email() :
    try :
        user_id = request.args.get('id')
        session_id = request.args.get('sid')
        token = request.args.get('token')
        email = request.args.get('email')

        if not isinstance(token, str) or not isinstance(email, str) or not \
            isinstance(int(user_id), int) or not isinstance(session_id, str) :
            return jsonify({"error": "Missing required fields"}), 400

        done = UserService.confirm_change(user_id, token, email, session_id)
        if done :
            return jsonify({"success": "email was updated for user"}), 201
        else :
            return jsonify({"error": "email couldn't be updated for user, try again"}), 409
    except ValueError as e :
        return jsonify({"error": str(e)}), 400

@user_bp.route('/update-password', methods=['POST'])
@Security.auth_guard()
def update_password() :
    try :
        body = request.get_json()
        user_id = request.user_id

        schema = UpdateUserPasswordSchema()
        try:
            validated_data = schema.load(body)
        except Exception as err:
            return jsonify({"errors": err.messages}), 400

        was_added = UserService.change_password(user_id=user_id, **validated_data, session_id=request.session_id)
        if was_added :
            return jsonify({"success": "profile updated for user"}), 201
        else :
            return jsonify({"error":"server error"}), 500
    except ValueError as e :
        return jsonify({"error": str(e)}), 400

@user_bp.route('/map',  methods=['GET'])
@Security.auth_guard()
def get_users_in_map():
    try :

        min_lat = request.args.get('min_lat')
        max_lat = request.args.get('max_lat')
        min_lng = request.args.get('min_lng')
        max_lng = request.args.get('max_lng')
        if not min_lat or not max_lat or not min_lng or not max_lng :
            return jsonify({"error": "invalid"}), 400
        else :
            users = UserService.get_range_users(request.user_id, min_lat, max_lat, min_lng, max_lng)

        return jsonify({"data": users})
    
    except Exception as e :
        print(e, flush=True)
        return jsonify({"error": e}), 400


@user_bp.route('/location',  methods=['GET'])
@Security.auth_guard()
def get_user_location():
    try :
        user = UserService.get_user_location(request.user_id)
        return jsonify({"data": user})
    
    except Exception as e :
        print(e, flush=True)
        return jsonify({"error": e}), 400


@user_bp.route('/update-location',  methods=['POST'])
@Security.auth_guard()
def update_user_location():
    try:
        body = request.get_json()
        schema = UpdateLocation()

        validated_data = schema.load(body)
        user = ProfileService.update_location(request.user_id, **validated_data)
        return jsonify({"data": user})
    except Exception as err:
        return jsonify({"errors": err.messages}), 400
    