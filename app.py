import streamlit as st
from utils.recommender import get_recommendations

# Embedded Recipe Knowledge Base (No external file needed!)
recipes = [
    {
        "id": 1,
        "name": "Grilled Chicken Salad",
        "category": "Dinner",
        "diet_type": "Non-Vegetarian",
        "allergens": [],
        "ingredients": ["chicken breast", "lettuce", "olive oil", "lemon"],
        "calories": 350,
        "protein": 35,
        "sodium": 200,
        "is_diabetic_friendly": True
    },
    {
        "id": 2,
        "name": "Peanut Butter Oatmeal",
        "category": "Breakfast",
        "diet_type": "Vegan",
        "allergens": ["peanuts", "nuts"],
        "ingredients": ["oats", "peanut butter", "almond milk", "banana"],
        "calories": 400,
        "protein": 15,
        "sodium": 100,
        "is_diabetic_friendly": False
    },
    {
        "id": 3,
        "name": "Quinoa Veggie Bowl",
        "category": "Lunch",
        "diet_type": "Vegan",
        "allergens": [],
        "ingredients": ["quinoa", "spinach", "tomatoes", "olive oil"],
        "calories": 300,
        "protein": 10,
        "sodium": 150,
        "is_diabetic_friendly": True
    }
]

st.title("🥗 AI-Powered Dietary & Recipe Expert System")
st.markdown("A rule-based recommendation system utilizing **forward and backward chaining** to deliver safe, personalized meals.")

# Sidebar User Profile Inputs
st.sidebar.header("User Health Profile")
user_name = st.sidebar.text_input("Your Name", "Master. Khairnar Kaushal")

# Allergies input
selected_allergies = st.sidebar.multiselect(
    "Select Known Allergens",
    ["peanuts", "nuts", "dairy", "shellfish", "gluten"]
)

# Health conditions
has_hypertension = st.sidebar.checkbox("Diagnosed with Hypertension (High BP)")
has_diabetes = st.sidebar.checkbox("Diagnosed with Diabetes")

# Fitness/Dietary Goal (Backward chaining target)
target_goal = st.sidebar.selectbox(
    "Select Nutritional Goal",
    ["None", "High Protein", "Low Calorie"]
)

# Build profile dictionary
user_profile = {
    "name": user_name,
    "allergies": selected_allergies,
    "has_hypertension": has_hypertension,
    "has_diabetes": has_diabetes
}

# Recommendation Button
if st.button("Generate Recommendations & Run Inference"):
    recommended, explanations = get_recommendations(user_profile, target_goal, recipes)
    
    st.subheader(f"Recommendations for {user_name}")
    
    if recommended:
        for rec in recommended:
            with st.expander(f"✨ {rec['name']} ({rec['category']})"):
                st.write(f"**Calories:** {rec['calories']} kcal | **Protein:** {rec['protein']}g | **Sodium:** {rec['sodium']}mg")
                st.write(f"**Ingredients:** {', '.join(rec['ingredients'])}")
    else:
        st.warning("No recipes matched your strict profile constraints.")
        
    st.markdown("---")
    st.subheader("🔍 Expert System Explanation Log (Inference Trace)")
    for recipe_name, explanation in explanations.items():
        if "Recommended" in explanation:
            st.success(f"**{recipe_name}**: {explanation}")
        else:
            st.error(f"**{recipe_name}**: {explanation}")