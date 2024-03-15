# Flask Rules Engine Service Documentation

## Overview

This Flask app,serves as a Rules Engine Service utilizing SQLite3 to perform Create, Read, Update, and Delete (CRUD) operations. The service allows users to define and manipulate rules, which consist of conditions that, when met, trigger defined actions.

## Features

- **Create Rules**: Add new rules with specified conditions.
- **Read Rules**: Retrieve and view existing rules and their details.
- **Update Rules**: Modify existing rules, including their name and conditions.
- **Delete Rules**: Remove rules from the system.

## Getting Started

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/neharana404/python-flask-sqlite-main.git
2. Navigate to the cloned directory:
   ```bash
   cd python-flask-sqlite-main
4. Install required Python dependencies:
   ```bash
   pip install -r requirements.txt
6. Start the Flask server:
   ```bash
   flask run --port 5001
8. Access the application via http://localhost:5001 in your web browser.

