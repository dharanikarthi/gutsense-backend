"""
GutSense FastAPI Backend - Lightweight for Vercel
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI(
    title="GutSense API",
    description="AI-powered gut health food advisor",
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
        "message": "🦠 GutSense API is running!",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "demo_mode",
        "version": "1.0.0",
        "environment": "production"
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

@app.get("/api/models/status")
async def model_status():
    """Check ML model system status - lightweight version"""
    return {
        "tensorflow_available": False,
        "tensorflow_version": "Not available in lightweight mode",
        "model_loader_available": False,
        "available_models": [],
        "model_count": 0,
        "mode": "lightweight",
        "message": "ML models disabled for Vercel compatibility"
    }

@app.get("/api/models/list")
async def list_models():
    """List available ML models - lightweight version"""
    return {
        "models": [],
        "count": 0,
        "status": "disabled",
        "message": "ML models disabled for Vercel compatibility"
    }

@app.post("/api/models/predict")
async def predict_with_model(request_data: dict):
    """Make prediction using ML model - lightweight version"""
    return {
        "status": "disabled",
        "message": "ML model predictions disabled for Vercel compatibility",
        "suggestion": "Use the demo food analysis endpoint instead: /api/demo/analyze-food"
    }

# For Vercel deployment
handler = app