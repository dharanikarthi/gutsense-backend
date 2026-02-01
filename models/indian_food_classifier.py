"""
Indian Food Classifier - Specialized loader for your .h5 model
"""

import os
import logging
import base64
import io
from typing import Dict, Any, Optional
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IndianFoodClassifier:
    """Specialized classifier for Indian food recognition using your .h5 model"""
    
    def __init__(self):
        self.model = None
        self.model_path = os.path.join(os.path.dirname(__file__), "h5_models")
        self.IMG_SIZE = 224  # Standard size for your model
        
        # Class names from your model (in correct order)
        self.class_names = [
            "Biryani",
            "Butter Chicken", 
            "Dosa",
            "Idli",
            "Paneer Tikka",
            "Samosa"
        ]
        
        # Enhanced food database with gut health analysis
        self.food_analysis = {
            "biryani": {
                "name": "Biryani",
                "category": "indian_rice",
                "spice_level": 4,
                "gut_impact": "high",
                "fermented": False,
                "reaction": "caution",
                "explanation": "Biryani is rich, spicy, and often contains heavy spices and oils. May cause digestive issues for sensitive individuals.",
                "alternatives": ["Plain rice with curry", "Vegetable pulao", "Khichdi"],
                "tips": ["Eat small portions", "Drink buttermilk", "Avoid late night consumption", "Choose vegetable biryani over meat"]
            },
            "butter chicken": {
                "name": "Butter Chicken",
                "category": "indian_curry",
                "spice_level": 3,
                "gut_impact": "high",
                "fermented": False,
                "reaction": "avoid",
                "explanation": "Butter chicken is high in cream, butter, and rich spices. Can be heavy on the digestive system.",
                "alternatives": ["Grilled chicken", "Chicken curry with less cream", "Dal with vegetables"],
                "tips": ["Share the portion", "Eat with plain rice", "Avoid if lactose intolerant", "Drink warm water"]
            },
            "dosa": {
                "name": "Dosa",
                "category": "indian_fermented",
                "spice_level": 1,
                "gut_impact": "low",
                "fermented": True,
                "reaction": "suitable",
                "explanation": "Dosa is fermented and made from rice and lentils, making it gut-friendly. The fermentation aids digestion.",
                "alternatives": ["Idli", "Uttapam", "Plain rice"],
                "tips": ["Choose less oily versions", "Eat with coconut chutney", "Great for breakfast", "Easy to digest"]
            },
            "idli": {
                "name": "Idli",
                "category": "indian_fermented",
                "spice_level": 0,
                "gut_impact": "very_low",
                "fermented": True,
                "reaction": "excellent",
                "explanation": "Idli is the perfect gut-friendly food - steamed, fermented, and easy to digest. Excellent for sensitive stomachs.",
                "alternatives": ["Dosa", "Dhokla", "Steamed rice"],
                "tips": ["Perfect for any time", "Great with coconut chutney", "Ideal for recovery meals", "Safe for all gut types"]
            },
            "paneer tikka": {
                "name": "Paneer Tikka",
                "category": "indian_grilled",
                "spice_level": 3,
                "gut_impact": "medium",
                "fermented": False,
                "reaction": "caution",
                "explanation": "Paneer tikka is grilled and spiced. While paneer is protein-rich, the spices and oil may affect sensitive digestion.",
                "alternatives": ["Grilled vegetables", "Plain paneer curry", "Tofu tikka"],
                "tips": ["Eat in moderation", "Pair with yogurt", "Choose less spicy versions", "Good protein source"]
            },
            "samosa": {
                "name": "Samosa",
                "category": "indian_fried",
                "spice_level": 2,
                "gut_impact": "high",
                "fermented": False,
                "reaction": "avoid",
                "explanation": "Samosas are deep-fried and contain refined flour, making them heavy and difficult to digest.",
                "alternatives": ["Baked samosa", "Steamed momos", "Vegetable cutlets"],
                "tips": ["Occasional treat only", "Eat with green chutney", "Avoid if sensitive", "Drink warm tea after"]
            }
        }
    
    def load_model(self) -> bool:
        """Load the Indian food classifier model"""
        try:
            # Check if TensorFlow is available
            try:
                import tensorflow as tf
                from tensorflow.keras.models import load_model
                logger.info("TensorFlow available, loading model...")
            except ImportError:
                logger.warning("TensorFlow not available - using fallback recognition")
                return False
            
            model_file = os.path.join(self.model_path, "indian_food_classifier.h5")
            
            if not os.path.exists(model_file):
                logger.warning(f"Model file not found: {model_file}")
                return False
            
            # Clear any previous session
            tf.keras.backend.clear_session()
            
            # Load model
            self.model = load_model(model_file, compile=False)
            logger.info("✅ Indian food classifier model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading Indian food classifier: {e}")
            return False
    
    def preprocess_image(self, image_data: str) -> Optional[np.ndarray]:
        """Preprocess image for model prediction"""
        try:
            # Import required libraries
            from PIL import Image
            import numpy as np
            
            # Decode base64 image
            if image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize to model input size
            image = image.resize((self.IMG_SIZE, self.IMG_SIZE))
            
            # Convert to array and normalize
            img_array = np.array(image)
            img_array = img_array / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            return None
    
    def predict_food(self, image_data: str) -> Dict[str, Any]:
        """Predict food from image using the trained model"""
        try:
            # Load model if not already loaded
            if self.model is None:
                if not self.load_model():
                    return self._fallback_prediction()
            
            # Preprocess image
            processed_image = self.preprocess_image(image_data)
            if processed_image is None:
                return self._error_response("Failed to process image")
            
            # Make prediction
            predictions = self.model.predict(processed_image)
            predicted_class = np.argmax(predictions)
            confidence = float(np.max(predictions))
            
            logger.info(f"Raw prediction: {predictions}")
            logger.info(f"Predicted class index: {predicted_class}")
            logger.info(f"Confidence: {confidence}")
            
            # Get class name
            if predicted_class < len(self.class_names):
                predicted_food = self.class_names[predicted_class]
                food_key = predicted_food.lower().replace(" ", " ")
                
                # Get detailed analysis
                analysis = self._get_food_analysis(food_key, predicted_food, confidence)
                analysis["raw_predictions"] = predictions.tolist()
                analysis["all_predictions"] = [
                    {"food": self.class_names[i], "confidence": float(predictions[0][i])}
                    for i in range(len(self.class_names))
                ]
                
                return analysis
            else:
                return self._error_response("Predicted class index out of range")
                
        except Exception as e:
            logger.error(f"Error in food prediction: {e}")
            return self._error_response(f"Prediction failed: {str(e)}")
    
    def _get_food_analysis(self, food_key: str, food_name: str, confidence: float) -> Dict[str, Any]:
        """Get detailed gut health analysis for predicted food"""
        
        # Normalize food key for lookup
        normalized_key = food_key.lower().replace(" ", " ")
        
        if normalized_key in self.food_analysis:
            analysis = self.food_analysis[normalized_key].copy()
        else:
            # Generic analysis for foods not in database
            analysis = {
                "name": food_name,
                "category": "indian",
                "spice_level": 2,
                "gut_impact": "medium",
                "fermented": False,
                "reaction": "caution",
                "explanation": f"{food_name} is an Indian dish. General caution advised for sensitive digestion.",
                "alternatives": ["Idli", "Plain rice", "Steamed vegetables"],
                "tips": ["Eat in moderation", "Monitor your response", "Pair with yogurt"]
            }
        
        # Add ML prediction data
        analysis.update({
            "confidence": int(confidence * 100),
            "ml_confidence": confidence,
            "recognition_method": "ml_model",
            "model_used": "indian_food_classifier",
            "prediction_timestamp": "now"
        })
        
        return analysis
    
    def _fallback_prediction(self) -> Dict[str, Any]:
        """Fallback prediction when model is not available"""
        return {
            "name": "Image Analysis Unavailable",
            "category": "unknown",
            "reaction": "caution",
            "confidence": 0,
            "explanation": "ML model not available. Please enter the food name manually for analysis.",
            "alternatives": ["Enter food name in text", "Use manual food search"],
            "tips": ["Describe the food", "Use specific names", "Try text input"],
            "recognition_method": "fallback",
            "model_used": "none"
        }
    
    def _error_response(self, error_message: str) -> Dict[str, Any]:
        """Generate error response"""
        return {
            "name": "Recognition Error",
            "category": "error",
            "reaction": "caution",
            "confidence": 0,
            "explanation": f"Error: {error_message}",
            "alternatives": ["Try different image", "Enter food name manually"],
            "tips": ["Use clear, well-lit photos", "Show food clearly", "Try again"],
            "recognition_method": "error",
            "error": error_message
        }
    
    def get_supported_foods(self) -> list:
        """Get list of foods the model can recognize"""
        return self.class_names
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the model"""
        return {
            "model_name": "Indian Food Classifier",
            "supported_foods": self.class_names,
            "input_size": f"{self.IMG_SIZE}x{self.IMG_SIZE}",
            "model_loaded": self.model is not None,
            "total_classes": len(self.class_names)
        }

# Global classifier instance
indian_food_classifier = IndianFoodClassifier()