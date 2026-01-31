"""
Gut Profile API routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import User, GutProfile
from app.schemas import GutProfileCreate, GutProfileUpdate, GutProfile as GutProfileSchema, Message
from app.auth import get_current_active_user

router = APIRouter()


@router.post("/", response_model=GutProfileSchema, status_code=status.HTTP_201_CREATED)
async def create_gut_profile(
    profile_data: GutProfileCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create or update user's gut profile"""
    
    # Validate gut type
    valid_gut_types = ["balanced", "high_inflammation", "low_diversity"]
    if profile_data.gut_type not in valid_gut_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid gut type. Must be one of: {', '.join(valid_gut_types)}"
        )
    
    # Validate spice tolerance
    if profile_data.spice_tolerance not in [1, 2, 3]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Spice tolerance must be 1 (low), 2 (medium), or 3 (high)"
        )
    
    # Check if profile already exists
    existing_profile = db.query(GutProfile).filter(GutProfile.user_id == current_user.id).first()
    
    if existing_profile:
        # Update existing profile
        existing_profile.gut_type = profile_data.gut_type
        existing_profile.sensitivities = ','.join(profile_data.sensitivities) if profile_data.sensitivities else ""
        existing_profile.spice_tolerance = profile_data.spice_tolerance
        existing_profile.additional_notes = profile_data.additional_notes
        
        db.commit()
        db.refresh(existing_profile)
        
        # Convert sensitivities back to list for response
        existing_profile.sensitivities = existing_profile.sensitivities.split(',') if existing_profile.sensitivities else []
        return existing_profile
    else:
        # Create new profile
        db_profile = GutProfile(
            user_id=current_user.id,
            gut_type=profile_data.gut_type,
            sensitivities=','.join(profile_data.sensitivities) if profile_data.sensitivities else "",
            spice_tolerance=profile_data.spice_tolerance,
            additional_notes=profile_data.additional_notes
        )
        
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        
        # Convert sensitivities back to list for response
        db_profile.sensitivities = db_profile.sensitivities.split(',') if db_profile.sensitivities else []
        return db_profile


@router.get("/", response_model=GutProfileSchema)
async def get_gut_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's gut profile"""
    
    profile = db.query(GutProfile).filter(GutProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gut profile not found. Please create one first."
        )
    
    # Convert sensitivities back to list for response
    profile.sensitivities = profile.sensitivities.split(',') if profile.sensitivities else []
    return profile


@router.put("/", response_model=GutProfileSchema)
async def update_gut_profile(
    profile_update: GutProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update user's gut profile"""
    
    profile = db.query(GutProfile).filter(GutProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gut profile not found. Please create one first."
        )
    
    # Update fields if provided
    if profile_update.gut_type is not None:
        valid_gut_types = ["balanced", "high_inflammation", "low_diversity"]
        if profile_update.gut_type not in valid_gut_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid gut type. Must be one of: {', '.join(valid_gut_types)}"
            )
        profile.gut_type = profile_update.gut_type
    
    if profile_update.sensitivities is not None:
        profile.sensitivities = ','.join(profile_update.sensitivities)
    
    if profile_update.spice_tolerance is not None:
        if profile_update.spice_tolerance not in [1, 2, 3]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Spice tolerance must be 1 (low), 2 (medium), or 3 (high)"
            )
        profile.spice_tolerance = profile_update.spice_tolerance
    
    if profile_update.additional_notes is not None:
        profile.additional_notes = profile_update.additional_notes
    
    db.commit()
    db.refresh(profile)
    
    # Convert sensitivities back to list for response
    profile.sensitivities = profile.sensitivities.split(',') if profile.sensitivities else []
    return profile


@router.delete("/", response_model=Message)
async def delete_gut_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete user's gut profile"""
    
    profile = db.query(GutProfile).filter(GutProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gut profile not found"
        )
    
    db.delete(profile)
    db.commit()
    
    return {"message": "Gut profile deleted successfully"}


@router.get("/gut-types")
async def get_available_gut_types():
    """Get list of available gut types with descriptions"""
    return {
        "gut_types": [
            {
                "value": "balanced",
                "label": "Balanced Gut",
                "description": "Generally healthy digestion with occasional minor issues"
            },
            {
                "value": "high_inflammation",
                "label": "High Inflammation",
                "description": "Prone to inflammatory responses, sensitive to certain foods"
            },
            {
                "value": "low_diversity",
                "label": "Low Diversity",
                "description": "Limited gut bacteria diversity, may need gradual dietary changes"
            }
        ]
    }


@router.get("/sensitivities")
async def get_available_sensitivities():
    """Get list of available gut sensitivities"""
    return {
        "sensitivities": [
            {
                "value": "acidity",
                "label": "Acidity / Acid Reflux",
                "description": "Sensitive to acidic foods and drinks"
            },
            {
                "value": "ibs",
                "label": "IBS (Irritable Bowel Syndrome)",
                "description": "Digestive disorder affecting the large intestine"
            },
            {
                "value": "ulcer",
                "label": "Ulcer Sensitivity",
                "description": "Stomach ulcer concerns and related sensitivities"
            },
            {
                "value": "lactose",
                "label": "Lactose Intolerance",
                "description": "Difficulty digesting dairy products"
            },
            {
                "value": "sensitive",
                "label": "Sensitive Digestion",
                "description": "General digestive sensitivity, bloating, and discomfort"
            }
        ]
    }