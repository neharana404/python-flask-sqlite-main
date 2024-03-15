# Author: Neha Rana, University of Rochester
# Date: 03/13/2024
# Description: This is a Flask App that uses SQLite3 to
# execute (C)reate, (R)ead, (U)pdate, (D)elete operations

from flask import Flask, jsonify
from flask import render_template
from flask import request
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Route to add a new record (INSERT) condition data to the database
@app.route("/addRules", methods=['POST'])
def addRules():
    if request.method == 'POST':
        response_message = ''
        try:
            # Assuming you're sending the rule name and conditions in a JSON format
            data = request.json

            rule_name = data['name']
            conditions = data['conditions']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                
                # Insert the rule
                cur.execute("INSERT INTO rules (name) VALUES (?)", (rule_name,))
                con.commit()
                # Fetch the last inserted rule_id
                rule_id = cur.lastrowid

                # Insert the conditions using the fetched rule_id
                for condition in conditions:
                    cur.execute("INSERT INTO conditions (rule_id, property, operator, value) VALUES (?, ?, ?, ?)",
                                (rule_id, condition['property'], condition['operator'], condition['value']))
                
                con.commit()
                response_message = "Rule and conditions added successfully."

        except Exception as e:
            response_message = f"Error: {str(e)}"
            # con.rollback()

        # finally:
        #     if con:
        #         con.close()

        return {'message': response_message}

@app.route("/deleteRule/<int:rule_id>", methods=['DELETE'])
def deleteRule(rule_id):
    response_message = ''
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            
            # Delete conditions associated with the rule first to maintain referential integrity
            cur.execute("DELETE FROM conditions WHERE rule_id = ?", (rule_id,))
            
            # Then, delete the rule itself
            cur.execute("DELETE FROM rules WHERE rule_id = ?", (rule_id,))
            
            con.commit()
            response_message = f"Rule with ID {rule_id} and its conditions have been deleted successfully."

    except Exception as e:
        response_message = f"Error: {str(e)}"
        # Optionally, you might want to rollback if there's an error
        # con.rollback()

    # Finally is not needed as 'with' context manager takes care of closing the connection
    # But it's here to show where you might handle additional post-operation tasks if necessary
    finally:
        # Additional cleanup or logging can go here if needed
        pass

    return {'message': response_message}


@app.route("/getRules", methods=['GET'])
def getRules():
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = sqlite3.Row  # This enables column access by name
            cur = con.cursor()

            # Fetch all rules
            cur.execute("SELECT * FROM rules")
            rules = cur.fetchall()

            # For each rule, fetch its conditions and append them to the rule's data
            rules_list = []
            for rule in rules:
                rule_dict = dict(rule)  # Convert the row to a dictionary
                cur.execute("SELECT * FROM conditions WHERE rule_id = ?", (rule['rule_id'],))
                conditions = cur.fetchall()
                rule_dict['conditions'] = [dict(condition) for condition in conditions]  # Convert each condition row to a dictionary
                rules_list.append(rule_dict)

        return rules_list

    except Exception as e:
        return {'message': f"Error: {str(e)}"}, 500
    
@app.route("/editRule", methods=['PUT'])
def editRule():
    response_message = ''
    try:
        data = request.json
        rule_id = data['rule_id']
        new_name = data['name']
        new_conditions = data['conditions']

        with sqlite3.connect('database.db') as con:
            cur = con.cursor()

            # Update the rule's name
            cur.execute("UPDATE rules SET name = ? WHERE rule_id = ?", (new_name, rule_id))

            # Remove existing conditions
            cur.execute("DELETE FROM conditions WHERE rule_id = ?", (rule_id,))

            # Insert new conditions
            for condition in new_conditions:
                cur.execute("INSERT INTO conditions (rule_id, property, operator, value) VALUES (?, ?, ?, ?)",
                            (rule_id, condition['property'], condition['operator'], condition['value']))

            con.commit()
            response_message = f"Rule with ID {rule_id} has been updated successfully."

    except Exception as e:
        response_message = f"Error: {str(e)}"
        # Optionally, you might want to rollback if there's an error
        # con.rollback()

    return {'message': response_message}