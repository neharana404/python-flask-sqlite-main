# Author: Clinton Daniel, University of South Florida
# Date: 4/4/2023
# Description: This python script assumes that you already have
# a database.db file at the root of your workspace.
# This python script will CREATE a table called students 
# in the database.db using SQLite3 which will be used
# to store the data collected by the forms in this app
# Execute this python script before testing or editing this app code. 
# Open a python terminal and execute this script:
# python create_table.py

import sqlite3

conn = sqlite3.connect('database.db')
print("Connected to database successfully")

conn.execute('CREATE TABLE rules (rule_id INTEGER PRIMARY KEY, name TEXT)')
print("Created table successfully!")

conn.execute('CREATE TABLE conditions (condition_id INTEGER PRIMARY KEY, rule_id INTEGER, property TEXT, operator TEXT, value REAL, FOREIGN KEY(rule_id) REFERENCES rules(rule_id))')
print("Created table successfully!")

conn.execute('CREATE TABLE actions (action_id INTEGER PRIMARY KEY, rule_id INTEGER, property TEXT, operator INTEGER, value REAL, FOREIGN KEY(rule_id) REFERENCES rules(rule_id))')
print("Created table successfully!")

conn.close()
