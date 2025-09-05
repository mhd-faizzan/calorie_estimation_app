#!/usr/bin/env python3
"""
Simple test script to verify the calorie estimation app components work correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PIL import Image
import numpy as np
from backend.models.food_detector import FoodDetector
from backend.models.calorie_estimator import CalorieEstimator
from backend.utils.image_processor import ImageProcessor

def create_test_image():
    """Create a simple test image for testing"""
    # Create a simple colored image that might represent food
    img_array = np.random.randint(0, 255, (400, 600, 3), dtype=np.uint8)
    
    # Add some green area (vegetables)
    img_array[100:200, 100:300] = [34, 139, 34]  # Green
    
    # Add some red area (fruits)
    img_array[200:300, 300:500] = [255, 69, 0]   # Red
    
    # Add some brown area (proteins)
    img_array[300:400, 200:400] = [139, 69, 19]  # Brown
    
    return Image.fromarray(img_array)

def test_models():
    """Test the ML models"""
    print("🧪 Testing Calorie Estimation App Components...")
    print("=" * 50)
    
    try:
        # Test 1: Initialize models
        print("1. Initializing models...")
        food_detector = FoodDetector()
        calorie_estimator = CalorieEstimator()
        image_processor = ImageProcessor()
        print("✅ Models initialized successfully!")
        
        # Test 2: Create test image
        print("\n2. Creating test image...")
        test_image = create_test_image()
        print(f"✅ Test image created: {test_image.size}")
        
        # Test 3: Process image
        print("\n3. Processing image...")
        processed_image = image_processor.preprocess(test_image)
        print("✅ Image processed successfully!")
        
        # Test 4: Detect food items
        print("\n4. Detecting food items...")
        food_items = food_detector.detect_food(processed_image)
        print(f"✅ Detected {len(food_items)} food items:")
        for item in food_items:
            print(f"   - {item['name']} (confidence: {item['confidence']:.2f})")
        
        # Test 5: Estimate calories
        print("\n5. Estimating calories...")
        total_calories = 0
        for item in food_items:
            calories = calorie_estimator.estimate_calories(
                item['name'], 
                item['confidence'],
                item.get('portion_size', 'medium')
            )
            total_calories += calories
            print(f"   - {item['name']}: {calories:.1f} calories")
        
        print(f"\n✅ Total estimated calories: {total_calories:.1f}")
        
        # Test 6: Test food database
        print("\n6. Testing food database...")
        foods = calorie_estimator.get_food_database()
        print(f"✅ Food database contains {len(foods)} items")
        
        # Test 7: Test image quality validation
        print("\n7. Testing image quality validation...")
        quality_info = image_processor.validate_image_quality(test_image)
        print(f"✅ Image quality score: {quality_info['quality_score']:.2f}")
        print(f"   - Good quality: {quality_info['is_good_quality']}")
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed! The app is ready to run.")
        print("\nTo start the app, run:")
        print("   streamlit run app.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_models()
    sys.exit(0 if success else 1)
