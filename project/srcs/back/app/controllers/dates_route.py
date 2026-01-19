from flask import Blueprint, request, jsonify
from app.services.dates_service import DatesService
from app.core.security import Security

dates_bp = Blueprint('dates_api', __name__, url_prefix='/dates')

@dates_bp.route('/propose', methods=['POST'])
@Security.auth_guard()
def propose_date():
    """Propose a date to a matched user"""
    body = request.get_json()
    
    partner_id = body.get('partner_id')
    location = body.get('location')
    datetime_str = body.get('datetime')
    description = body.get('description', '')
    
    date_id = DatesService.propose_date(
        proposer_id=request.user_id,
        partner_id=partner_id,
        location=location,
        datetime_str=datetime_str,
        description=description
    )
    
    return jsonify({"success": True, "date_id": date_id}), 201

@dates_bp.route('/respond/<int:date_id>', methods=['POST'])
@Security.auth_guard()
def respond_to_date(date_id):
    """Accept or decline a date proposal"""
    body = request.get_json()
    status = body.get('status')
    
    DatesService.respond_to_date(
        date_id=date_id,
        responder_id=request.user_id,
        status=status
    )
    
    return jsonify({"success": True}), 200

@dates_bp.route('/my-dates', methods=['GET'])
@Security.auth_guard()
def get_my_dates():
    """Get all dates (proposed and received)"""
    dates = DatesService.get_user_dates(request.user_id)
    return jsonify({"data": dates}), 200