import cv2
import numpy as np
from PIL import Image
import json
import os

class FoodDetector:
    """
    Food detection class that identifies food items in images.
    For this demo, we'll use a simplified approach with color analysis
    and basic computer vision techniques.
    """
    
    def __init__(self):
        self.food_categories = {
            'fruits': ['apple', 'banana', 'orange', 'strawberry', 'grape', 'lemon'],
            'vegetables': ['carrot', 'broccoli', 'tomato', 'lettuce', 'cucumber', 'onion'],
            'proteins': ['chicken', 'beef', 'fish', 'egg', 'cheese', 'yogurt'],
            'grains': ['bread', 'rice', 'pasta', 'cereal', 'oats'],
            'snacks': ['chips', 'cookies', 'candy', 'nuts', 'chocolate'],
            'beverages': ['coffee', 'tea', 'juice', 'soda', 'water', 'milk']
        }
        
        # Color ranges for different food types (HSV)
        self.color_ranges = {
            'fruits': [(0, 50, 50), (20, 255, 255)],  # Red/Orange
            'vegetables': [(35, 50, 50), (85, 255, 255)],  # Green
            'proteins': [(0, 0, 0), (180, 255, 100)],  # Brown/White
            'grains': [(20, 50, 50), (35, 255, 255)],  # Yellow/Brown
        }
    
    def detect_food(self, image):
        """
        Detect food items in the given image.
        Returns a list of detected food items with confidence scores.
        """
        try:
            # Convert PIL image to OpenCV format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Apply image preprocessing
            processed_image = self._preprocess_image(cv_image)
            
            # Detect food regions
            food_regions = self._detect_food_regions(processed_image)
            
            # Classify detected regions
            detected_foods = []
            for region in food_regions:
                food_item = self._classify_food_region(cv_image, region)
                if food_item:
                    detected_foods.append(food_item)
            
            # If no specific foods detected, provide a general estimate
            if not detected_foods:
                detected_foods = self._general_food_estimation(cv_image)
            
            return detected_foods
            
        except Exception as e:
            print(f"Error in food detection: {str(e)}")
            # Return a default food item if detection fails
            return [{
                'name': 'mixed food',
                'confidence': 0.5,
                'portion_size': 'medium'
            }]
    
    def _preprocess_image(self, image):
        """Preprocess image for better food detection"""
        # Resize image for faster processing
        height, width = image.shape[:2]
        if width > 800:
            scale = 800 / width
            new_width = 800
            new_height = int(height * scale)
            image = cv2.resize(image, (new_width, new_height))
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        
        # Convert to HSV for better color analysis
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        return hsv
    
    def _detect_food_regions(self, hsv_image):
        """Detect potential food regions in the image"""
        food_regions = []
        
        # Create masks for different food color ranges
        for category, (lower, upper) in self.color_ranges.items():
            mask = cv2.inRange(hsv_image, np.array(lower), np.array(upper))
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:  # Filter out small regions
                    x, y, w, h = cv2.boundingRect(contour)
                    food_regions.append({
                        'bbox': (x, y, w, h),
                        'area': area,
                        'category': category
                    })
        
        return food_regions
    
    def _classify_food_region(self, image, region):
        """Classify a specific food region"""
        x, y, w, h = region['bbox']
        roi = image[y:y+h, x:x+w]
        
        # Analyze color distribution
        dominant_colors = self._get_dominant_colors(roi)
        
        # Simple classification based on color and shape
        food_name = self._classify_by_features(region, dominant_colors)
        
        if food_name:
            return {
                'name': food_name,
                'confidence': min(0.9, region['area'] / 10000),  # Simple confidence based on size
                'portion_size': self._estimate_portion_size(region['area'])
            }
        
        return None
    
    def _get_dominant_colors(self, roi):
        """Get dominant colors in the region of interest"""
        # Reshape image to be a list of pixels
        pixels = roi.reshape(-1, 3)
        
        # Convert to HSV
        hsv_pixels = cv2.cvtColor(pixels.reshape(1, -1, 3), cv2.COLOR_BGR2HSV).reshape(-1, 3)
        
        # Get mean HSV values
        mean_hsv = np.mean(hsv_pixels, axis=0)
        
        return mean_hsv
    
    def _classify_by_features(self, region, colors):
        """Classify food based on region features and colors"""
        category = region['category']
        h, s, v = colors
        
        # Simple classification rules
        if category == 'fruits':
            if h < 20:  # Red/Orange
                return 'apple' if s > 100 else 'orange'
            elif h < 40:  # Yellow
                return 'banana'
            else:
                return 'strawberry'
        
        elif category == 'vegetables':
            if s > 100:  # High saturation green
                return 'broccoli' if region['area'] > 5000 else 'lettuce'
            else:
                return 'carrot'
        
        elif category == 'proteins':
            if v > 150:  # Light colored
                return 'chicken' if region['area'] > 3000 else 'cheese'
            else:
                return 'beef'
        
        elif category == 'grains':
            return 'bread' if region['area'] > 2000 else 'rice'
        
        return None
    
    def _estimate_portion_size(self, area):
        """Estimate portion size based on detected area"""
        if area > 15000:
            return 'large'
        elif area > 5000:
            return 'medium'
        else:
            return 'small'
    
    def _general_food_estimation(self, image):
        """Provide general food estimation when specific detection fails"""
        # Analyze overall image characteristics
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Check for common food colors
        green_mask = cv2.inRange(hsv, np.array([35, 50, 50]), np.array([85, 255, 255]))
        red_mask = cv2.inRange(hsv, np.array([0, 50, 50]), np.array([20, 255, 255]))
        brown_mask = cv2.inRange(hsv, np.array([10, 50, 50]), np.array([25, 255, 255]))
        
        green_pixels = cv2.countNonZero(green_mask)
        red_pixels = cv2.countNonZero(red_mask)
        brown_pixels = cv2.countNonZero(brown_mask)
        
        total_pixels = image.shape[0] * image.shape[1]
        
        # Estimate based on dominant colors
        if green_pixels > total_pixels * 0.1:
            return [{'name': 'mixed vegetables', 'confidence': 0.6, 'portion_size': 'medium'}]
        elif red_pixels > total_pixels * 0.1:
            return [{'name': 'mixed fruits', 'confidence': 0.6, 'portion_size': 'medium'}]
        elif brown_pixels > total_pixels * 0.1:
            return [{'name': 'cooked food', 'confidence': 0.6, 'portion_size': 'medium'}]
        else:
            return [{'name': 'mixed food', 'confidence': 0.5, 'portion_size': 'medium'}]

