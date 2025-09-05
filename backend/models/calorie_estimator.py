import json
import os

class CalorieEstimator:
    """
    Calorie estimation class that calculates calories for detected food items.
    Uses a comprehensive food database with nutritional information.
    """
    
    def __init__(self):
        self.food_database = self._load_food_database()
        self.portion_multipliers = {
            'small': 0.5,
            'medium': 1.0,
            'large': 1.5,
            'extra_large': 2.0
        }
    
    def _load_food_database(self):
        """Load comprehensive food database with calorie information"""
        return {
            # Fruits (per 100g)
            'apple': {'calories_per_100g': 52, 'category': 'fruits'},
            'banana': {'calories_per_100g': 89, 'category': 'fruits'},
            'orange': {'calories_per_100g': 47, 'category': 'fruits'},
            'strawberry': {'calories_per_100g': 32, 'category': 'fruits'},
            'grape': {'calories_per_100g': 62, 'category': 'fruits'},
            'lemon': {'calories_per_100g': 29, 'category': 'fruits'},
            'mixed fruits': {'calories_per_100g': 50, 'category': 'fruits'},
            
            # Vegetables (per 100g)
            'carrot': {'calories_per_100g': 41, 'category': 'vegetables'},
            'broccoli': {'calories_per_100g': 34, 'category': 'vegetables'},
            'tomato': {'calories_per_100g': 18, 'category': 'vegetables'},
            'lettuce': {'calories_per_100g': 15, 'category': 'vegetables'},
            'cucumber': {'calories_per_100g': 16, 'category': 'vegetables'},
            'onion': {'calories_per_100g': 40, 'category': 'vegetables'},
            'mixed vegetables': {'calories_per_100g': 25, 'category': 'vegetables'},
            
            # Proteins (per 100g)
            'chicken': {'calories_per_100g': 165, 'category': 'proteins'},
            'beef': {'calories_per_100g': 250, 'category': 'proteins'},
            'fish': {'calories_per_100g': 206, 'category': 'proteins'},
            'egg': {'calories_per_100g': 155, 'category': 'proteins'},
            'cheese': {'calories_per_100g': 113, 'category': 'proteins'},
            'yogurt': {'calories_per_100g': 59, 'category': 'proteins'},
            
            # Grains (per 100g)
            'bread': {'calories_per_100g': 265, 'category': 'grains'},
            'rice': {'calories_per_100g': 130, 'category': 'grains'},
            'pasta': {'calories_per_100g': 131, 'category': 'grains'},
            'cereal': {'calories_per_100g': 350, 'category': 'grains'},
            'oats': {'calories_per_100g': 389, 'category': 'grains'},
            
            # Snacks (per 100g)
            'chips': {'calories_per_100g': 536, 'category': 'snacks'},
            'cookies': {'calories_per_100g': 488, 'category': 'snacks'},
            'candy': {'calories_per_100g': 400, 'category': 'snacks'},
            'nuts': {'calories_per_100g': 607, 'category': 'snacks'},
            'chocolate': {'calories_per_100g': 546, 'category': 'snacks'},
            
            # Beverages (per 100ml)
            'coffee': {'calories_per_100g': 2, 'category': 'beverages'},
            'tea': {'calories_per_100g': 1, 'category': 'beverages'},
            'juice': {'calories_per_100g': 45, 'category': 'beverages'},
            'soda': {'calories_per_100g': 42, 'category': 'beverages'},
            'water': {'calories_per_100g': 0, 'category': 'beverages'},
            'milk': {'calories_per_100g': 42, 'category': 'beverages'},
            
            # Mixed/General foods
            'mixed food': {'calories_per_100g': 200, 'category': 'mixed'},
            'cooked food': {'calories_per_100g': 180, 'category': 'mixed'},
            'salad': {'calories_per_100g': 50, 'category': 'mixed'},
            'sandwich': {'calories_per_100g': 250, 'category': 'mixed'},
            'pizza': {'calories_per_100g': 266, 'category': 'mixed'},
            'burger': {'calories_per_100g': 295, 'category': 'mixed'},
            'pasta_dish': {'calories_per_100g': 200, 'category': 'mixed'},
            'soup': {'calories_per_100g': 80, 'category': 'mixed'},
        }
    
    def estimate_calories(self, food_name, confidence, portion_size='medium'):
        """
        Estimate calories for a given food item.
        
        Args:
            food_name (str): Name of the food item
            confidence (float): Confidence score from detection (0-1)
            portion_size (str): Size of the portion ('small', 'medium', 'large', 'extra_large')
        
        Returns:
            float: Estimated calories
        """
        try:
            # Normalize food name (lowercase, remove spaces)
            normalized_name = food_name.lower().strip()
            
            # Find matching food in database
            food_info = self._find_food_match(normalized_name)
            
            if not food_info:
                # If no exact match, try to find similar foods
                food_info = self._find_similar_food(normalized_name)
            
            if not food_info:
                # Default to mixed food if no match found
                food_info = self.food_database.get('mixed food', {'calories_per_100g': 200})
            
            # Get base calories per 100g
            base_calories = food_info['calories_per_100g']
            
            # Apply portion size multiplier
            portion_multiplier = self.portion_multipliers.get(portion_size, 1.0)
            
            # Estimate weight based on portion size (rough estimates)
            estimated_weight = self._estimate_weight(portion_size, food_info['category'])
            
            # Calculate total calories
            total_calories = (base_calories * estimated_weight / 100) * portion_multiplier
            
            # Apply confidence adjustment (reduce calories if confidence is low)
            confidence_adjustment = 0.7 + (confidence * 0.3)  # Range: 0.7 to 1.0
            adjusted_calories = total_calories * confidence_adjustment
            
            return max(10, adjusted_calories)  # Minimum 10 calories
            
        except Exception as e:
            print(f"Error estimating calories for {food_name}: {str(e)}")
            return 150  # Default fallback calories
    
    def _find_food_match(self, food_name):
        """Find exact match in food database"""
        return self.food_database.get(food_name)
    
    def _find_similar_food(self, food_name):
        """Find similar food items using keyword matching"""
        # Simple keyword matching
        keywords = food_name.split()
        
        for db_food, info in self.food_database.items():
            db_keywords = db_food.split()
            
            # Check if any keywords match
            if any(keyword in db_keywords for keyword in keywords):
                return info
        
        return None
    
    def _estimate_weight(self, portion_size, category):
        """
        Estimate weight in grams based on portion size and food category.
        These are rough estimates for typical serving sizes.
        """
        base_weights = {
            'fruits': {'small': 80, 'medium': 150, 'large': 250, 'extra_large': 350},
            'vegetables': {'small': 60, 'medium': 120, 'large': 200, 'extra_large': 300},
            'proteins': {'small': 100, 'medium': 150, 'large': 250, 'extra_large': 350},
            'grains': {'small': 50, 'medium': 100, 'large': 150, 'extra_large': 200},
            'snacks': {'small': 30, 'medium': 60, 'large': 100, 'extra_large': 150},
            'beverages': {'small': 150, 'medium': 250, 'large': 350, 'extra_large': 500},
            'mixed': {'small': 100, 'medium': 200, 'large': 300, 'extra_large': 400}
        }
        
        return base_weights.get(category, base_weights['mixed']).get(portion_size, 150)
    
    def get_food_database(self):
        """Get the complete food database"""
        return self.food_database
    
    def get_foods_by_category(self, category):
        """Get all foods in a specific category"""
        return {name: info for name, info in self.food_database.items() 
                if info['category'] == category}
    
    def add_custom_food(self, name, calories_per_100g, category='custom'):
        """Add a custom food item to the database"""
        self.food_database[name.lower()] = {
            'calories_per_100g': calories_per_100g,
            'category': category
        }
    
    def get_nutritional_info(self, food_name):
        """Get detailed nutritional information for a food item"""
        food_info = self._find_food_match(food_name.lower())
        if food_info:
            return {
                'name': food_name,
                'calories_per_100g': food_info['calories_per_100g'],
                'category': food_info['category'],
                'portion_sizes': list(self.portion_multipliers.keys())
            }
        return None

