from flask import Blueprint, request, jsonify
from services.user_service import UserService

user_bp = Blueprint('users', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        user = UserService.create_user(
            username=data['username'],
            email=data['email']
        )
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400