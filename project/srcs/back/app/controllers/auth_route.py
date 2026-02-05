from flask import Blueprint, request, jsonify, Response, redirect
from app.services.auth_service import AuthService
from app.core.security import Security
from app.core.schemas import UserLoginSchema, ValidationError
from app.core.config import Config
import requests

from app.dal.repositories.user_repository import UserRepository
from app.dal.models.user import User
# from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token


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




@auth_bp.route('/oauth/<string:provider>', methods=['GET', 'POST'])
def proxy_to(provider):
    try :
        upstream_url = f"http://omni_auth:4567/auth/{provider}"

        headers = dict(request.headers)
        headers['Host'] = Config.PUBLIC_HOST
        headers['X-Forwarded-Proto'] = 'http'

        cookies = request.cookies

        data = request.get_data() if request.method == 'POST' else None

        upstream_resp = requests.request(
            method='POST',
            url=upstream_url,
            headers=headers,
            cookies=cookies,
            data=data,
            params=request.args,
            allow_redirects=False,
            stream=True
        )

        response_headers = []
        for k, v in upstream_resp.headers.items():
            if k.lower() == 'set-cookie':
                v = v.replace("omni_auth", Config.PUBLIC_HOST.split(':')[0])
            elif k.lower() == 'location':
                v = v.replace("omni_auth:4567", Config.PUBLIC_HOST)
            response_headers.append((k, v))

        return Response(
            upstream_resp.raw,
            status=upstream_resp.status_code,
            headers=response_headers,
            content_type=upstream_resp.headers.get('Content-Type')
        )

    except Exception as e:
        print(e, flush=True)
        return jsonify({"error": "unexpected error!"}), 400


@auth_bp.route('/oauth/callback', methods=['GET', 'POST'])
def handle_github_callback():
    try :
        upstream_url = f"http://omni_auth:4567/api/auth/oauth/callback"

        headers = {k: v for k, v in request.headers if k.lower() != 'host'}
        headers['Host'] = Config.PUBLIC_HOST
        headers['X-Forwarded-Proto'] = 'http'


        cookies = request.cookies

        data = request.get_data() if request.method == 'POST' else None

        upstream_resp = requests.request(
            method=request.method,
            url=upstream_url,
            headers=headers,
            cookies=cookies,
            data=data,
            params=request.args,
            allow_redirects=False,
            stream=True
        )

        oauth_user = upstream_resp.json()["infos"]


        user_by_email = UserRepository.find_by_email(oauth_user["email"])

        user_id = None

        if user_by_email and not user_by_email.is_verified :
            user_id = user_by_email.id
            UserRepository.verify_token(user_id)
        if user_by_email:
            user_id = user_by_email.id
            access_token, refresh_token = AuthService.generate_token(id=user_id, username=user_id, request=request)
            return redirect(f"{Config.FRONT_LINK}/auth-success?token={access_token}&refresh={refresh_token}")

        username = oauth_user["nickname"]

        user_by_username = None
        if not user_by_email :
            user_by_username = UserRepository.find_by_username(username)
        
        name_parts = oauth_user["name"].split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""
        
        if not user_by_email and not user_by_username :
            user_id = UserRepository.create_user_oauth(User(
                username=username, 
                email=oauth_user["email"],
                first_name=first_name,
                last_name=last_name)
            )

        if user_by_username :
            username =  UserRepository.generate_unique_username(username)
            user_id = UserRepository.create_user_oauth(User(
                username=username, 
                email=oauth_user["email"],
                first_name=first_name,
                last_name=last_name)
            )
        
        access_token, refresh_token = AuthService.generate_token(id=user_id, username=user_id, request=request)

        return redirect(f"{Config.FRONT_LINK}/auth-success?token={access_token}&refresh={refresh_token}")
    except Exception as e:
        print (e, flush=True)
        return jsonify({"error": "unexpected error!"}), 400

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
 
# @auth_bp.route('/refresh', methods=['POST'])
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
        
        return redirect(f"{Config.FRONT_LINK}/new-password?token={token}", code=302) 
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
