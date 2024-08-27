from flask import Flask, request, jsonify
import os
import sqlite3
import psycopg2  # Add this if you are using PostgreSQL
from psycopg2.extras import RealDictCursor
import json

app = Flask(__name__)

# Choose the database configuration based on the environment
def get_db_connection():
    if os.getenv('FLASK_ENV') == 'production':
        print("Connecting to PostgreSQL database...")
        DATABASE_URL = os.getenv('DATABASE_URL')
        conn = psycopg2.connect(DATABASE_URL, sslmode='require', cursor_factory=RealDictCursor)
    else:
        print("Connecting to SQLite database...")
        conn = sqlite3.connect('users.db')
        conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

# Initialize SQLite Database (for local development)
def init_db():
    if os.getenv('FLASK_ENV') != 'production':  # Only initialize SQLite in non-production environments
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (uid TEXT PRIMARY KEY, 
                      phone TEXT,
                      name TEXT,
                      email TEXT,
                      age INTEGER,
                      photo TEXT,
                      dentalQuestions TEXT)''')
        conn.commit()
        conn.close()

init_db()

@app.route('/add-user', methods=['POST'])
def add_user():
    data = request.get_json()
    print(f"Received data: {data}")
    id_token = data.get('idToken')
    phone_number = data.get('phone')
    profile_data = data.get('profileData', {})

    # Default structure for dentalQuestions
    default_dental_questions = {
        "question1": False,
        "question2": "",
        "question3": False
    }

    # Use provided dentalQuestions from profile_data or fallback to default
    dental_questions = profile_data.get('dentalQuestions', default_dental_questions)


    try:
        conn = get_db_connection()
        c = conn.cursor()

        # Determine the parameter placeholder syntax based on the environment
        if os.getenv('FLASK_ENV') == 'production':
            # PostgreSQL syntax
            select_query = "SELECT * FROM users WHERE uid = %s"
            update_query = """
                UPDATE users 
                SET phone = %s, 
                    name = COALESCE(%s, name), 
                    email = COALESCE(%s, email), 
                    age = COALESCE(%s, age), 
                    photo = COALESCE(%s, photo), 
                    "dentalQuestions" = COALESCE(%s, "dentalQuestions")
                WHERE uid = %s
            """
            insert_query = """
                INSERT INTO users (uid, phone, name, email, age, photo, "dentalQuestions") 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        else:
            # SQLite syntax
            select_query = "SELECT * FROM users WHERE uid = ?"
            update_query = """
                UPDATE users 
                SET phone = ?, 
                    name = COALESCE(?, name), 
                    email = COALESCE(?, email), 
                    age = COALESCE(?, age), 
                    photo = COALESCE(?, photo), 
                    dentalQuestions = COALESCE(?, dentalQuestions)
                WHERE uid = ?
            """
            insert_query = """
                INSERT INTO users (uid, phone, name, email, age, photo, dentalQuestions) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """

        # Check if idToken already exists
        c.execute(select_query, (id_token,))
        user = c.fetchone()

        if user:
            # Update existing user details
            c.execute(update_query, (
                phone_number,
                profile_data.get('name'),
                profile_data.get('email'),
                profile_data.get('age'),
                profile_data.get('photo'),
                json.dumps(dental_questions),
                id_token
            ))
            message = "User details updated successfully"
        else:
            # Insert new user details
            c.execute(insert_query, (
                id_token,
                phone_number,
                profile_data.get('name'),
                profile_data.get('email'),
                profile_data.get('age'),
                profile_data.get('photo'),
                json.dumps(dental_questions)
            ))
            message = "User added successfully with placeholders for profile data"

        conn.commit()
        conn.close()

        return jsonify({"message": message}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/get-user', methods=['GET'])
def get_user():
    id_token = request.args.get('idToken')

    if not id_token:
        return jsonify({"error": "idToken is required"}), 400

    try:
        conn = get_db_connection()
        c = conn.cursor()

        # Determine the parameter placeholder syntax based on the environment
        if os.getenv('FLASK_ENV') == 'production':
            # PostgreSQL syntax
            select_query = 'SELECT uid, phone, name, email, age, photo, "dentalQuestions" FROM users WHERE uid = %s'
        else:
            # SQLite syntax
            select_query = "SELECT uid, phone, name, email, age, photo, dentalQuestions FROM users WHERE uid = ?"

        # Execute the query
        c.execute(select_query, (id_token,))
        user = c.fetchone()
        conn.close()

        if user:
            user_details = {
                "phone": user['phone'],
                "name": user['name'],
                "email": user['email'],
                "age": user['age'],
                "photo": user['photo'],
                "dentalQuestions": user['dentalQuestions']
            }
            return jsonify(user_details), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
