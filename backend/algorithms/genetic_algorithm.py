import random
import numpy as np
import pandas as pd
from config.settings import Config
from data.data_manager import data_manager

class GeneticAlgorithm:
    def __init__(self, user_id, products_df, behavior_df, ratings_df):
        self.user_id = user_id
        self.products_df = products_df
        self.behavior_df = behavior_df
        self.ratings_df = ratings_df
        
        self.pop_size = Config.GA_POPULATION_SIZE
        self.generations = Config.GA_GENERATIONS
        self.base_mutation_rate = Config.GA_MUTATION_RATE
        self.mutation_rate = self.base_mutation_rate
        self.crossover_rate = Config.GA_CROSSOVER_RATE
        self.recommendation_size = 10
        self.elitism_count = 2 # Elitism Strategy
        
        # Fetch detailed tracking events
        self.tracking_events = data_manager.get_user_events(user_id)
        self.recent_recs = data_manager.get_recent_recommendations(user_id, limit=30)

    def calculate_product_scores(self):
        """Pre-calculate scores incorporating deep behavioral tracking."""
        product_scores = {}
        
        # Base stats
        product_views = self.behavior_df.groupby('product_id')['viewed'].sum()
        product_clicks = self.behavior_df.groupby('product_id')['clicked'].sum()
        product_purchases = self.behavior_df.groupby('product_id')['purchased'].sum()
        product_ratings = self.ratings_df.groupby('product_id')['rating'].mean()
        
        # User tracking stats
        user_category_durations = {}
        user_product_clicks = {}
        user_search_queries = []
        
        if not self.tracking_events.empty:
            # Session durations per category
            view_events = self.tracking_events[self.tracking_events['event_type'] == 'view']
            if not view_events.empty:
                user_category_durations = view_events.groupby('category')['duration'].sum().to_dict()
                
            # Click events
            click_events = self.tracking_events[self.tracking_events['event_type'] == 'click']
            if not click_events.empty:
                user_product_clicks = click_events.groupby('product_id').size().to_dict()
                
            # Searches
            search_events = self.tracking_events[self.tracking_events['event_type'] == 'search']
            if not search_events.empty:
                user_search_queries = search_events['search_query'].dropna().str.lower().tolist()

        user_interacted_categories = list(user_category_durations.keys())
        total_duration = sum(user_category_durations.values()) or 1
        
        for _, product in self.products_df.iterrows():
            pid = product['product_id']
            cat = product['category']
            name = str(product['name']).lower()
            
            # Components of fitness
            rating_score = product_ratings.get(pid, 3.0) / 5.0
            popularity_score = (product_views.get(pid, 0) + product_clicks.get(pid, 0) * 2 + product_purchases.get(pid, 0) * 5)
            popularity_score = min(popularity_score / 100.0, 1.0)
            
            # Dynamic User Interest based on session duration & clicks
            interest_score = user_category_durations.get(cat, 0) / total_duration
            click_bonus = min(user_product_clicks.get(pid, 0) * 0.1, 0.5)
            
            # Search alignment
            search_bonus = 0
            if any(q in name or q in str(cat).lower() for q in user_search_queries):
                search_bonus = 0.3
                
            # Weighted Fitness
            fitness = (rating_score * 0.2) + (popularity_score * 0.2) + (interest_score * 0.4) + click_bonus + search_bonus
            
            product_scores[pid] = {
                'score': fitness,
                'interest': interest_score,
                'rating': rating_score,
                'popularity': popularity_score
            }
            
        return product_scores

    def initialize_population(self):
        all_product_ids = self.products_df['product_id'].tolist()
        population = []
        for _ in range(self.pop_size):
            population.append(random.sample(all_product_ids, self.recommendation_size))
        return population

    def calculate_fitness(self, individual, product_scores):
        score = sum(product_scores[pid]['score'] for pid in individual)
        unique_items = len(set(individual))
        diversity_penalty = (self.recommendation_size - unique_items) * 1.5 # Stricter penalty
        
        # Repetition penalty (History)
        repetition_penalty = sum([1.0 for pid in individual if pid in self.recent_recs]) * 0.2
        
        return max(0, score - diversity_penalty - repetition_penalty)

    def selection(self, population, fitness_scores):
        total_fitness = sum(fitness_scores)
        if total_fitness <= 0:
            return random.choices(population, k=2)
        probs = [f / total_fitness for f in fitness_scores]
        return random.choices(population, weights=probs, k=2)

    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            point = random.randint(1, self.recommendation_size - 1)
            return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]
        return parent1, parent2

    def mutation(self, individual, all_product_ids):
        mutated = individual.copy()
        for i in range(len(mutated)):
            if random.random() < self.mutation_rate:
                mutated[i] = random.choice(all_product_ids)
        return mutated

    def run(self):
        product_scores = self.calculate_product_scores()
        all_product_ids = self.products_df['product_id'].tolist()
        population = self.initialize_population()
        
        best_fitness_history = []

        for generation in range(self.generations):
            fitness_scores = [self.calculate_fitness(ind, product_scores) for ind in population]
            current_best = max(fitness_scores)
            best_fitness_history.append(current_best)
            
            # Adaptive Mutation: if fitness isn't improving much, increase mutation rate to escape local optimum
            if generation > 2 and (best_fitness_history[-1] - best_fitness_history[-3]) < 0.1:
                self.mutation_rate = min(self.mutation_rate * 1.2, 0.5) # Increase mutation
            else:
                self.mutation_rate = max(self.mutation_rate * 0.9, self.base_mutation_rate) # Decrease mutation
                
            new_population = []
            
            # Elitism Strategy
            sorted_pop = [x for _, x in sorted(zip(fitness_scores, population), key=lambda pair: pair[0], reverse=True)]
            new_population.extend(sorted_pop[:self.elitism_count])
            
            while len(new_population) < self.pop_size:
                p1, p2 = self.selection(population, fitness_scores)
                c1, c2 = self.crossover(p1, p2)
                new_population.extend([self.mutation(c1, all_product_ids), self.mutation(c2, all_product_ids)])
                
            population = new_population[:self.pop_size]
            
            # Log metrics for dashboard
            data_manager.log_ga_metric(generation, float(current_best), float(self.mutation_rate))
            
        fitness_scores = [self.calculate_fitness(ind, product_scores) for ind in population]
        best_index = np.argmax(fitness_scores)
        best_individual = population[best_index]
        best_score = fitness_scores[best_index]
        
        # Ensure unique and fill
        best_individual_unique = list(dict.fromkeys(best_individual))
        while len(best_individual_unique) < self.recommendation_size:
            extra = random.choice(all_product_ids)
            if extra not in best_individual_unique:
                best_individual_unique.append(extra)
                
        recommended_products = self.products_df[self.products_df['product_id'].isin(best_individual_unique)].to_dict(orient='records')
        avg_interest = np.mean([product_scores[p]['interest'] for p in best_individual_unique])
        
        return {
            "recommended_products": recommended_products,
            "fitness_score": float(best_score),
            "mutation_rate": float(self.mutation_rate),
            "match_percentage": float(min(100.0, best_score / self.recommendation_size * 100)),
            "recommendation_reason": "Based on real-time activity tracking, search intent, and adaptive Genetic Algorithm.",
            "user_interest_analysis": f"Strong alignment with your active categories (Interest score: {avg_interest:.2f})"
        }
