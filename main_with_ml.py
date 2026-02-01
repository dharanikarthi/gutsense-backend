"""
GutSense FastAPI Backend - Full ML Version (for dedicated servers)
This version includes TensorFlow and ML model support
Use this when deploying to a server that can handle heavy dependencies
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI(
    title="GutSense API - Full ML Version",
    description="AI-powered gut health food advisor with ML models",
    version="1.0.0"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "https://gutsense-frontend.vercel.app",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "🦠 GutSense API is running with ML support!",
        "version": "1.0.0",
        "status": "healthy",
        "ml_enabled": True
    }

@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "demo_mode",
        "version": "1.0.0",
        "environment": "production",
        "ml_support": True
    }

@app.get("/api/demo/food-categories")
async def get_food_categories():
    """Get available food categories"""
    return {
        "categories": [
            {"id": "indian", "name": "Indian", "icon": "🍛"},
            {"id": "italian", "name": "Italian", "icon": "🍕"},
            {"id": "chinese", "name": "Chinese", "icon": "🍜"},
            {"id": "mexican", "name": "Mexican", "icon": "🌮"},
            {"id": "american", "name": "American", "icon": "🍔"},
            {"id": "healthy", "name": "Healthy", "icon": "🥗"}
        ]
    }

@app.get("/api/demo/gut-types")
async def get_gut_types():
    """Get available gut types"""
    return {
        "gut_types": [
            {"id": "balanced", "name": "Balanced", "description": "Normal digestive health"},
            {"id": "high_inflammation", "name": "High Inflammation", "description": "Prone to inflammatory responses"},
            {"id": "low_diversity", "name": "Low Diversity", "description": "Limited gut microbiome diversity"}
        ]
    }

@app.post("/api/demo/analyze-food")
async def analyze_food(food_data: dict):
    """Demo food analysis endpoint"""
    food_name = food_data.get("food_name", "Unknown Food")
    
    # Simple demo analysis
    return {
        "food_name": food_name,
        "reaction": "suitable",
        "confidence_score": 85,
        "explanation": f"{food_name} appears to be suitable for your gut profile based on general guidelines.",
        "alternatives": ["Grilled chicken", "Steamed vegetables", "Brown rice"],
        "tips": [
            "Eat in moderation",
            "Chew thoroughly",
            "Stay hydrated"
        ]
    }

@app.get("/api/models/list")
async def list_models():
    """List available ML models"""
    try:
        from models.model_loader import model_loader
        models = model_loader.list_available_models()
        return {
            "models": models,
            "count": len(models),
            "status": "success"
        }
    except Exception as e:
        return {
            "models": [],
            "count": 0,
            "status": "error",
            "message": f"Model loading not available: {str(e)}"
        }

@app.post("/api/models/predict")
async def predict_with_model(request_data: dict):
    """Make prediction using ML model"""
    try:
        from models.model_loader import model_loader
        
        model_name = request_data.get("model_name", "default")
        input_data = request_data.get("input_data", [])
        
        if not input_data:
            return {
                "status": "error",
                "message": "No input data provided"
            }
        
        result = model_loader.predict(model_name, input_data)
        
        if result is None:
            return {
                "status": "error",
                "message": f"Model {model_name} not available or failed to load"
            }
            
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Prediction failed: {str(e)}"
        }

@app.get("/api/models/status")
async def model_status():
    """Check ML model system status"""
    try:
        import tensorflow as tf
        tensorflow_version = tf.__version__
        tensorflow_available = True
    except ImportError:
        tensorflow_version = "Not installed"
        tensorflow_available = False
    
    try:
        from models.model_loader import model_loader
        available_models = model_loader.list_available_models()
        model_loader_available = True
    except Exception as e:
        available_models = []
        model_loader_available = False
    
    return {
        "tensorflow_available": tensorflow_available,
        "tensorflow_version": tensorflow_version,
        "model_loader_available": model_loader_available,
        "available_models": available_models,
        "model_count": len(available_models)
    }

# For local development or dedicated server deployment
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)