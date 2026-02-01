"""
GutSense FastAPI Backend - Ultra Lightweight for Vercel
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import base64
import io
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="GutSense API",
    description="AI-powered gut health food advisor",
    version="1.0.0"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enhanced food database with better recognition
FOOD_DATABASE = {
    # Indian Foods
    "unniappam": {
        "name": "Unniappam",
        "category": "indian_sweet",
        "description": "Traditional Kerala sweet made with rice flour, jaggery, and coconut",
        "reaction": "caution",
        "confidence": 92,
        "explanation": "Unniappam is high in sugar (jaggery) and may cause digestive issues for sensitive individuals. The coconut and rice flour are generally gut-friendly.",
        "alternatives": ["Steamed idli", "Plain dosa", "Coconut rice"],
        "tips": ["Eat in small portions", "Drink warm water after eating", "Avoid if you have sugar sensitivity"]
    },
    "idli": {
        "name": "Idli",
        "category": "indian",
        "description": "Steamed rice and lentil cakes",
        "reaction": "suitable",
        "confidence": 95,
        "explanation": "Idli is fermented and steamed, making it very gut-friendly and easy to digest.",
        "alternatives": ["Dosa", "Uttapam", "Steamed rice"],
        "tips": ["Best eaten warm", "Pair with coconut chutney", "Good for sensitive stomachs"]
    },
    "dosa": {
        "name": "Dosa",
        "category": "indian",
        "description": "Fermented crepe made from rice and lentils",
        "reaction": "suitable",
        "confidence": 90,
        "explanation": "Dosa is fermented which promotes good gut bacteria, but can be heavy if made with too much oil.",
        "alternatives": ["Idli", "Uttapam", "Plain rice"],
        "tips": ["Choose less oily versions", "Eat with sambar for protein", "Avoid spicy chutneys if sensitive"]
    },
    "biryani": {
        "name": "Biryani",
        "category": "indian",
        "description": "Spiced rice dish with meat or vegetables",
        "reaction": "caution",
        "confidence": 88,
        "explanation": "Biryani is rich and spicy, which may trigger digestive issues in sensitive individuals.",
        "alternatives": ["Plain rice with curry", "Pulao", "Khichdi"],
        "tips": ["Eat small portions", "Drink buttermilk", "Avoid late night consumption"]
    },
    "pizza": {
        "name": "Pizza",
        "category": "italian",
        "description": "Flatbread with cheese and toppings",
        "reaction": "avoid",
        "confidence": 85,
        "explanation": "Pizza is high in processed cheese, refined flour, and often greasy, which can cause digestive distress.",
        "alternatives": ["Whole wheat bread with vegetables", "Grilled chicken salad", "Vegetable soup"],
        "tips": ["Choose thin crust", "Add vegetables", "Limit cheese"]
    },
    "burger": {
        "name": "Burger",
        "category": "american",
        "description": "Sandwich with meat patty and vegetables",
        "reaction": "avoid",
        "confidence": 80,
        "explanation": "Burgers are typically high in processed meat, refined carbs, and unhealthy fats.",
        "alternatives": ["Grilled chicken wrap", "Vegetable sandwich", "Salad bowl"],
        "tips": ["Choose grilled over fried", "Add more vegetables", "Skip the fries"]
    }
}

# Food recognition patterns
FOOD_PATTERNS = {
    "unniappam": ["unniappam", "unniyappam", "sweet ball", "kerala sweet", "jaggery ball"],
    "idli": ["idli", "steamed cake", "white round", "south indian"],
    "dosa": ["dosa", "crepe", "pancake", "fermented"],
    "biryani": ["biryani", "rice dish", "spiced rice", "colored rice"],
    "pizza": ["pizza", "cheese bread", "flatbread", "italian"],
    "burger": ["burger", "sandwich", "patty", "bun"]
}

def recognize_food_from_text(text: str) -> str:
    """Recognize food from text input"""
    text_lower = text.lower()
    
    for food_key, patterns in FOOD_PATTERNS.items():
        for pattern in patterns:
            if pattern in text_lower:
                return food_key
    
    # Default fallback
    return "unknown"

def get_food_analysis(food_key: str, food_name: str = None) -> dict:
    """Get detailed food analysis"""
    if food_key in FOOD_DATABASE:
        analysis = FOOD_DATABASE[food_key].copy()
        return analysis
    
    # Generic analysis for unknown foods
    return {
        "name": food_name or "Unknown Food",
        "category": "unknown",
        "description": "Food not in database",
        "reaction": "caution",
        "confidence": 50,
        "explanation": f"We don't have specific information about {food_name or 'this food'}. Please consult with a nutritionist for personalized advice.",
        "alternatives": ["Steamed vegetables", "Plain rice", "Grilled chicken"],
        "tips": ["Eat in moderation", "Monitor your body's response", "Keep a food diary"]
    }

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
        "database": "enhanced_demo",
        "version": "1.0.0",
        "environment": "production",
        "food_database_size": len(FOOD_DATABASE)
    }

@app.get("/api/demo/food-categories")
async def get_food_categories():
    """Get available food categories"""
    return {
        "categories": [
            {"id": "indian", "name": "Indian", "icon": "🍛"},
            {"id": "indian_sweet", "name": "Indian Sweets", "icon": "🍮"},
            {"id": "italian", "name": "Italian", "icon": "🍕"},
            {"id": "chinese", "name": "Chinese", "icon": "🍜"},
            {"id": "mexican", "name": "Mexican", "icon": "🌮"},
            {"id": "american", "name": "American", "icon": "🍔"},
            {"id": "healthy", "name": "Healthy", "icon": "🥗"}
        ]
    }

@app.post("/api/analyze-food")
async def analyze_food(food_data: dict):
    """Enhanced food analysis endpoint with ML model support"""
    food_name = food_data.get("food_name", "").strip()
    image_data = food_data.get("image", None)
    
    if not food_name and not image_data:
        raise HTTPException(status_code=400, detail="Please provide either food name or image")
    
    # If image is provided, use ML model
    if image_data:
        try:
            from models.indian_food_classifier import indian_food_classifier
            result = indian_food_classifier.predict_food(image_data)
            return result
        except Exception as e:
            logger.error(f"ML prediction failed: {e}")
            # Fallback to text analysis if available
            if food_name:
                food_key = recognize_food_from_text(food_name)
                return get_food_analysis(food_key, food_name)
            else:
                return {
                    "name": "Image Analysis Failed",
                    "category": "error",
                    "reaction": "caution",
                    "confidence": 0,
                    "explanation": "Image analysis failed. Please try again or enter food name manually.",
                    "alternatives": ["Try different image", "Enter food name"],
                    "tips": ["Use clear photos", "Good lighting", "Show food clearly"],
                    "error": str(e)
                }
    
    # Text-based recognition
    if food_name:
        food_key = recognize_food_from_text(food_name)
        analysis = get_food_analysis(food_key, food_name)
        return analysis
    
    raise HTTPException(status_code=400, detail="No valid input provided")

@app.get("/api/models/indian-food-info")
async def get_indian_food_model_info():
    """Get information about the Indian food classifier model"""
    try:
        from models.indian_food_classifier import indian_food_classifier
        return indian_food_classifier.get_model_info()
    except Exception as e:
        return {
            "error": str(e),
            "model_loaded": False,
            "message": "Indian food classifier not available"
        }

@app.post("/api/demo/analyze-food")
async def demo_analyze_food(food_data: dict):
    """Demo food analysis - redirects to main analysis"""
    return await analyze_food(food_data)

@app.get("/api/foods/search")
async def search_foods(q: str = ""):
    """Search for foods in database"""
    if not q:
        return {"foods": list(FOOD_DATABASE.keys())[:10]}
    
    q_lower = q.lower()
    matches = []
    
    for food_key, food_info in FOOD_DATABASE.items():
        if (q_lower in food_key.lower() or 
            q_lower in food_info["name"].lower() or
            q_lower in food_info["description"].lower()):
            matches.append({
                "key": food_key,
                "name": food_info["name"],
                "category": food_info["category"],
                "description": food_info["description"]
            })
    
    return {"foods": matches[:10]}

@app.get("/api/foods/{food_key}")
async def get_food_info(food_key: str):
    """Get detailed information about a specific food"""
    if food_key not in FOOD_DATABASE:
        raise HTTPException(status_code=404, detail="Food not found")
    
    return FOOD_DATABASE[food_key]

# For Vercel deployment
handler = app