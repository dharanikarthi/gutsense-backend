"""
Food Analysis API routes
"""

import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import User, GutProfile, FoodAnalysis
from app.schemas import (
    FoodAnalysisRequest, 
    FoodAnalysisResponse, 
    FoodAnalysisHistory,
    Message
)
from app.auth import get_current_active_user
from app.food_engine import food_engine

router = APIRouter()


@router.post("/analyze", response_model=FoodAnalysisResponse)
async def analyze_food(
    analysis_request: FoodAnalysisRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Analyze food compatibility with user's gut profile"""
    
    # Get user's gut profile
    gut_profile = db.query(GutProfile).filter(GutProfile.user_id == current_user.id).first()
    if not gut_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please create your gut profile first before analyzing foods"
        )
    
    # Analyze food using rule-based engine
    analysis_result = food_engine.analyze_food(analysis_request.food_name, gut_profile)
    
    # Save analysis to database
    db_analysis = FoodAnalysis(
        user_id=current_user.id,
        food_name=analysis_request.food_name,
        food_category=analysis_request.food_category,
        reaction=analysis_result["reaction"],
        explanation=analysis_result["explanation"],
        alternatives=json.dumps(analysis_result["alternatives"]),
        confidence_score=analysis_result["confidence_score"],
        reported_symptoms=analysis_request.reported_symptoms
    )
    
    db.add(db_analysis)
    db.commit()
    
    # Return analysis response
    return FoodAnalysisResponse(
        food_name=analysis_request.food_name,
        reaction=analysis_result["reaction"],
        explanation=analysis_result["explanation"],
        alternatives=analysis_result["alternatives"],
        confidence_score=analysis_result["confidence_score"],
        gut_score=analysis_result["gut_score"],
        tips=analysis_result["tips"]
    )


@router.get("/history", response_model=List[FoodAnalysisHistory])
async def get_food_history(
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's food analysis history"""
    
    analyses = db.query(FoodAnalysis)\
        .filter(FoodAnalysis.user_id == current_user.id)\
        .order_by(FoodAnalysis.created_at.desc())\
        .limit(limit)\
        .all()
    
    return analyses


@router.get("/history/{analysis_id}", response_model=FoodAnalysisHistory)
async def get_food_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get specific food analysis by ID"""
    
    analysis = db.query(FoodAnalysis)\
        .filter(FoodAnalysis.id == analysis_id, FoodAnalysis.user_id == current_user.id)\
        .first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food analysis not found"
        )
    
    return analysis


@router.delete("/history/{analysis_id}", response_model=Message)
async def delete_food_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete specific food analysis"""
    
    analysis = db.query(FoodAnalysis)\
        .filter(FoodAnalysis.id == analysis_id, FoodAnalysis.user_id == current_user.id)\
        .first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food analysis not found"
        )
    
    db.delete(analysis)
    db.commit()
    
    return {"message": "Food analysis deleted successfully"}


@router.delete("/history", response_model=Message)
async def clear_food_history(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Clear all food analysis history for user"""
    
    db.query(FoodAnalysis)\
        .filter(FoodAnalysis.user_id == current_user.id)\
        .delete()
    
    db.commit()
    
    return {"message": "Food history cleared successfully"}


@router.get("/stats")
async def get_food_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's food analysis statistics"""
    
    # Get total analyses
    total_analyses = db.query(FoodAnalysis)\
        .filter(FoodAnalysis.user_id == current_user.id)\
        .count()
    
    # Get reaction counts
    suitable_count = db.query(FoodAnalysis)\
        .filter(FoodAnalysis.user_id == current_user.id, FoodAnalysis.reaction == "suitable")\
        .count()
    
    caution_count = db.query(FoodAnalysis)\
        .filter(FoodAnalysis.user_id == current_user.id, FoodAnalysis.reaction == "caution")\
        .count()
    
    avoid_count = db.query(FoodAnalysis)\
        .filter(FoodAnalysis.user_id == current_user.id, FoodAnalysis.reaction == "avoid")\
        .count()
    
    # Get recent analyses for trends
    recent_analyses = db.query(FoodAnalysis)\
        .filter(FoodAnalysis.user_id == current_user.id)\
        .order_by(FoodAnalysis.created_at.desc())\
        .limit(10)\
        .all()
    
    return {
        "total_analyses": total_analyses,
        "suitable_foods": suitable_count,
        "caution_foods": caution_count,
        "avoid_foods": avoid_count,
        "recent_analyses": [
            {
                "food_name": analysis.food_name,
                "reaction": analysis.reaction,
                "date": analysis.created_at.isoformat()
            }
            for analysis in recent_analyses
        ]
    }


@router.get("/search")
async def search_foods(
    query: str,
    limit: int = 10
):
    """Search for foods (mock implementation for demo)"""
    
    # Mock food database - in production, this would be a real food database
    mock_foods = [
        {"name": "Chicken Curry", "category": "indian", "description": "Spicy Indian dish with chicken"},
        {"name": "Margherita Pizza", "category": "italian", "description": "Classic pizza with tomato and mozzarella"},
        {"name": "Greek Salad", "category": "mediterranean", "description": "Fresh salad with feta cheese"},
        {"name": "Fried Rice", "category": "chinese", "description": "Stir-fried rice with vegetables"},
        {"name": "Cheeseburger", "category": "american", "description": "Beef burger with cheese"},
        {"name": "Spaghetti Carbonara", "category": "italian", "description": "Pasta with eggs and cheese"},
        {"name": "Fish Tacos", "category": "mexican", "description": "Tacos with grilled fish"},
        {"name": "Quinoa Salad", "category": "healthy", "description": "Nutritious grain salad"},
        {"name": "Pad Thai", "category": "thai", "description": "Stir-fried noodles with sweet and sour sauce"},
        {"name": "Caesar Salad", "category": "american", "description": "Romaine lettuce with Caesar dressing"}
    ]
    
    # Filter foods based on query
    query_lower = query.lower()
    matching_foods = [
        food for food in mock_foods 
        if query_lower in food["name"].lower() or query_lower in food["description"].lower()
    ]
    
    return {
        "query": query,
        "results": matching_foods[:limit]
    }