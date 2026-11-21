
import os
from datetime import datetime, timedelta, timezone

import jwt
import mysql.connector

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.security import check_password_hash


# Load environment variables
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))


app = Flask(__name__)


# CORS configuration
# Allows Angular localhost development ports
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                r"http://localhost:\d+",
                r"http://127\.0\.0\.1:\d+"
            ],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": [
                "Content-Type",
                "Authorization"
            ]
        }
    }
)


# MySQL database connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "nobroker_sales"),
        port=int(os.getenv("DB_PORT", "3306"))
    )


# Home API
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "NoBroker Sales Dashboard API is running",
        "status": "success"
    })


# Database connection test
@app.route("/api/test-db", methods=["GET"])
def test_db():

    connection = None

    try:
        connection = get_db_connection()

        return jsonify({
            "status": "success",
            "message": "MySQL connected"
        })

    except Exception:
        app.logger.exception("Database connection failed")

        return jsonify({
            "status": "error",
            "message": "MySQL connection failed"
        }), 500

    finally:
        if connection and connection.is_connected():
            connection.close()


# Dashboard API
@app.route("/api/dashboard", methods=["GET"])
def dashboard():

    return jsonify({
        "company": "NoBroker",
        "team_lead": "Arun M",
        "teams": [
            {
                "name": "Seller Team",
                "region": "Chennai"
            },
            {
                "name": "Non-Super Team",
                "region": "Chennai"
            },
            {
                "name": "Postpaid Team",
                "region": "Bangalore and Chennai"
            }
        ]
    })


# Login API
@app.route("/api/login", methods=["POST", "OPTIONS"])
def login():

    # Handle browser preflight request
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    # Validate input
    if not email or not password:
        return jsonify({
            "status": "error",
            "message": "Email and password are required"
        }), 400

    connection = None
    cursor = None

    try:

        # Connect to MySQL
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Find user
        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                password_hash,
                role,
                team,
                region,
                is_active
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        user = cursor.fetchone()

        # Check user exists and active
        if not user or not user["is_active"]:
            return jsonify({
                "status": "error",
                "message": "Invalid email or password"
            }), 401

        # Verify password
        if not check_password_hash(
            user["password_hash"],
            password
        ):
            return jsonify({
                "status": "error",
                "message": "Invalid email or password"
            }), 401

        # JWT secret
        secret = os.getenv("SECRET_KEY")

        if not secret:
            app.logger.error("SECRET_KEY is missing")

            return jsonify({
                "status": "error",
                "message": "Server authentication configuration is missing"
            }), 500

        # Generate JWT token
        token = jwt.encode(
            {
                "user_id": user["id"],
                "role": user["role"],
                "exp": datetime.now(timezone.utc)
                + timedelta(hours=8)
            },
            secret,
            algorithm="HS256"
        )

        # Successful login
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "token": token,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"],
                "team": user["team"],
                "region": user["region"]
            }
        }), 200

    except Exception:

        app.logger.exception("Login API error")

        return jsonify({
            "status": "error",
            "message": "Unable to process login"
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# Start Flask server
if __name__ == "__main__":

 app.run(
    host="127.0.0.1",
    port=5001,
    debug=True
)
