import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({
        "status": "success",
        "message": "SSL Pinning is working!",
        "data": {
            "timestamp": "2024-01-01",
            "server": "Python Flask"
        }
    })

@app.route('/api/login', methods=['POST'])
def login():
    """Login endpoint that accepts username and password"""
    # Get JSON data from request
    data = request.get_json()

    # Validate request data
    if not data:
        return jsonify({
            "status": "error",
            "message": "No data provided"
        }), 400

    username = data.get('username')
    password = data.get('password')

    # Validate credentials
    if not username or not password:
        return jsonify({
            "status": "error",
            "message": "Username and password are required"
        }), 400

    # Mock user database (for testing purposes)
    users = {
        "admin": {
            "password": "admin123",
            "data": {
                "id": 1,
                "username": "admin",
                "name": "Admin User",
                "email": "admin@example.com",
                "age": 30,
                "userType": "administrator",
                "role": "admin",
                "department": "IT",
                "joinDate": "2020-01-15",
                "isActive": True
            }
        },
        "john": {
            "password": "john123",
            "data": {
                "id": 2,
                "username": "john",
                "name": "John Doe",
                "email": "john.doe@example.com",
                "age": 28,
                "userType": "regular",
                "role": "developer",
                "department": "Engineering",
                "joinDate": "2021-03-20",
                "isActive": True
            }
        },
        "sarah": {
            "password": "sarah123",
            "data": {
                "id": 3,
                "username": "sarah",
                "name": "Sarah Smith",
                "email": "sarah.smith@example.com",
                "age": 32,
                "userType": "premium",
                "role": "manager",
                "department": "Product",
                "joinDate": "2019-07-10",
                "isActive": True
            }
        },
        "demo": {
            "password": "demo123",
            "data": {
                "id": 4,
                "username": "demo",
                "name": "Demo User",
                "email": "demo@example.com",
                "age": 25,
                "userType": "trial",
                "role": "viewer",
                "department": "Sales",
                "joinDate": "2024-01-01",
                "isActive": True
            }
        }
    }

    # Check credentials
    if username in users and users[username]["password"] == password:
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "token": f"mock_token_{username}_12345",  # Mock JWT token
            "user": users[username]["data"]
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Invalid username or password"
        }), 401

@app.route('/api/user', methods=['GET'])
def get_user():
    return jsonify({
        "id": 1,
        "name": "Test User",
        "email": "test@example.com"
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "healthy",
        "service": "ssl-pinning-test"
    })

if __name__ == '__main__':
    # Get port from environment variable (Railway sets this)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
