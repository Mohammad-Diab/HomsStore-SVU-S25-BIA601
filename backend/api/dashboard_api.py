from flask import Blueprint, jsonify
from data.data_manager import data_manager

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    # Overall summary stats for admin dashboard
    stats = {
        "total_revenue": float(data_manager.products_df[
            data_manager.products_df['product_id'].isin(
                data_manager.behavior_df[data_manager.behavior_df['purchased'] == 1]['product_id']
            )
        ]['price'].sum()),
        "active_users": int(data_manager.behavior_df['user_id'].nunique()),
        "top_category": data_manager.products_df.loc[
            data_manager.products_df['product_id'].isin(
                data_manager.behavior_df[data_manager.behavior_df['purchased'] == 1]['product_id']
            ), 'category'
        ].mode()[0] if not data_manager.behavior_df[data_manager.behavior_df['purchased'] == 1].empty else "N/A"
    }
    return jsonify(stats), 200

@dashboard_bp.route('/dashboard/charts', methods=['GET'])
def get_dashboard_charts():
    import pandas as pd
    
    # Category popularity for Pie Chart
    purchased_products = data_manager.behavior_df[data_manager.behavior_df['purchased'] == 1]['product_id']
    category_counts = data_manager.products_df[data_manager.products_df['product_id'].isin(purchased_products)]['category'].value_counts()
    
    category_chart = [
        {"name": str(category), "value": int(count)} for category, count in category_counts.items()
    ]
    
    # GA Metrics Trend
    try:
        ga_metrics = pd.read_sql_query("SELECT generation, fitness_score, mutation_rate FROM ga_metrics ORDER BY id DESC LIMIT 10", data_manager.conn)
        if ga_metrics.empty:
            accuracy_trend = []
            latest_fitness = 0.0
            latest_mutation = 0.1
        else:
            ga_metrics = ga_metrics.iloc[::-1] # Reverse to get chronological order
            accuracy_trend = [
                {"generation": int(row['generation']), "fitness": float(row['fitness_score'])}
                for _, row in ga_metrics.iterrows()
            ]
            latest_fitness = float(ga_metrics.iloc[-1]['fitness_score'])
            latest_mutation = float(ga_metrics.iloc[-1]['mutation_rate'])
    except Exception as e:
        accuracy_trend = []
        latest_fitness = 0.0
        latest_mutation = 0.1

    return jsonify({
        "category_distribution": category_chart,
        "ga_accuracy_trend": accuracy_trend,
        "latest_fitness": latest_fitness,
        "latest_mutation": latest_mutation
    }), 200
