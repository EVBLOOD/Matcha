from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

user_bp = Blueprint('user_api', __name__, url_prefix='/user')


@user_bp.route('/create_user', methods=['GET'])
def create_usergeg() :
    return jsonify({"msg":"LOL"}), 200

@user_bp.route('/create_user', methods=['POST'])
def create_user() :
    data = request.get_json()
    if not data or not all(key in data for key in ['username', 'email', 'password', 'first_name', 'last_name']):
        return jsonify({"error": "Missing required fields"}), 400
    try :
        user = UserService.create_user(username=data['username'], 
                                       email=data['email'],
                                       password=data['password'],
                                       first_name=data['first_name'],
                                       last_name=data['last_name']
                                       )
        return jsonify({"id": user}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
# latitude
# longitude

@user_bp.route('/verify_account', methods=["GET", "POST"])
def verify_account() :
    try :
        token_id = request.args.get('token_id')
        if not isinstance(token_id, str) :
            return jsonify({"error": "Missing required fields"}), 400

        print (token_id, flush=True)
        UserService.verify_account(token=token_id)
        return jsonify({"result": "success"}), 201
    except ValueError as e :
        return jsonify({"error": str(e)}), 400

@user_bp.route('/init_infos', methods=["POST"])
def init_infos() :
    try :
        # get the user id or token from front cache or header
        token = request.headers.get('Authorization')
        if token == None or not isinstance(token, str) :
            return jsonify({"error": "Non Authorized!"}), 403
        token_spliter = stoken.split()
        # decrypt the token
        
    except ValueError as e :
        return jsonify({"error": str(e)}), 400