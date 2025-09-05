import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io

class ImageProcessor:
    """
    Image processing utilities for food image analysis.
    Handles preprocessing, enhancement, and optimization of food images.
    """
    
    def __init__(self):
        self.target_size = (800, 600)  # Standard size for processing
        self.quality_threshold = 0.7  # Minimum quality threshold
    
    def preprocess(self, image):
        """
        Preprocess image for better food detection.
        
        Args:
            image (PIL.Image): Input image
            
        Returns:
            PIL.Image: Preprocessed image
        """
        try:
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image while maintaining aspect ratio
            image = self._resize_image(image)
            
            # Enhance image quality
            image = self._enhance_image(image)
            
            # Apply noise reduction
            image = self._reduce_noise(image)
            
            return image
            
        except Exception as e:
            print(f"Error preprocessing image: {str(e)}")
            return image
    
    def _resize_image(self, image):
        """Resize image while maintaining aspect ratio"""
        # Calculate new dimensions
        width, height = image.size
        target_width, target_height = self.target_size
        
        # Calculate scaling factor
        scale = min(target_width / width, target_height / height)
        
        # Only resize if image is larger than target
        if scale < 1:
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        return image
    
    def _enhance_image(self, image):
        """Enhance image quality for better analysis"""
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.1)
        
        # Enhance color saturation
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.1)
        
        return image
    
    def _reduce_noise(self, image):
        """Reduce image noise while preserving important details"""
        # Convert PIL to OpenCV format
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Apply bilateral filter for noise reduction
        filtered = cv2.bilateralFilter(cv_image, 9, 75, 75)
        
        # Convert back to PIL
        image = Image.fromarray(cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB))
        
        return image
    
    def detect_food_regions(self, image):
        """
        Detect potential food regions in the image.
        
        Args:
            image (PIL.Image): Input image
            
        Returns:
            list: List of detected food regions with bounding boxes
        """
        try:
            # Convert to OpenCV format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Convert to HSV for better color analysis
            hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
            
            # Create mask for food-like colors (excluding very dark/light areas)
            lower_bound = np.array([0, 30, 30])
            upper_bound = np.array([180, 255, 255])
            mask = cv2.inRange(hsv, lower_bound, upper_bound)
            
            # Apply morphological operations to clean up the mask
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filter contours by area and aspect ratio
            food_regions = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:  # Minimum area threshold
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h
                    
                    # Filter by aspect ratio (food items are usually not too elongated)
                    if 0.2 < aspect_ratio < 5.0:
                        food_regions.append({
                            'bbox': (x, y, w, h),
                            'area': area,
                            'contour': contour
                        })
            
            return food_regions
            
        except Exception as e:
            print(f"Error detecting food regions: {str(e)}")
            return []
    
    def extract_food_features(self, image, region):
        """
        Extract features from a food region for classification.
        
        Args:
            image (PIL.Image): Input image
            region (dict): Food region information
            
        Returns:
            dict: Extracted features
        """
        try:
            x, y, w, h = region['bbox']
            
            # Extract region of interest
            roi = image.crop((x, y, x + w, y + h))
            
            # Convert to OpenCV format
            cv_roi = cv2.cvtColor(np.array(roi), cv2.COLOR_RGB2BGR)
            
            # Extract color features
            color_features = self._extract_color_features(cv_roi)
            
            # Extract texture features
            texture_features = self._extract_texture_features(cv_roi)
            
            # Extract shape features
            shape_features = self._extract_shape_features(region)
            
            return {
                'color': color_features,
                'texture': texture_features,
                'shape': shape_features,
                'size': region['area']
            }
            
        except Exception as e:
            print(f"Error extracting features: {str(e)}")
            return {}
    
    def _extract_color_features(self, cv_image):
        """Extract color-based features from image region"""
        # Convert to HSV
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        
        # Calculate mean and standard deviation for each channel
        mean_hsv = np.mean(hsv, axis=(0, 1))
        std_hsv = np.std(hsv, axis=(0, 1))
        
        # Calculate dominant color
        pixels = hsv.reshape(-1, 3)
        unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
        dominant_color = unique_colors[np.argmax(counts)]
        
        return {
            'mean_hsv': mean_hsv.tolist(),
            'std_hsv': std_hsv.tolist(),
            'dominant_color': dominant_color.tolist()
        }
    
    def _extract_texture_features(self, cv_image):
        """Extract texture-based features from image region"""
        # Convert to grayscale
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # Calculate texture features using Local Binary Pattern approximation
        # (Simplified version for demo)
        
        # Calculate gradient magnitude
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        # Calculate texture statistics
        texture_mean = np.mean(gradient_magnitude)
        texture_std = np.std(gradient_magnitude)
        
        return {
            'texture_mean': float(texture_mean),
            'texture_std': float(texture_std)
        }
    
    def _extract_shape_features(self, region):
        """Extract shape-based features from region"""
        x, y, w, h = region['bbox']
        area = region['area']
        
        # Calculate shape features
        aspect_ratio = w / h
        perimeter = cv2.arcLength(region['contour'], True)
        circularity = 4 * np.pi * area / (perimeter ** 2) if perimeter > 0 else 0
        
        return {
            'aspect_ratio': float(aspect_ratio),
            'circularity': float(circularity),
            'area': int(area)
        }
    
    def validate_image_quality(self, image):
        """
        Validate if image quality is sufficient for analysis.
        
        Args:
            image (PIL.Image): Input image
            
        Returns:
            dict: Quality assessment results
        """
        try:
            # Convert to grayscale for analysis
            gray = image.convert('L')
            gray_array = np.array(gray)
            
            # Calculate sharpness using Laplacian variance
            laplacian_var = cv2.Laplacian(gray_array, cv2.CV_64F).var()
            
            # Calculate brightness
            brightness = np.mean(gray_array)
            
            # Calculate contrast
            contrast = np.std(gray_array)
            
            # Determine quality score
            quality_score = min(1.0, (laplacian_var / 1000) * (contrast / 50))
            
            is_good_quality = quality_score > self.quality_threshold
            
            return {
                'quality_score': float(quality_score),
                'is_good_quality': is_good_quality,
                'sharpness': float(laplacian_var),
                'brightness': float(brightness),
                'contrast': float(contrast)
            }
            
        except Exception as e:
            print(f"Error validating image quality: {str(e)}")
            return {
                'quality_score': 0.5,
                'is_good_quality': True,  # Default to True to not block processing
                'sharpness': 0,
                'brightness': 128,
                'contrast': 50
            }

