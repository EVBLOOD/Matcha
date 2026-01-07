from flask import Blueprint, request, jsonify
from app.services.chat_service import ChatService
from app.core.security import Security



chats_bp = Blueprint('chats_api', __name__, url_prefix='/chats')

@chats_bp.route('/', methods=['GET'])
@Security.auth_guard()
def getChats():
    try :
        return jsonify({"data": ChatService.get_chats(request.user_id)})
    except Exception as e:
        return jsonify({"error": str(e)}), 404
