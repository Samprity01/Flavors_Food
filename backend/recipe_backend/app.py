from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Recipe Recommendation System
def fetch_recipes(ingredients):
    base_url = "https://www.themealdb.com/api/json/v1/1/filter.php"
    recipes = []
    for ingredient in ingredients:
        params = {"i": ingredient}
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json().get("meals", [])
            if data:
                recipes.extend(data)
        else:
            print(f"Error fetching recipes for {ingredient}: {response.status_code}")
    return recipes

def filter_recipes_by_diet(recipes, diet_restrictions):
    if not diet_restrictions:
        return recipes  # No restrictions, return all recipes

    filtered_recipes = []
    for recipe in recipes:
        recipe_details = fetch_recipe_details(recipe["idMeal"])
        if not recipe_details:
            continue

        # Gather all ingredients for the recipe
        ingredients = [
            recipe_details.get(f"strIngredient{i}") for i in range(1, 21)
            if recipe_details.get(f"strIngredient{i}")
        ]

        # Check if any restricted ingredient is present
        if not any(restriction in ingredients for restriction in diet_restrictions):
            filtered_recipes.append(recipe)

    return filtered_recipes

def fetch_recipe_details(recipe_id):
    base_url = "https://www.themealdb.com/api/json/v1/1/lookup.php"
    params = {"i": recipe_id}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json().get("meals", [])[0]
    else:
        return None

@app.route('/api/getRecipes', methods=['POST'])
def get_recipes_endpoint():
    data = request.json
    ingredients = data.get('ingredients')
    restrictions = data.get('restrictions', [])
    
    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400
    
    recipes = fetch_recipes(ingredients)
    filtered_recipes = filter_recipes_by_diet(recipes, restrictions)
    
    return jsonify(filtered_recipes)

# Nutritional Analysis System
dynamic_nutritional_data = {
    'rice': {'calories': 130, 'protein': 2.7, 'fat': 0.3, 'carbs': 28.2},
    'chicken': {'calories': 239, 'protein': 27.3, 'fat': 13.6, 'carbs': 0},
    'spices': {'calories': 100, 'protein': 3.5, 'fat': 5.0, 'carbs': 20.0},
    'yogurt': {'calories': 59, 'protein': 10, 'fat': 0.4, 'carbs': 3.6},
    'cucumber': {'calories': 16, 'protein': 0.7, 'fat': 0.1, 'carbs': 3.6},
    'paneer': {'calories': 265, 'protein': 18.6, 'fat': 20.0, 'carbs': 1.2},
    'bell pepper': {'calories': 20, 'protein': 0.9, 'fat': 0.2, 'carbs': 4.7},
    'flour': {'calories': 364, 'protein': 10.3, 'fat': 1.0, 'carbs': 76.3},
    'potatoes': {'calories': 77, 'protein': 2.0, 'fat': 0.1, 'carbs': 17.6},
    'milk': {'calories': 42, 'protein': 3.4, 'fat': 1.0, 'carbs': 5.0},
    'sugar': {'calories': 387, 'protein': 0, 'fat': 0, 'carbs': 100}
}

@app.route('/api/analyzeNutrition', methods=['POST'])
def analyze_nutrition_endpoint():
    data = request.json
    recipe_name = data.get('recipe_name')
    ingredients = data.get('ingredients')

    total_nutrition = {
        'recipe_name': recipe_name,
        'calories': sum(dynamic_nutritional_data[ingredient]['calories'] for ingredient in ingredients if ingredient in dynamic_nutritional_data),
        'protein (g)': sum(dynamic_nutritional_data[ingredient]['protein'] for ingredient in ingredients if ingredient in dynamic_nutritional_data),
        'fat (g)': sum(dynamic_nutritional_data[ingredient]['fat'] for ingredient in ingredients if ingredient in dynamic_nutritional_data),
        'carbs (g)': sum(dynamic_nutritional_data[ingredient]['carbs'] for ingredient in ingredients if ingredient in dynamic_nutritional_data),
    }

    return jsonify(total_nutrition)

if __name__ == '__main__':
   app.run(debug=True)
