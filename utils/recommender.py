from utils.rules import forward_chaining_constraints, backward_chaining_goal_check

def get_recommendations(user_profile, target_goal, recipes):
    """
    Applies forward-chaining constraints to filter out unsafe recipes,
    then applies backward-chaining goal checks and scores the matches.
    """
    # Step 1: Get active constraints via Forward Chaining
    constraints = forward_chaining_constraints(user_profile)
    
    filtered_recipes = []
    explanations = {}

    for recipe in recipes:
        # Check 1: Allergen check (Forward Chaining rule output)
        has_allergen = any(allergen in constraints["excluded_allergens"] for allergen in recipe["allergens"])
        if has_allergen:
            explanations[recipe["name"]] = f"Excluded: Contains allergens matching your profile ({recipe['allergens']})."
            continue
            
        # Check 2: Sodium limit check
        if recipe["sodium"] > constraints["max_sodium"]:
            explanations[recipe["name"]] = f"Excluded: Sodium level ({recipe['sodium']}mg) exceeds your restriction."
            continue
            
        # Check 3: Diabetic friendly check
        if constraints.get("diabetic_friendly_only") and not recipe["is_diabetic_friendly"]:
            explanations[recipe["name"]] = "Excluded: Not suitable for diabetic meal plans."
            continue
            
        # Check 4: Goal verification via Backward Chaining
        meets_goal = backward_chaining_goal_check(recipe, target_goal)
        if not meets_goal:
            explanations[recipe["name"]] = f"Excluded: Does not satisfy your target goal ({target_goal})."
            continue
            
        # If it passes all rules, it's recommended!
        filtered_recipes.append(recipe)
        explanations[recipe["name"]] = f"Recommended: Safely passed all health rules and matched your goal ({target_goal})."
        
    return filtered_recipes, explanations