"""
Model loader for GutSense ML models
"""

import os
import logging
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelLoader:
    """Load and manage ML models for food analysis"""
    
    def __init__(self):
        self.models = {}
        self.model_path = os.path.join(os.path.dirname(__file__), "h5_models")
        
    def load_model(self, model_name: str) -> Optional[object]:
        """Load a specific model by name"""
        try:
            # Check if TensorFlow/Keras is available
            try:
                import tensorflow as tf
                from tensorflow import keras
                TENSORFLOW_AVAILABLE = True
            except ImportError:
                logger.warning("TensorFlow not available. Install with: pip install tensorflow")
                TENSORFLOW_AVAILABLE = False
                return None
            
            model_file = os.path.join(self.model_path, f"{model_name}.h5")
            
            if not os.path.exists(model_file):
                logger.warning(f"Model file not found: {model_file}")
                return None
                
            if model_name not in self.models:
                logger.info(f"Loading model: {model_name}")
                self.models[model_name] = keras.models.load_model(model_file)
                logger.info(f"Model {model_name} loaded successfully")
                
            return self.models[model_name]
            
        except Exception as e:
            logger.error(f"Error loading model {model_name}: {e}")
            return None
    
    def predict(self, model_name: str, input_data) -> Optional[dict]:
        """Make prediction using specified model"""
        try:
            model = self.load_model(model_name)
            if model is None:
                return None
                
            prediction = model.predict(input_data)
            
            return {
                "prediction": prediction.tolist() if hasattr(prediction, 'tolist') else prediction,
                "model_used": model_name,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error making prediction with {model_name}: {e}")
            return {
                "error": str(e),
                "model_used": model_name,
                "status": "error"
            }
    
    def list_available_models(self) -> list:
        """List all available .h5 model files"""
        try:
            if not os.path.exists(self.model_path):
                return []
                
            models = []
            for file in os.listdir(self.model_path):
                if file.endswith('.h5'):
                    models.append(file.replace('.h5', ''))
            return models
            
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []

# Global model loader instance
model_loader = ModelLoader()