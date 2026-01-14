from flask import Blueprint, request, jsonify, redirect
from app.services.user_service import UserService
from app.core.security import Security
from app.core.schemas import UserRegisterSchema, UpdateGeneralUserSchema, ValidationError, UpdateUserPasswordSchema
import time

from app.core.config import Config

user_bp = Blueprint('user_api', __name__, url_prefix='/user')


@user_bp.route('/create_user', methods=['GET'])
def create_usergeg() :
    return jsonify({"msg":"LOL"}), 200

@user_bp.route('/create_user', methods=['POST'])
def create_user() :
    data = request.get_json()

    schema = UserRegisterSchema()

    try:
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

# @user_bp.route('/init_infos', methods=["POST"])
# def init_infos() :
#     try :
#         # request.user_id : here is the user
        
#     except ValueError as e :
#         return jsonify({"error": str(e)}), 400

@user_bp.route("/protected", methods=["GET", "POST"])
@Security.auth_guard()
def protected() :
    return jsonify({"user_id": request.user_id})

# @user_bp.route("/my_status", methods=["GET", "POST"])
# @Security.auth_guard()
# def my_status() :
#     return jsonify({"result": f"protected {request.user_id}"})

@user_bp.route("/not_protected", methods=["GET", "POST"])
def not_protected() :
    return jsonify({"result": "not_protected"})



@user_bp.route('/change-general-infos', methods=['POST'])
@Security.auth_guard()
def change_general_infos() :
    try :
        body = request.get_json()
        user_id = request.user_id

        schema = UpdateGeneralUserSchema()
        try:
            print(body, flush=True)
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
