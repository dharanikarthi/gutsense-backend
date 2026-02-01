"""
GutSense FastAPI Backend - Simplified for Vercel
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

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

# For Vercel deployment
handler = app