from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt, get_jwt_identity
from functools import wraps
from flask import jsonify
from app.services.auth_service import AuthService
from flask import request


class Security :
    jwt = JWTManager()

    def init_jwt(self,app):
        self.jwt.init_app(app)

    @staticmethod
    # def auth_guard(refresh=True, required_roles=None):
    def auth_guard(required_roles=None, check_profile=True) :
        def decorator(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):

                try:
                        
                    verify_jwt_in_request()
                    claims = get_jwt()
                    message, status = AuthService.validate_token(claims["user_id"], get_jwt_identity())
                    if status != 200 :
                        raise Exception(message)
                    # This maybe will be moved down when working with the admin role
                    if check_profile and not AuthService.check_profile_completion(claims["user_id"]) :
                        return jsonify({"error": "profile completion required"}), 301
                except Exception as e:
                    return jsonify({"error": str(e)}), 401

                if required_roles:
                    claims = get_jwt()
                    user_roles = claims.get("roles", [])
                    if not set(required_roles).intersection(user_roles):
                        return jsonify({"error": "Insufficient permissions"}), 403
                request.session_id = get_jwt_identity()
                print (request.session_id, flush=True)
                request.user_id = claims["user_id"]
                return fn(*args, **kwargs)
            return wrapper
        return decorator
    
