from flask import Flask, request, jsonify # type: ignore

app = Flask(__name__)

# In-memory user storage
users = {}

# Home route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the User Management API!"})

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# GET a single user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(str(user_id))
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# POST - Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not data.get("name") or not data.get("email"):
        return jsonify({"error": "Name and email are required"}), 400

    user_id = len(users) + 1
    users[str(user_id)] = {
        "id": user_id,
        "name": data.get("name"),
        "email": data.get("email")
    }
    return jsonify(users[str(user_id)]), 201

# PUT - Update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user_key = str(user_id)
    if user_key not in users:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    users[user_key]["name"] = data.get("name", users[user_key]["name"])
    users[user_key]["email"] = data.get("email", users[user_key]["email"])
    return jsonify(users[user_key])

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_key = str(user_id)
    if user_key not in users:
        return jsonify({"error": "User not found"}), 404

    deleted_user = users.pop(user_key)
    return jsonify({"message": "User deleted", "user": deleted_user})
    return jsonify({"message": "User deleted", "user": deleted_user})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)