"""
SQLAlchemy database models for GutSense
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """User model for authentication and profile"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    gut_profile = relationship("GutProfile", back_populates="user", uselist=False)
    food_analyses = relationship("FoodAnalysis", back_populates="user")


class GutProfile(Base):
    """Gut profile model to store user's gut health information"""
    __tablename__ = "gut_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Gut type selection
    gut_type = Column(String, nullable=False)  # balanced, high_inflammation, low_diversity
    
    # Sensitivities (stored as comma-separated values for simplicity)
    sensitivities = Column(Text)  # acidity,ibs,lactose,etc.
    
    # Spice tolerance (1=low, 2=medium, 3=high)
    spice_tolerance = Column(Integer, default=2)
    
    # Additional notes
    additional_notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="gut_profile")


class FoodAnalysis(Base):
    """Food analysis history model"""
    __tablename__ = "food_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Food information
    food_name = Column(String, nullable=False)
    food_category = Column(String)  # indian, italian, healthy, etc.
    
    # Analysis results
    reaction = Column(String, nullable=False)  # suitable, caution, avoid
    explanation = Column(Text, nullable=False)
    alternatives = Column(Text)  # JSON string of alternative foods
    confidence_score = Column(Integer, default=85)  # 0-100
    
    # Optional user symptoms
    reported_symptoms = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="food_analyses")