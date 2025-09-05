import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import base64
import requests
import json
from datetime import datetime
import os

# Import our custom modules
from backend.models.food_detector import FoodDetector
from backend.models.calorie_estimator import CalorieEstimator
from backend.utils.image_processor import ImageProcessor

# Page configuration
st.set_page_config(
    page_title="🍎 Calorie Estimation App",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .calorie-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .food-item {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #c3e6cb;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #f5c6cb;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #5a6fd8 0%, #6a4190 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'image_uploaded' not in st.session_state:
    st.session_state.image_uploaded = False

# Initialize models
@st.cache_resource
def load_models():
    """Load ML models with caching"""
    try:
        food_detector = FoodDetector()
        calorie_estimator = CalorieEstimator()
        image_processor = ImageProcessor()
        return food_detector, calorie_estimator, image_processor
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return None, None, None

def process_image(image):
    """Process uploaded image and estimate calories"""
    try:
        # Load models
        food_detector, calorie_estimator, image_processor = load_models()
        
        if not all([food_detector, calorie_estimator, image_processor]):
            return None
        
        # Process the image
        processed_image = image_processor.preprocess(image)
        
        # Detect food items
        food_items = food_detector.detect_food(processed_image)
        
        # Estimate calories for each food item
        results = []
        total_calories = 0
        
        for food_item in food_items:
            calories = calorie_estimator.estimate_calories(
                food_item['name'], 
                food_item['confidence'],
                food_item.get('portion_size', 'medium')
            )
            
            results.append({
                'food_name': food_item['name'],
                'confidence': food_item['confidence'],
                'calories': calories,
                'portion_size': food_item.get('portion_size', 'medium')
            })
            
            total_calories += calories
        
        return {
            'total_calories': round(total_calories, 1),
            'food_items': results,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🍎 AI Calorie Estimation App</h1>
        <p>Take a photo of your food and get instant calorie estimates powered by AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📊 App Info")
        st.info("""
        **How it works:**
        1. 📸 Take a photo or upload an image
        2. 🤖 AI analyzes the food items
        3. 📊 Get calorie estimates instantly
        4. 📱 Works on mobile and desktop
        """)
        
        st.header("🍽️ Food Database")
        st.write("Our AI recognizes:")
        st.write("• 🍎 Fruits (apple, banana, orange, etc.)")
        st.write("• 🥕 Vegetables (carrot, broccoli, tomato, etc.)")
        st.write("• 🥩 Proteins (chicken, beef, fish, etc.)")
        st.write("• 🍞 Grains (bread, rice, pasta, etc.)")
        st.write("• 🍪 Snacks (chips, cookies, nuts, etc.)")
        st.write("• 🥤 Beverages (coffee, tea, juice, etc.)")
        
        st.header("⚙️ Settings")
        portion_size = st.selectbox(
            "Default portion size:",
            ["small", "medium", "large", "extra_large"],
            index=1
        )
        
        confidence_threshold = st.slider(
            "Confidence threshold:",
            min_value=0.1,
            max_value=1.0,
            value=0.5,
            step=0.1
        )
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📸 Upload Your Food Photo")
        
        # Image upload options
        upload_option = st.radio(
            "Choose upload method:",
            ["📷 Take Photo", "📁 Upload Image"]
        )
        
        uploaded_image = None
        
        if upload_option == "📷 Take Photo":
            # Camera input
            camera_image = st.camera_input("Take a photo of your food")
            if camera_image:
                uploaded_image = Image.open(camera_image)
                st.session_state.image_uploaded = True
        
        else:
            # File uploader
            uploaded_file = st.file_uploader(
                "Choose an image file",
                type=['png', 'jpg', 'jpeg', 'gif', 'webp'],
                help="Upload a clear photo of your food for best results"
            )
            
            if uploaded_file:
                uploaded_image = Image.open(uploaded_file)
                st.session_state.image_uploaded = True
        
        # Display uploaded image
        if uploaded_image:
            st.subheader("📷 Your Image")
            st.image(uploaded_image, caption="Uploaded food image", use_column_width=True)
            
            # Process button
            if st.button("🔍 Analyze Food & Estimate Calories", type="primary"):
                with st.spinner("🤖 AI is analyzing your food..."):
                    results = process_image(uploaded_image)
                    if results:
                        st.session_state.results = results
                        st.success("✅ Analysis complete!")
                    else:
                        st.error("❌ Failed to process image. Please try again.")
    
    with col2:
        st.header("📊 Calorie Analysis Results")
        
        if st.session_state.results:
            results = st.session_state.results
            
            # Total calories display
            st.markdown(f"""
            <div class="calorie-card">
                <h2>🔥 Total Calories</h2>
                <h1 style="font-size: 3rem; margin: 0;">{results['total_calories']}</h1>
                <p>Estimated calories in your meal</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Individual food items
            st.subheader("🍽️ Detected Food Items")
            
            for item in results['food_items']:
                confidence_percent = round(item['confidence'] * 100)
                
                # Color code confidence
                if confidence_percent >= 80:
                    confidence_color = "#28a745"  # Green
                elif confidence_percent >= 60:
                    confidence_color = "#ffc107"  # Yellow
                else:
                    confidence_color = "#dc3545"  # Red
                
                st.markdown(f"""
                <div class="food-item">
                    <h4>🍽️ {item['food_name'].title()}</h4>
                    <p><strong>Calories:</strong> {item['calories']:.1f} kcal</p>
                    <p><strong>Portion Size:</strong> {item['portion_size'].title()}</p>
                    <p><strong>Confidence:</strong> <span style="color: {confidence_color};">{confidence_percent}%</span></p>
                </div>
                """, unsafe_allow_html=True)
            
            # Additional information
            st.subheader("ℹ️ Additional Info")
            st.info(f"""
            **Analysis completed at:** {datetime.fromisoformat(results['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}
            
            **Note:** These are estimated values based on AI analysis. For precise nutritional information, 
            consider consulting a nutritionist or using a food scale for accurate measurements.
            """)
            
            # Reset button
            if st.button("🔄 Analyze Another Image"):
                st.session_state.results = None
                st.session_state.image_uploaded = False
                st.rerun()
        
        else:
            if st.session_state.image_uploaded:
                st.info("👆 Click 'Analyze Food & Estimate Calories' to get started!")
            else:
                st.info("📸 Upload an image or take a photo to get started!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🍎 <strong>Calorie Estimation App</strong> | Powered by AI & Computer Vision</p>
        <p>Built with ❤️ using Streamlit, OpenCV, and Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
