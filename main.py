import os
from flask import Flask, jsonify
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
