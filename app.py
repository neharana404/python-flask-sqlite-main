from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Connect to SQLite Database (or any other database)
def init_db():
    conn = sqlite3.connect('users.db')
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
    id_token = data.get('idToken')
    phone_number = data.get('phone')
    profile_data = data.get('profileData', {})

    try:
        # Connect to the database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        # Check if idToken already exists
        c.execute("SELECT * FROM users WHERE uid = ?", (id_token,))
        user = c.fetchone()

        if user:
            # Update existing user details
            c.execute("""
                UPDATE users 
                SET phone = ?, 
                    name = COALESCE(?, name), 
                    email = COALESCE(?, email), 
                    age = COALESCE(?, age), 
                    photo = COALESCE(?, photo), 
                    dentalQuestions = COALESCE(?, dentalQuestions)
                WHERE uid = ?
            """, (
                phone_number,
                profile_data.get('name'),
                profile_data.get('email'),
                profile_data.get('age'),
                profile_data.get('photo'),
                str(profile_data.get('dentalQuestions')),
                id_token
            ))
            message = "User details updated successfully"
        else:
            c.execute("""
                INSERT INTO users (uid, phone, name, email, age, photo, dentalQuestions) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                id_token,
                phone_number,
                profile_data.get('name'),
                profile_data.get('email'),
                profile_data.get('age'),
                profile_data.get('photo'),
                str(profile_data.get('dentalQuestions'))
            ))
            message = "User added successfully with placeholders for profile data"

        # Commit changes and close connection
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
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute("SELECT uid, phone, name, email, age, photo, dentalQuestions FROM users WHERE uid = ?", (id_token,))
        user = c.fetchone()
        conn.close()

        if user:
            user_details = {
                "phone": user[1],
                "name": user[2],
                "email": user[3],
                "age": user[4],
                "photo": user[5],
                "dentalQuestions": user[6]
            }

            conn.close()
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
