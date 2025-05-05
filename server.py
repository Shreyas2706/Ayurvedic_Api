from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample data for yoga asanas and meditation for different dosha types
yoga_data = {
    "Vata": {
        "asanas": ["Tree Pose", "Warrior Pose", "Downward Dog", "Seated Forward Bend"],
        "meditation": "Guided breathing meditation focusing on grounding and stability."
    },
    "Pitta": {
        "asanas": ["Child's Pose", "Triangle Pose", "Bridge Pose", "Camel Pose"],
        "meditation": "Cool, calming meditation with focus on breath awareness."
    },
    "Kapha": {
        "asanas": ["Sun Salutation", "Bow Pose", "Cobra Pose", "Lotus Pose"],
        "meditation": "Energizing meditation to stimulate the body and mind."
    },
    "Tridosha": {
        "asanas": ["Mountain Pose", "Chair Pose", "Cat-Cow Pose", "Savasana"],
        "meditation": "Balanced meditation that helps in harmonizing the energies."
    }
}

@app.route('/get_yoga', methods=['POST'])
def get_yoga():
    # Get the dosha type from the request body
    data = request.get_json()
    print(data)
    # Check if the dosha key is in the provided data
    dosha = data.get('dosha', '').capitalize()
    
    if dosha in yoga_data:
        return jsonify(yoga_data[dosha])
    else:
        return jsonify({"error": "Invalid dosha type. Please enter one of the following: Vata, Pitta, Kapha, Tridosha"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


    

