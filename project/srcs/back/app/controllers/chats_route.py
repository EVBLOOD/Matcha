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

@chats_bp.route('/<int:conversation_id>', methods=['GET'])
@Security.auth_guard()
def getMessages(conversation_id):
    try :
        print(f"conversation_id {conversation_id}", flush=True)
        return jsonify({"data": ChatService.get_messages(request.user_id, conversation_id)})
    except Exception as e:
        return jsonify({"error": str(e)}), 404
