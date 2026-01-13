from flask import Blueprint, request, jsonify, redirect
from app.services.user_service import UserService
from app.core.security import Security
from app.core.schemas import UserRegisterSchema, ValidationError
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


@user_bp.route('/verify_account', methods=["GET", "POST"])
def verify_account() :
    try :
        token_id = request.args.get('token_id')
        if not isinstance(token_id, str) :
            return jsonify({"error": "Missing required fields"}), 400

        print (token_id, flush=True)
        value = UserService.verify_account(token=token_id)
        if value :
            return redirect(f"{Config.FRONT_LINK}/confirm-email", code=302) # TODO: maybe to login with success prompt -> profile fill
        else :
            return jsonify({"error": str(value)}), 400
    except ValueError as e :
        return jsonify({"error": str(e)}), 400 # TODO: this should be updated somehow, maybe to login with issue prompt -> resend email

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