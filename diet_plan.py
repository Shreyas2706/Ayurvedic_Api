from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/custom_diet_plan', methods=['POST'])
def generate_custom_diet_plan():
    data = request.get_json()
    dosha = data.get('dosha')
    goal = data.get('goal', None)
    duration = data.get('duration', None)
    diseases = data.get('diseases', [])

    # Weekly rotating diet plan based on dosha
    weekly_meals = {
        "Vata": {
            "breakfast": [
                "Warm oatmeal with ghee and dates",
                "Vegetable upma with ginger tea",
                "Banana pancakes with honey",
                "Ragi porridge with almonds",
                "Sweet potato hash with cinnamon",
                "Quinoa kheer with raisins",
                "Moong dal chilla with mint chutney"
            ],
            "lunch": [
                "Rice with lentil soup and sautéed spinach",
                "Khichdi with ghee and roasted veggies",
                "Chapati with paneer curry and beetroot",
                "Vegetable stew with millet",
                "Chickpea curry with jeera rice",
                "Stuffed paratha with yogurt",
                "Pumpkin curry with brown rice"
            ],
            "dinner": [
                "Moong dal soup with steamed veggies",
                "Lentil curry with rice and turmeric milk",
                "Palak paneer with chapati",
                "Methi thepla with carrot soup",
                "Bottle gourd curry with jeera rice",
                "Beetroot poriyal with khichdi",
                "Warm kitchari with coriander chutney"
            ],
            "insights": "Follow warm, moist, and grounding meals. Avoid dry, raw, and cold foods.",
            "food_to_avoid": ["Cold salads", "Dry snacks", "Frozen desserts"],
            "food_to_prefer": ["Soups", "Cooked vegetables", "Warming spices", "Oily food"]
        },
        "Pitta": {
            "breakfast": [
                "Coconut water and soaked almonds",
                "Rice flakes with cucumber and mint",
                "Fruit salad with melon",
                "Barley porridge with cardamom",
                "Avocado toast with coriander",
                "Chilled amaranth with rosewater",
                "Milkshake with figs and banana"
            ],
            "lunch": [
                "Rice with bottle gourd curry",
                "Chapati with pumpkin sabzi and cucumber raita",
                "Tofu stir-fry with rice",
                "Mung bean salad and mint chutney",
                "Coconut curry with chapati",
                "Cooling khichdi with coriander",
                "Vegetable pulao with coconut yogurt"
            ],
            "dinner": [
                "Zucchini soup with quinoa",
                "Beet salad and lentil patties",
                "Cool mung dal and rice",
                "Stuffed capsicum with mint chutney",
                "Bitter gourd stir-fry and rice",
                "Aloe vera sabzi with rotis",
                "Ash gourd stew with buttermilk"
            ],
            "insights": "Eat cooling, hydrating, and less spicy food. Avoid hot, oily, and fried items.",
            "food_to_avoid": ["Chili", "Fried food", "Tomatoes", "Fermented foods"],
            "food_to_prefer": ["Cool fruits", "Coconut", "Mint", "Cucumber", "Melons"]
        },
        "Kapha": {
            "breakfast": [
                "Ginger tea with roasted seeds",
                "Fruit salad with lemon",
                "Sprouted moong with pepper",
                "Millet porridge with dry fruits",
                "Upma with veggies",
                "Steamed idli with spicy chutney",
                "Herbal tea with oats chilla"
            ],
            "lunch": [
                "Barley khichdi with sautéed vegetables",
                "Mixed veg curry with millet roti",
                "Chickpea salad and lemon rice",
                "Steamed broccoli with dal",
                "Cabbage sabzi with roti",
                "Lauki kofta and rice",
                "Mixed sprouts curry with chapati"
            ],
            "dinner": [
                "Clear veggie soup with garlic",
                "Moong dal with spinach",
                "Mixed veg stew with roti",
                "Turai curry with millet",
                "Grilled tofu and sautéed kale",
                "Ajwain paratha with green chutney",
                "Herbal soup with quinoa"
            ],
            "insights": "Light, dry, and warm food is ideal. Avoid dairy, heavy and oily meals.",
            "food_to_avoid": ["Dairy", "Sugar", "Fried food", "Heavy grains"],
            "food_to_prefer": ["Barley", "Millet", "Spices", "Light soups", "Green leafy vegetables"]
        }
    }

    if not dosha or dosha not in weekly_meals:
        return jsonify({"error": "Unsupported or missing dosha type"}), 400

    # Extract the diet plan for the specified dosha
    diet_plan = weekly_meals[dosha]

    # Recommendations based on goal, duration, and diseases
    recommendations = []

    # Based on goal
    if goal:
        if "weight loss" in goal.lower():
            recommendations.append("Focus on lighter dinners and avoid sugar-rich foods.")
        elif "muscle gain" in goal.lower():
            recommendations.append("Include more protein-rich legumes and paneer.")
        elif "detox" in goal.lower():
            recommendations.append("Drink warm water with lemon every morning and eat steamed vegetables.")

    # Based on duration
    if duration:
        try:
            weeks = int(duration.split()[0])  # e.g., "4 weeks"
            if weeks < 2:
                recommendations.append("For noticeable results, follow the plan for at least 2 weeks.")
            elif weeks >= 4:
                recommendations.append("You're on track for long-term benefits. Stay consistent!")
        except:
            recommendations.append("Duration format not recognized. Make sure to mention in 'x weeks' format.")

    # Based on diseases
    if diseases:
        if any("diabetes" in d.lower() for d in diseases):
            recommendations.append("Avoid sugary fruits and include bitter gourd and fenugreek in meals.")
        if any("hypertension" in d.lower() or "bp" in d.lower() for d in diseases):
            recommendations.append("Reduce salt and processed foods; prefer steamed and boiled dishes.")
        if any("thyroid" in d.lower() for d in diseases):
            recommendations.append("Limit goitrogens like cabbage and cauliflower; include more iodine-rich foods.")

    return jsonify({
        "dosha": dosha,
        "goal": goal,
        "duration": duration,
        "diseases": diseases,
        "diet_plan": diet_plan,
        "recommendations": recommendations
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)