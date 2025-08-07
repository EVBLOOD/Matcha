from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from app.core.security import Security

auth_bp = Blueprint('auth_api', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['POST'])
def login() :
    try :
        data = request.get_json()
        if not data:
            raise ValueError("No input data provided")

        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            raise ValueError("Username and password required")

        user = AuthService.verify_user(username, password)    
        if user is None :
            return jsonify({"error": "Invalid credentials"}), 401
  
        access_token, refresh_token = AuthService.generate_token(id=user.id, username=user.id, request=request)

        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200
    except ValueError as e :
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/logout', methods=['POST'])
@Security.auth_guard()
def logout() :
    try :
        session_id = request.session_id
        
        AuthService.logout(session_id)
        return jsonify({"success": "logged out!"}), 200
    except ValueError as e :
        return jsonify({"error": str(e)}), 400
 
# @auth_bp.route('/refresh', methods=['POST'])
# @jwt_refresh_token_required()
# def refresh():
#     current_user = get_jwt_identity()
#     new_token = create_access_token(identity=current_user)
#     return jsonify(access_token=new_token), 200