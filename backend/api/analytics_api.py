from flask import Blueprint, jsonify
from data.data_manager import data_manager

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics', methods=['GET'])
def get_analytics():
    total_users = len(data_manager.users_df)
    total_products = len(data_manager.products_df)
    total_purchases = int(data_manager.behavior_df['purchased'].sum())
    
    return jsonify({
        "total_users": total_users,
        "total_products": total_products,
        "total_purchases": total_purchases
    }), 200

@analytics_bp.route('/user-behavior', methods=['GET'])
def get_user_behavior():
    total_views = int(data_manager.behavior_df['viewed'].sum())
    total_clicks = int(data_manager.behavior_df['clicked'].sum())
    total_purchases = int(data_manager.behavior_df['purchased'].sum())
    
    return jsonify({
        "views": total_views,
        "clicks": total_clicks,
        "purchases": total_purchases
    }), 200

@analytics_bp.route('/click-rate', methods=['GET'])
def get_click_rate():
    total_views = int(data_manager.behavior_df['viewed'].sum())
    total_clicks = int(data_manager.behavior_df['clicked'].sum())
    
    ctr = (total_clicks / total_views * 100) if total_views > 0 else 0
    
    return jsonify({
        "click_through_rate": round(ctr, 2)
    }), 200

@analytics_bp.route('/purchase-rate', methods=['GET'])
def get_purchase_rate():
    total_clicks = int(data_manager.behavior_df['clicked'].sum())
    total_purchases = int(data_manager.behavior_df['purchased'].sum())
    
    ptr = (total_purchases / total_clicks * 100) if total_clicks > 0 else 0
    
    return jsonify({
        "purchase_rate": round(ptr, 2)
    }), 200
