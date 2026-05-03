from flask import Blueprint, request, jsonify
from data.data_manager import data_manager
import pandas as pd

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
        
    user = data_manager.users_df[data_manager.users_df['user_id'] == int(user_id)]
    
    if user.empty:
        return jsonify({"error": "User not found"}), 404
        
    return jsonify({"message": "Login successful", "user": user.to_dict(orient='records')[0]}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    age = data.get('age')
    location = data.get('location')
    
    if not age or not location:
        return jsonify({"error": "age and location are required"}), 400
        
    new_id = int(data_manager.users_df['user_id'].max() + 1) if not data_manager.users_df.empty else 1
    
    new_user = pd.DataFrame([{'user_id': new_id, 'age': age, 'location': location}])
    data_manager.users_df = pd.concat([data_manager.users_df, new_user], ignore_index=True)
    data_manager.save_users()
    
    return jsonify({"message": "User registered successfully", "user_id": new_id}), 201
