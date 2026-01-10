from flask import Blueprint, request, jsonify, redirect
from app.services.auth_service import AuthService
from app.core.security import Security
from app.core.schemas import UserLoginSchema, ValidationError

auth_bp = Blueprint('auth_api', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['POST'])
def login() :
    try :
        data = request.get_json()
        if not data:
            raise ValueError("No input data provided")

        schema = UserLoginSchema()

        try:
            validated_data = schema.load(data)
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

        user = AuthService.verify_user(**validated_data)    
        if user is None :
            return jsonify({"error": "Invalid credentials"}), 401
  
        access_token, refresh_token = AuthService.generate_token(id=user.id, username=user.id, request=request)

        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200
    except ValueError as e :
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/oauth/<string:provider>', methods=['POST'])
def proxy_to(provider):
    url = f"http://auth_sidecar:4567/auth/{provider}"
    return redirect(url)


@auth_bp.route('/logout', methods=['POST'])
@Security.auth_guard(check_profile=False, require_verify_mail=False)
def logout() :
    try :
        session_id = request.session_id
        user_id = request.user_id
        
        AuthService.logout(session_id, user_id)
        return jsonify({"success": "logged out!"}), 200
    except ValueError as e :
        return jsonify({"error": str(e)}), 400
 
# @auth_bp.route('/refresh', methods=['POST']) # this will be implemented for the refresh token
# @Security.auth_guard(refresh=True)
# def refresh():
#     current_user = get_jwt_identity()
#     new_token = create_access_token(identity=current_user)
#     return jsonify(access_token=new_token), 200

@auth_bp.route('/forgot_pass', methods=['POST'])
def forgot_pass() :
    try :
        body = request.get_json()
        user_input = body.get('user_input')
        if not isinstance(user_input, str) :
            raise ("Missing required fields")

        AuthService.reset_password(user_input)

        return jsonify({"success": "check your email"}), 200
    except ValueError as e :
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/verify-reset-token', methods=['GET'])
def verify_reset_token():
    try :
        token = request.args.get('token')
        if not token:
            raise ValueError("Token required")
        if AuthService.check_token(token=token) is None :
            return jsonify({"valid": False, "error": "Invalid/expired token"}), 401
        return jsonify({"valid": True}), 200
    except ValueError as e :
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/confirm-reset', methods=['POST'])
def confirm_reset():
    try :
    
        body = request.get_json()
        token = body.get('token')
        new_password = body.get('new_password')

        if not all([token, new_password]):
            raise ValueError("Token and password required")

        AuthService.check_and_reset_token(token=token, new_password=new_password)

        return jsonify({"message": "Password updated successfully"}), 200
    except ValueError as e :
        return jsonify({"error": str(e)}), 400
