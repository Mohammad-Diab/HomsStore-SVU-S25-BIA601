from flask import Blueprint, jsonify, request
from algorithms.genetic_algorithm import GeneticAlgorithm
from data.data_manager import data_manager

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    # Verify user exists
    if not (data_manager.users_df['user_id'] == user_id).any():
        # Fallback for demo, allow ID 1
        if user_id != 1:
            return jsonify({"error": "User not found"}), 404
        
    ga = GeneticAlgorithm(
        user_id=user_id,
        products_df=data_manager.products_df,
        behavior_df=data_manager.behavior_df,
        ratings_df=data_manager.ratings_df
    )
    
    result = ga.run()
    
    # Log history
    recommended_ids = [p['product_id'] for p in result.get('recommended_products', [])]
    data_manager.log_recommendation_history(user_id, recommended_ids)
    
    return jsonify(result), 200

@recommendations_bp.route('/recommendation-score', methods=['POST'])
def recommendation_score():
    """Allows user/frontend to send feedback on a recommendation"""
    data = request.json
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    score = data.get('score') # e.g. from 1-5 or explicit rating
    
    # Save the new rating to update GA for future
    if user_id and product_id and score:
        new_rating = {'user_id': user_id, 'product_id': product_id, 'rating': score}
        import pandas as pd
        data_manager.ratings_df = pd.concat([data_manager.ratings_df, pd.DataFrame([new_rating])], ignore_index=True)
        data_manager.save_ratings()
        return jsonify({"message": "Recommendation feedback recorded successfully"}), 201
        
    return jsonify({"error": "Missing data"}), 400

@recommendations_bp.route('/user-interest/<int:user_id>', methods=['GET'])
def user_interest(user_id):
    user_behavior = data_manager.behavior_df[data_manager.behavior_df['user_id'] == user_id]
    
    if user_behavior.empty:
        return jsonify({"message": "No behavior data for user"}), 200
        
    user_interacted_products = user_behavior[user_behavior['viewed'] > 0]['product_id'].tolist()
    interacted_categories = data_manager.products_df[data_manager.products_df['product_id'].isin(user_interacted_products)]['category'].tolist()
    
    category_counts = {}
    for cat in interacted_categories:
        category_counts[cat] = category_counts.get(cat, 0) + 1
        
    total_interactions = sum(category_counts.values())
    interest_distribution = {cat: (count / total_interactions) * 100 for cat, count in category_counts.items()}
    
    return jsonify({
        "user_id": user_id,
        "interests": interest_distribution
    }), 200
