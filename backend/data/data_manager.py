import pandas as pd
import os
import sqlite3
import datetime
from config.settings import Config

class DataManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
            cls._instance.load_data()
            cls._instance.init_tracking_db()
        return cls._instance

    def load_data(self):
        """Loads data from Excel files into Pandas DataFrames"""
        try:
            self.users_df = pd.read_excel(Config.USERS_FILE) if os.path.exists(Config.USERS_FILE) else pd.DataFrame(columns=['user_id', 'age', 'location'])
            self.products_df = pd.read_excel(Config.PRODUCTS_FILE) if os.path.exists(Config.PRODUCTS_FILE) else pd.DataFrame(columns=['product_id', 'category', 'price', 'name', 'image_url'])
            self.ratings_df = pd.read_excel(Config.RATINGS_FILE) if os.path.exists(Config.RATINGS_FILE) else pd.DataFrame(columns=['user_id', 'product_id', 'rating'])
            self.behavior_df = pd.read_excel(Config.BEHAVIOR_FILE) if os.path.exists(Config.BEHAVIOR_FILE) else pd.DataFrame(columns=['user_id', 'product_id', 'viewed', 'clicked', 'purchased'])
            # Ensure required columns exist with defaults
            for col in ['description', 'stock', 'rating', 'specifications', 'image_url']:
                if col not in self.products_df.columns:
                    defaults = {'description': '', 'stock': 50, 'rating': 4.0, 'specifications': '', 'image_url': ''}
                    self.products_df[col] = defaults[col]
            # Rename 'name' to standardize
            if 'name' in self.products_df.columns and 'product_name' not in self.products_df.columns:
                self.products_df['product_name'] = self.products_df['name']
        except Exception as e:
            print(f"Error loading data: {e}")
            self.users_df = pd.DataFrame(columns=['user_id', 'age', 'location'])
            self.products_df = pd.DataFrame(columns=['product_id', 'category', 'price', 'name', 'image_url'])
            self.ratings_df = pd.DataFrame(columns=['user_id', 'product_id', 'rating'])
            self.behavior_df = pd.DataFrame(columns=['user_id', 'product_id', 'viewed', 'clicked', 'purchased'])

    def reload_data(self):
        """Reload Excel files to pick up any changes dynamically"""
        try:
            self.products_df = pd.read_excel(Config.PRODUCTS_FILE) if os.path.exists(Config.PRODUCTS_FILE) else self.products_df
            for col in ['description', 'stock', 'rating', 'specifications', 'image_url']:
                if col not in self.products_df.columns:
                    defaults = {'description': '', 'stock': 50, 'rating': 4.0, 'specifications': '', 'image_url': ''}
                    self.products_df[col] = defaults[col]
            if 'name' in self.products_df.columns and 'product_name' not in self.products_df.columns:
                self.products_df['product_name'] = self.products_df['name']
        except Exception as e:
            print(f"Error reloading data: {e}")

    def save_users(self):
        self.users_df.to_excel(Config.USERS_FILE, index=False)
        
    def save_behavior(self):
        self.behavior_df.to_excel(Config.BEHAVIOR_FILE, index=False)

    def save_ratings(self):
        self.ratings_df.to_excel(Config.RATINGS_FILE, index=False)

    def init_tracking_db(self):
        db_path = os.path.join(os.path.dirname(Config.USERS_FILE), 'tracking.db')
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tracking_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                event_type TEXT, -- 'view', 'click', 'add_to_cart', 'search', 'purchase'
                product_id INTEGER,
                category TEXT,
                duration INTEGER DEFAULT 0, -- session duration in seconds
                search_query TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ga_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                generation INTEGER,
                fitness_score REAL,
                mutation_rate REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recommendation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def log_event(self, user_id, event_type, product_id=None, category=None, duration=0, search_query=None):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO tracking_events (user_id, event_type, product_id, category, duration, search_query, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, event_type, product_id, category, duration, search_query, datetime.datetime.now()))
        self.conn.commit()

    def get_user_events(self, user_id):
        return pd.read_sql_query(f"SELECT * FROM tracking_events WHERE user_id={user_id}", self.conn)

    def log_ga_metric(self, generation, fitness_score, mutation_rate):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO ga_metrics (generation, fitness_score, mutation_rate)
            VALUES (?, ?, ?)
        ''', (generation, fitness_score, mutation_rate))
        self.conn.commit()

    def log_recommendation_history(self, user_id, product_ids):
        cursor = self.conn.cursor()
        for pid in product_ids:
            cursor.execute('''
                INSERT INTO recommendation_history (user_id, product_id)
                VALUES (?, ?)
            ''', (user_id, pid))
        self.conn.commit()

    def get_recent_recommendations(self, user_id, limit=50):
        return pd.read_sql_query(f"SELECT product_id FROM recommendation_history WHERE user_id={user_id} ORDER BY id DESC LIMIT {limit}", self.conn)['product_id'].tolist()

data_manager = DataManager()
