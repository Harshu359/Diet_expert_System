def forward_chaining_constraints(user_profile):
    """
    Forward Chaining: Takes base user facts (allergies, health conditions)
    and infers a strict set of active safety constraints.
    """
    constraints = {
        "excluded_allergens": [],
        "max_sodium": 1000,  # default high limit
        "diabetic_friendly_only": False
    }
    
    # Rule 1: Allergy check
    if "allergies" in user_profile:
        constraints["excluded_allergens"].extend(user_profile["allergies"])
        
    # Rule 2: Health condition check (e.g., Hypertension)
    if user_profile.get("has_hypertension"):
        constraints["max_sodium"] = 300  # Stricter sodium rule
        
    # Rule 3: Health condition check (e.g., Diabetes)
    if user_profile.get("has_diabetes"):
        constraints["diabetic_friendly_only"] = True
        
    return constraints

def backward_chaining_goal_check(recipe, target_goal):
    """
    Backward Chaining: Starts from a target nutritional goal (e.g., 'High Protein')
    and works backward to see if the recipe satisfies the sub-conditions.
    """
    if target_goal == "High Protein":
        # Sub-condition: Must have >= 25g protein
        return recipe.get("protein", 0) >= 25
    elif target_goal == "Low Calorie":
        # Sub-condition: Must have <= 350 calories
        return recipe.get("calories", 500) <= 350
    
    return True  # If no specific goal is targeted