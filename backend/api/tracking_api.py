from flask import Blueprint, jsonify, request
from data.data_manager import data_manager

tracking_bp = Blueprint('tracking', __name__)

@tracking_bp.route('/track', methods=['POST'])
def track_event():
    data = request.json
    user_id = data.get('user_id', 1) # Default to 1 if not provided for demo purposes
    event_type = data.get('event_type')
    product_id = data.get('product_id')
    category = data.get('category')
    duration = data.get('duration', 0)
    search_query = data.get('search_query')
    
    if not event_type:
        return jsonify({"error": "event_type is required"}), 400
        
    data_manager.log_event(user_id, event_type, product_id, category, duration, search_query)
    
    return jsonify({"status": "success"}), 201
