
import os
from datetime import datetime, timedelta, timezone, date

import jwt
import mysql.connector

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.security import check_password_hash


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(
    dotenv_path=os.path.join(BASE_DIR, ".env")
)

app = Flask(__name__)


# --------------------------------------------------
# CORS CONFIGURATION
# --------------------------------------------------

frontend_origin = os.getenv("FRONTEND_ORIGIN", "").strip()

allowed_origins = [
    r"http://localhost:\d+",
    r"http://127\.0\.0\.1:\d+"
]

if frontend_origin:
    allowed_origins.append(frontend_origin)

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": [
                "Content-Type",
                "Authorization"
            ]
        }
    }
)


# --------------------------------------------------
# MYSQL DATABASE CONNECTION
# --------------------------------------------------

def get_db_connection():

    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "nobroker_sales"),
        port=int(os.getenv("DB_PORT", "3306")),
        connection_timeout=10
    )


# --------------------------------------------------
# HOME API
# --------------------------------------------------

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "NoBroker Sales Dashboard API is running",
        "status": "success"
    }), 200


# --------------------------------------------------
# DATABASE CONNECTION TEST
# --------------------------------------------------

@app.route("/api/test-db", methods=["GET"])
def test_db():

    connection = None

    try:

        connection = get_db_connection()

        return jsonify({
            "status": "success",
            "message": "MySQL connected successfully"
        }), 200

    except Exception:

        app.logger.exception("Database connection failed")

        return jsonify({
            "status": "error",
            "message": "MySQL connection failed"
        }), 500

    finally:

        if connection and connection.is_connected():
            connection.close()


# --------------------------------------------------
# DASHBOARD API
# --------------------------------------------------

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

    }), 200


# --------------------------------------------------
# LOGIN API
# --------------------------------------------------

@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json(silent=True) or {}

    email = data.get("email", "")
    password = data.get("password", "")

    if not isinstance(email, str) or not isinstance(password, str):
        return jsonify({
            "status": "error",
            "message": "Invalid login input"
        }), 400

    email = email.strip().lower()

    if not email or not password:

        return jsonify({
            "status": "error",
            "message": "Email and password are required"
        }), 400

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

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

        if not user or not user["is_active"]:

            return jsonify({
                "status": "error",
                "message": "Invalid email or password"
            }), 401

        if not check_password_hash(
            user["password_hash"],
            password
        ):

            return jsonify({
                "status": "error",
                "message": "Invalid email or password"
            }), 401

        secret = os.getenv("SECRET_KEY")

        if not secret:

            app.logger.error("SECRET_KEY is missing")

            return jsonify({
                "status": "error",
                "message": "Server authentication configuration is missing"
            }), 500

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


# --------------------------------------------------
# GOOGLE SHEET SYNC API
# --------------------------------------------------

@app.route("/api/sheets/sync", methods=["POST"])
def sync_google_sheet():

    # Verify dedicated sync token
    expected_token = os.getenv("SHEET_SYNC_TOKEN")
    received_token = request.headers.get("X-Sheet-Token", "")

    if not expected_token:
        app.logger.error("SHEET_SYNC_TOKEN is missing")

        return jsonify({
            "status": "error",
            "message": "Sync configuration missing"
        }), 500

    if not received_token or received_token != expected_token:

        return jsonify({
            "status": "error",
            "message": "Unauthorized"
        }), 401

    data = request.get_json(silent=True) or {}
    rows = data.get("rows")

    if not isinstance(rows, list):

        return jsonify({
            "status": "error",
            "message": "Rows must be a list"
        }), 400

    if len(rows) > 500:

        return jsonify({
            "status": "error",
            "message": "Maximum 500 rows per request"
        }), 400

    connection = None
    cursor = None

    try:

        connection = get_db_connection()
        cursor = connection.cursor()

        synced_count = 0
        skipped_count = 0

        for item in rows:

            if not isinstance(item, dict):
                skipped_count += 1
                continue

            lead_id = str(
                item.get("lead_id") or ""
            ).strip()

            rm_email = str(
                item.get("rm_email") or ""
            ).strip().lower()

            tl_name = str(
                item.get("tl_name") or ""
            ).strip()

            visit_status = str(
                item.get("visit_status") or ""
            ).strip()

            try:
                visit_count = int(
                    item.get("visit_count") or 1
                )
            except (ValueError, TypeError):
                skipped_count += 1
                continue

            visit_date = item.get("visit_date") or None

            if not lead_id or not rm_email or visit_count < 1:
                skipped_count += 1
                continue

            # Accept ISO date: YYYY-MM-DD
            if visit_date:
                try:
                    if isinstance(visit_date, str):
                        visit_date = date.fromisoformat(
                            visit_date[:10]
                        )
                except ValueError:
                    skipped_count += 1
                    continue

            cursor.execute(
                """
                INSERT INTO schedules
                    (
                        tl_name,
                        rm_email,
                        lead_id,
                        visit_date,
                        visit_count,
                        visit_status
                    )
                VALUES (%s, %s, %s, %s, %s, %s)

                ON DUPLICATE KEY UPDATE
                    tl_name = VALUES(tl_name),
                    visit_date = VALUES(visit_date),
                    visit_status = VALUES(visit_status)
                """,
                (
                    tl_name,
                    rm_email,
                    lead_id,
                    visit_date,
                    visit_count,
                    visit_status
                )
            )

            synced_count += 1

        connection.commit()

        return jsonify({
            "status": "success",
            "message": "Google Sheet data synced successfully",
            "synced_rows": synced_count,
            "skipped_rows": skipped_count
        }), 200

    except Exception:

        if connection:
            connection.rollback()

        app.logger.exception("Google Sheet sync failed")

        return jsonify({
            "status": "error",
            "message": "Unable to sync Google Sheet data"
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# --------------------------------------------------
# HEALTH CHECK API
# --------------------------------------------------

@app.route("/api/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy",
        "service": "NoBroker Sales Dashboard API"
    }), 200


# --------------------------------------------------
# PRODUCTION SERVER
# --------------------------------------------------

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5001))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
