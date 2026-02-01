#!/usr/bin/env python3
"""
Shuffle Data Provider - Mock Test User API for Cerberus Testing

This script provides randomized test user data for Cerberus test automation.
It can run as a Flask API server OR output JSON data for file-based integration.

Usage:
    API Mode:     python3 shuffle_provider.py --api --port 5000
    JSON Output:  python3 shuffle_provider.py --json > shuffle_data.json
    Single User:  python3 shuffle_provider.py --single

Cerberus Integration:
    - API: Use callUrl action with http://localhost:5000/shuffle/get_user
    - File: Read shuffle_data.json in test initialization step
"""

import json
import random
import argparse
from typing import Dict, List
from datetime import datetime

# Test user pool (Firebase-safe phone numbers for testing)
TEST_USERS = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice.johnson@testmail.com",
        "phone": "5555551001",
        "countryCode": "+1",
        "password": "TestPass123!",
        "otp": "123456"  # Firebase test OTP
    },
    {
        "id": 2,
        "name": "Bob Smith",
        "email": "bob.smith@testmail.com",
        "phone": "5555551002",
        "countryCode": "+1",
        "password": "TestPass456!",
        "otp": "123456"
    },
    {
        "id": 3,
        "name": "Carol Davis",
        "email": "carol.davis@testmail.com",
        "phone": "5555551003",
        "countryCode": "+1",
        "password": "TestPass789!",
        "otp": "123456"
    },
    {
        "id": 4,
        "name": "David Wilson",
        "email": "david.wilson@testmail.com",
        "phone": "5555551004",
        "countryCode": "+1",
        "password": "TestPass321!",
        "otp": "123456"
    },
    {
        "id": 5,
        "name": "Eve Martinez",
        "email": "eve.martinez@testmail.com",
        "phone": "5555551005",
        "countryCode": "+1",
        "password": "TestPass654!",
        "otp": "123456"
    }
]


def get_random_user() -> Dict:
    """Get a random test user from the pool."""
    user = random.choice(TEST_USERS)
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "phone": user["phone"],
        "countryCode": user["countryCode"],
        "fullPhone": f"{user['countryCode']}{user['phone']}",
        "password": user["password"],
        "otp": user["otp"],
        "timestamp": datetime.now().isoformat(),
        "source": "shuffle_provider"
    }


def get_all_users() -> List[Dict]:
    """Get all test users with metadata."""
    return {
        "users": TEST_USERS,
        "count": len(TEST_USERS),
        "generated_at": datetime.now().isoformat(),
        "notes": [
            "These are Firebase-safe test phone numbers",
            "Configure these in Firebase Console → Phone numbers for testing",
            "OTP is fixed at 123456 for all test numbers"
        ]
    }


def run_api_server(port: int = 5000):
    """Run Flask API server for Cerberus integration."""
    try:
        from flask import Flask, jsonify
        from flask_cors import CORS
    except ImportError:
        print("❌ Flask not installed. Install with: pip3 install flask flask-cors")
        exit(1)

    app = Flask(__name__)
    CORS(app)

    @app.route('/shuffle/get_user', methods=['GET'])
    def get_user():
        """Get a random test user."""
        user = get_random_user()
        return jsonify(user)

    @app.route('/shuffle/get_all', methods=['GET'])
    def get_all():
        """Get all test users."""
        return jsonify(get_all_users())

    @app.route('/shuffle/health', methods=['GET'])
    def health():
        """Health check endpoint."""
        return jsonify({
            "status": "healthy",
            "service": "shuffle_provider",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat()
        })

    print(f"""
    ╔═══════════════════════════════════════════════════════════════╗
    ║  🎲 Shuffle Test Data Provider - API Server Running          ║
    ╚═══════════════════════════════════════════════════════════════╝

    API Endpoints:
      📍 Get Random User:    http://localhost:{port}/shuffle/get_user
      📍 Get All Users:      http://localhost:{port}/shuffle/get_all
      📍 Health Check:       http://localhost:{port}/shuffle/health

    Cerberus Integration:
      ✅ Use 'callUrl' action with: http://localhost:{port}/shuffle/get_user
      ✅ Store response fields: phone, countryCode, fullPhone, otp, password

    Press Ctrl+C to stop the server.
    """)

    app.run(host='0.0.0.0', port=port, debug=False)


def main():
    parser = argparse.ArgumentParser(description='Shuffle Test Data Provider')
    parser.add_argument('--api', action='store_true', help='Run as Flask API server')
    parser.add_argument('--json', action='store_true', help='Output JSON data')
    parser.add_argument('--single', action='store_true', help='Output single random user')
    parser.add_argument('--port', type=int, default=5000, help='API server port (default: 5000)')

    args = parser.parse_args()

    if args.api:
        run_api_server(args.port)
    elif args.json:
        print(json.dumps(get_all_users(), indent=2))
    elif args.single:
        print(json.dumps(get_random_user(), indent=2))
    else:
        # Default: show help
        parser.print_help()
        print("\n📋 Example Usage:")
        print("  python3 shuffle_provider.py --api           # Start API server")
        print("  python3 shuffle_provider.py --json          # Generate JSON file")
        print("  python3 shuffle_provider.py --single        # Get one random user")


if __name__ == '__main__':
    main()
