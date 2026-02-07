from flask import Blueprint, request, jsonify
from app.services.notifications_service import NotificationService
from app.core.security import Security
from PIL import Image
from app.core.schemas import ProfileSchema, UpdateProfileSchema
from app.core.config import Config



notifs_bp = Blueprint('notifs_api', __name__, url_prefix='/notifs')

@notifs_bp.route('/', methods=['GET'])
@Security.auth_guard()
def getNotifications():
    try :
        return jsonify({"data": NotificationService.get_notifications(request.user_id)})
    except Exception as e:
        return jsonify({"error": str(e)}), 404
