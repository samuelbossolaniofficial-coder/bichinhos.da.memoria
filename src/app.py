from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory sample data
pets = [
    {"id": 1, "name": "Bichinho1", "memory": ["primeira lembrança"]},
    {"id": 2, "name": "Bichinho2", "memory": []}
]

@app.route('/')
def index():
    return jsonify({"message": "Bichinhos da Memória API", "status": "ok"})

@app.route('/pets', methods=['GET'])
def list_pets():
    return jsonify(pets)

@app.route('/pets/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    pet = next((p for p in pets if p["id"] == pet_id), None)
    if pet is None:
        return jsonify({"error":"Not found"}), 404
    return jsonify(pet)

@app.route('/pets/<int:pet_id>/memories', methods=['POST'])
def add_memory(pet_id):
    pet = next((p for p in pets if p["id"] == pet_id), None)
    if pet is None:
        return jsonify({"error":"Not found"}), 404
    data = request.get_json() or {}
    memory = data.get("memory")
    if not memory:
        return jsonify({"error":"memory is required"}), 400
    pet["memory"].append(memory)
    return jsonify(pet)

@app.route('/pets', methods=['POST'])
def create_pet():
    data = request.get_json() or {}
    new_id = max([p["id"] for p in pets]) + 1 if pets else 1
    pet = {"id": new_id, "name": data.get("name","unnamed"), "memory": data.get("memory",[])}
    pets.append(pet)
    return jsonify(pet), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
