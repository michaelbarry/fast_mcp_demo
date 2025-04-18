from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

# In-memory database for pets
pets = [
    {"id": "1", "name": "Fluffy", "type": "cat", "age": 3},
    {"id": "2", "name": "Rex", "type": "dog", "age": 5},
    {"id": "3", "name": "Bubbles", "type": "fish", "age": 1}
]

@app.route('/pets', methods=['GET'])
def list_pets():
    """List all pets"""
    return jsonify(pets)

@app.route('/pets', methods=['POST'])
def create_pet():
    """Create a new pet"""
    new_pet = request.json
    
    # Validate required fields
    if 'name' not in new_pet or 'type' not in new_pet:
        return jsonify({"error": "Name and type are required fields"}), 400
    
    # Generate a simple ID
    if not new_pet.get('id'):
        max_id = max([int(pet['id']) for pet in pets]) if pets else 0
        new_pet['id'] = str(max_id + 1)
    
    # Ensure age is an integer if provided
    if 'age' in new_pet and not isinstance(new_pet['age'], int):
        try:
            new_pet['age'] = int(new_pet['age'])
        except (ValueError, TypeError):
            return jsonify({"error": "Age must be an integer"}), 400
    
    pets.append(new_pet)
    
    # Return 201 Created status code
    response = make_response(jsonify(new_pet))
    response.status_code = 201
    return response

@app.route('/pets/<petId>', methods=['GET'])
def get_pet(petId):
    """Get a pet by ID"""
    for pet in pets:
        if pet['id'] == petId:
            return jsonify(pet)
    
    return jsonify({"error": "Pet not found"}), 404

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed"}), 405

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("Pet Store API Server")
    print("Running on http://localhost:5000")
    print("Endpoints:")
    print("  GET  /pets - List all pets")
    print("  POST /pets - Create a new pet")
    print("  GET  /pets/{petId} - Get a pet by ID")
    print("\nAvailable test pets:", pets)
    app.run(debug=True)