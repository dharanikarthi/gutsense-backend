"""
Rule-based food analysis engine for GutSense
This uses simple IF-ELSE logic to determine food reactions based on gut profiles
"""

import json
from typing import Dict, List, Tuple
from app.models import GutProfile


class FoodAnalysisEngine:
    """Rule-based engine for analyzing food compatibility with gut profiles"""
    
    def __init__(self):
        self.food_categories = {
            # High inflammation foods
            "high_inflammation": [
                "fried chicken", "french fries", "pizza", "burger", "hot dog",
                "fried rice", "fried noodles", "donuts", "chips", "soda",
                "processed meat", "bacon", "sausage", "ice cream", "cake"
            ],
            
            # Spicy foods
            "spicy": [
                "curry", "chili", "hot sauce", "jalapeño", "pepper",
                "spicy pasta", "buffalo wings", "kimchi", "wasabi",
                "sriracha", "cayenne", "paprika", "tabasco"
            ],
            
            # Dairy foods
            "dairy": [
                "milk", "cheese", "yogurt", "butter", "cream",
                "ice cream", "milkshake", "lasagna", "pizza",
                "mac and cheese", "cheesecake", "cottage cheese"
            ],
            
            # Acidic foods
            "acidic": [
                "tomato", "citrus", "orange", "lemon", "lime",
                "grapefruit", "vinegar", "wine", "coffee",
                "tomato sauce", "marinara", "salsa", "pickles"
            ],
            
            # High fiber foods
            "high_fiber": [
                "beans", "lentils", "chickpeas", "broccoli", "cabbage",
                "brussels sprouts", "cauliflower", "whole grains",
                "quinoa", "brown rice", "oats", "bran"
            ],
            
            # Gentle foods
            "gentle": [
                "rice", "banana", "toast", "chicken breast", "fish",
                "sweet potato", "oatmeal", "applesauce", "crackers",
                "plain pasta", "steamed vegetables", "herbal tea"
            ]
        }
    
    def categorize_food(self, food_name: str) -> List[str]:
        """Categorize food based on its name"""
        food_lower = food_name.lower()
        categories = []
        
        for category, foods in self.food_categories.items():
            if any(food in food_lower for food in foods):
                categories.append(category)
        
        return categories
    
    def analyze_food(self, food_name: str, gut_profile: GutProfile) -> Dict:
        """
        Main analysis function using rule-based logic
        Returns reaction, explanation, alternatives, and confidence score
        """
        food_categories = self.categorize_food(food_name)
        sensitivities = gut_profile.sensitivities.split(',') if gut_profile.sensitivities else []
        
        # Initialize result
        result = {
            "reaction": "suitable",
            "explanation": "",
            "alternatives": [],
            "confidence_score": 85,
            "gut_score": 85,
            "tips": []
        }
        
        # Apply rules based on gut type and sensitivities
        reaction, explanation, gut_score = self._apply_gut_rules(
            food_name, food_categories, gut_profile.gut_type, sensitivities, gut_profile.spice_tolerance
        )
        
        result["reaction"] = reaction
        result["explanation"] = explanation
        result["gut_score"] = gut_score
        result["alternatives"] = self._get_alternatives(food_name, reaction)
        result["tips"] = self._get_tips(food_name, reaction, food_categories)
        
        # Adjust confidence based on how specific the match is
        if food_categories:
            result["confidence_score"] = min(95, result["confidence_score"] + len(food_categories) * 5)
        
        return result
    
    def _apply_gut_rules(self, food_name: str, food_categories: List[str], 
                        gut_type: str, sensitivities: List[str], spice_tolerance: int) -> Tuple[str, str, int]:
        """Apply rule-based logic for gut analysis"""
        
        # Check for specific sensitivities first
        if "lactose" in sensitivities and "dairy" in food_categories:
            return "avoid", f"{food_name} contains dairy which may cause discomfort due to your lactose intolerance. This could lead to bloating, gas, and digestive upset.", 15
        
        if "acidity" in sensitivities and "acidic" in food_categories:
            return "caution", f"{food_name} is acidic and might trigger acid reflux based on your profile. Consider having it in smaller portions or with alkaline foods.", 35
        
        if "ibs" in sensitivities and "high_fiber" in food_categories:
            return "caution", f"{food_name} is high in fiber which might cause IBS symptoms. Start with small portions and see how you feel.", 40
        
        # Check spice tolerance
        if "spicy" in food_categories:
            if spice_tolerance == 1:  # Low tolerance
                return "avoid", f"{food_name} is spicy and may cause digestive discomfort given your low spice tolerance. This could lead to stomach irritation.", 20
            elif spice_tolerance == 2:  # Medium tolerance
                return "caution", f"{food_name} is spicy. While you have medium spice tolerance, consider having it in moderation to avoid any discomfort.", 50
        
        # Apply gut type specific rules
        if gut_type == "high_inflammation":
            if "high_inflammation" in food_categories:
                return "avoid", f"{food_name} may increase inflammation in your gut. With your high inflammation profile, it's best to choose anti-inflammatory alternatives.", 25
            elif "gentle" in food_categories:
                return "suitable", f"{food_name} is gentle on the digestive system and suitable for your high inflammation gut profile. This should be easy to digest.", 90
        
        elif gut_type == "low_diversity":
            if "high_fiber" in food_categories:
                return "caution", f"{food_name} is high in fiber. While fiber is good for gut diversity, introduce it gradually to avoid digestive upset.", 45
            elif "gentle" in food_categories:
                return "suitable", f"{food_name} is gentle and suitable for your low diversity gut profile. This can help maintain digestive comfort.", 85
        
        elif gut_type == "balanced":
            if "high_inflammation" in food_categories:
                return "caution", f"{food_name} might cause some inflammation. While your gut is balanced, it's good to enjoy this in moderation.", 60
            elif "gentle" in food_categories:
                return "suitable", f"{food_name} is great for your balanced gut! This food should be well-tolerated and nutritious.", 95
        
        # Default case - no specific rules triggered
        if "gentle" in food_categories:
            return "suitable", f"{food_name} appears to be gentle on the digestive system and should be well-tolerated.", 80
        elif "high_inflammation" in food_categories:
            return "caution", f"{food_name} might cause some digestive stress. Consider having it occasionally rather than regularly.", 55
        else:
            return "suitable", f"{food_name} looks fine for your gut profile. No major concerns identified with this food choice.", 75
    
    def _get_alternatives(self, food_name: str, reaction: str) -> List[str]:
        """Get alternative food suggestions"""
        if reaction == "suitable":
            return []
        
        # Simple alternatives based on food type
        alternatives_map = {
            "pizza": ["whole grain flatbread with vegetables", "cauliflower crust pizza", "grilled chicken salad"],
            "burger": ["grilled chicken sandwich", "turkey burger", "veggie wrap"],
            "ice cream": ["frozen yogurt", "coconut milk ice cream", "fruit sorbet"],
            "fried": ["grilled", "baked", "steamed"],
            "spicy": ["mild seasoned", "herb-crusted", "lemon pepper"],
            "curry": ["mild coconut curry", "turmeric rice", "ginger chicken"],
            "pasta": ["zucchini noodles", "quinoa pasta", "rice noodles"]
        }
        
        food_lower = food_name.lower()
        alternatives = []
        
        for key, alts in alternatives_map.items():
            if key in food_lower:
                alternatives.extend(alts[:2])  # Limit to 2 alternatives
                break
        
        if not alternatives:
            alternatives = ["grilled chicken with rice", "steamed vegetables", "banana and oatmeal"]
        
        return alternatives[:3]  # Maximum 3 alternatives
    
    def _get_tips(self, food_name: str, reaction: str, food_categories: List[str]) -> List[Dict]:
        """Get helpful tips based on food analysis"""
        tips = []
        
        if reaction == "suitable":
            tips.append({
                "icon": "✅",
                "title": "Great choice!",
                "text": "This food aligns well with your gut profile. Enjoy it as part of a balanced diet."
            })
            tips.append({
                "icon": "⏰",
                "title": "Timing tip",
                "text": "Best enjoyed when you're relaxed and can eat slowly for optimal digestion."
            })
        
        elif reaction == "caution":
            tips.append({
                "icon": "🥛",
                "title": "Pairing tip",
                "text": "Consider having this with probiotic yogurt or a glass of water to aid digestion."
            })
            tips.append({
                "icon": "🍽️",
                "title": "Portion tip",
                "text": "Try a smaller portion first to see how your body responds."
            })
        
        elif reaction == "avoid":
            tips.append({
                "icon": "🔄",
                "title": "Alternative tip",
                "text": "Try the suggested alternatives which are more suitable for your gut profile."
            })
            tips.append({
                "icon": "💡",
                "title": "Future tip",
                "text": "Your gut health can improve over time with the right dietary choices."
            })
        
        # Add category-specific tips
        if "spicy" in food_categories:
            tips.append({
                "icon": "🌶️",
                "title": "Spice tip",
                "text": "If you do eat spicy food, have some milk or yogurt nearby to cool your palate."
            })
        
        if "dairy" in food_categories:
            tips.append({
                "icon": "🥥",
                "title": "Dairy alternative",
                "text": "Consider plant-based alternatives like almond, oat, or coconut milk products."
            })
        
        return tips[:2]  # Limit to 2 tips for UI clarity


# Create global instance
food_engine = FoodAnalysisEngine()