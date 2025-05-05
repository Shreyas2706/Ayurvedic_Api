from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Yoga & Meditation Data
yoga_asanas = {
    "Vata": [
        {
            "name": "Tree Pose",
            "duration": {"value": 5, "unit": "minutes"},
            "time": "Morning",
        },
        {
            "name": "Warrior Pose",
            "duration": {"value": 7, "unit": "minutes"},
            "time": "Morning",
        },
        {
            "name": "Downward Dog",
            "duration": {"value": 6, "unit": "minutes"},
            "time": "Evening",
        },
        {
            "name": "Seated Forward Bend",
            "duration": {"value": 8, "unit": "minutes"},
            "time": "Evening",
        }
    ],
    "Pitta": [
        {
            "name": "Child's Pose",
            "duration": {"value": 6, "unit": "minutes"},
            "time": "Evening",
        },
        {
            "name": "Triangle Pose",
            "duration": {"value": 7, "unit": "minutes"},
            "time": "Morning",
        },
        {
            "name": "Bridge Pose",
            "duration": {"value": 8, "unit": "minutes"},
            "time": "Evening",
        },
        {
            "name": "Camel Pose",
            "duration": {"value": 5, "unit": "minutes"},
            "time": "Morning",
        }
    ],
    "Kapha": [
        {
            "name": "Sun Salutation",
            "duration": {"value": 10, "unit": "minutes"},
            "time": "Morning",
           
        },
        {
            "name": "Bow Pose",
            "duration": {"value": 7, "unit": "minutes"},
            "time": "Afternoon",
        },
        {
            "name": "Cobra Pose",
            "duration": {"value": 6, "unit": "minutes"},
            "time": "Morning",
        },
        {
            "name": "Lotus Pose",
            "duration": {"value": 5, "unit": "minutes"},
            "time": "Evening",
        }
    ]
}

meditation_data = {
    "Vata": {
        "description": "Grounding meditation with body awareness.",
        "duration": {"value": 15, "unit": "minutes"}
    },
    "Pitta": {
        "description": "Cooling meditation with breathwork.",
        "duration": {"value": 12, "unit": "minutes"}
    },
    "Kapha": {
        "description": "Energizing meditation with movement.",
        "duration": {"value": 10, "unit": "minutes"}
    }
}

# Dosha insights and qualities
dosha_insights = {
    "Vata": "Vata types are creative, energetic, and quick thinkers but may experience anxiety, dryness, and irregular routines. Grounding routines, warm foods, and regular schedules help balance Vata.",
    "Pitta": "Pitta types are focused, intense, and intelligent, but may struggle with anger or overheating. Cooling foods, calm environments, and relaxation help balance Pitta.",
    "Kapha": "Kapha types are calm, compassionate, and strong but may feel lazy or gain weight easily. Stimulating routines, light foods, and energetic exercise balance Kapha."
}

dosha_qualities = {
    "Vata": ["Dry", "Cold", "Light", "Irregular", "Mobile", "Creative"],
    "Pitta": ["Hot", "Sharp", "Intense", "Ambitious", "Focused", "Fiery"],
    "Kapha": ["Heavy", "Stable", "Slow", "Cool", "Loyal", "Calm"]
}

# Diet section
diet_data = {
    "Vata": {
        "prefer": ["Warm soups", "Cooked vegetables", "Rice", "Ghee", "Oats"],
        "avoid": ["Raw foods", "Cold drinks", "Caffeine", "Dry snacks"],
        "insight": "Vata should prefer grounding, warm, and moist foods to counter dryness and cold.",
        "meals": {
            "breakfast": "Warm oatmeal with ghee and cinnamon",
            "lunch": "Steamed rice with cooked lentils and sautéed veggies",
            "dinner": "Vegetable soup with ghee toast"
        }
    },
    "Pitta": {
        "prefer": ["Coconut", "Cucumber", "Mint", "Sweet fruits", "Milk"],
        "avoid": ["Spicy food", "Alcohol", "Tomatoes", "Onion", "Garlic"],
        "insight": "Pitta benefits from cooling, calming foods to counter internal heat.",
        "meals": {
            "breakfast": "Coconut milk smoothie with banana",
            "lunch": "Mint rice with cucumber raita",
            "dinner": "Sweet potato mash with steamed broccoli"
        }
    },
    "Kapha": {
        "prefer": ["Light soups", "Barley", "Green veggies", "Spices", "Fruits"],
        "avoid": ["Heavy dairy", "Fried food", "Sugar", "Red meat"],
        "insight": "Kapha needs stimulating and light foods to maintain energy and avoid sluggishness.",
        "meals": {
            "breakfast": "Warm herbal tea with barley upma",
            "lunch": "Mixed vegetable stir fry with millet",
            "dinner": "Clear lentil soup with salad"
        }
    }
}

# Dosha detection logic
def detect_dosha(data):
    vata = pitta = kapha = 0
    hair = data.get('hair', '').lower()
    if "soft" in hair: vata += 1
    if "fine" in hair: vata += 1
    if "grey" in hair: pitta += 1

    digestive = data.get('digestivePattern', '').lower()
    if "fast" in digestive or "acid" in digestive: pitta += 1
    if "slow" in digestive: kapha += 1

    energy = data.get('energy', '').lower()
    if "drains fast" in energy: vata += 1
    if "steady" in energy: kapha += 1

    sleep = data.get('sleep', '').lower()
    if "long" in sleep: kapha += 1
    if "light" in sleep: vata += 1

    symptoms = data.get('symptoms', [])
    for symptom in symptoms:
        symptom = symptom.lower()
        if "headache" in symptom or "acid" in symptom: pitta += 1
        if "low energy" in symptom: kapha += 1
        if "anxiety" in symptom: vata += 1

    emotion = data.get('emotion', '').lower()
    if "lazy" in emotion or "calm" in emotion: kapha += 1
    if "overwhelmed" in emotion or "fear" in emotion: vata += 1

    exercise = data.get('exercise', '').lower()
    if "6" in exercise: pitta += 1
    if "less" in exercise: kapha += 1

    diet = data.get('diet', '').lower()
    if "fresh" in diet: kapha += 1
    if "light" in diet: vata += 1

    result = {"Vata": vata, "Pitta": pitta, "Kapha": kapha}
    dominant = max(result, key=result.get)
    return {"dosha": dominant, "score": result}


@app.route('/log_data', methods=['POST'])
def analyze_dosha():
    data = request.get_json()
    detected = detect_dosha(data)
    dosha = detected["dosha"]

    return jsonify({
        "dosha": dosha,
        "score": detected["score"],
        "qualities": dosha_qualities[dosha],
        "insight": dosha_insights[dosha],
        "yoga": yoga_asanas[dosha],
        "meditation": meditation_data[dosha],
        "diet": diet_data[dosha]
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
