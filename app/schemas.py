"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# Authentication Schemas
class UserCreate(BaseModel):
    """Schema for user registration"""
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class User(BaseModel):
    """Schema for user response"""
    id: int
    name: str
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str
    user: User


# Gut Profile Schemas
class GutProfileCreate(BaseModel):
    """Schema for creating gut profile"""
    gut_type: str  # balanced, high_inflammation, low_diversity
    sensitivities: Optional[List[str]] = []
    spice_tolerance: int = 2  # 1=low, 2=medium, 3=high
    additional_notes: Optional[str] = None


class GutProfileUpdate(BaseModel):
    """Schema for updating gut profile"""
    gut_type: Optional[str] = None
    sensitivities: Optional[List[str]] = None
    spice_tolerance: Optional[int] = None
    additional_notes: Optional[str] = None


class GutProfile(BaseModel):
    """Schema for gut profile response"""
    id: int
    user_id: int
    gut_type: str
    sensitivities: List[str]
    spice_tolerance: int
    additional_notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Food Analysis Schemas
class FoodAnalysisRequest(BaseModel):
    """Schema for food analysis request"""
    food_name: str
    food_category: Optional[str] = None
    reported_symptoms: Optional[str] = None


class FoodAnalysisResponse(BaseModel):
    """Schema for food analysis response"""
    food_name: str
    reaction: str  # suitable, caution, avoid
    explanation: str
    alternatives: List[str]
    confidence_score: int
    gut_score: int  # 0-100 for frontend display
    tips: List[dict]  # List of tip objects with icon, title, text


class FoodAnalysisHistory(BaseModel):
    """Schema for food analysis history"""
    id: int
    food_name: str
    food_category: Optional[str]
    reaction: str
    explanation: str
    confidence_score: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# General Response Schemas
class Message(BaseModel):
    """Schema for general message responses"""
    message: str


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    error: str
    detail: Optional[str] = None