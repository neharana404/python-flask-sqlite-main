# Flask Rules Engine Service Documentation

## Overview

This Flask app, serves as a Rules Engine Service utilizing SQLite3 to perform Create, Read, Update, and Delete (CRUD) operations. The service allows users to define and manipulate rules, which consist of conditions that, when met, trigger defined actions.

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
9. Before using the application, you need to set up the database and create the necessary tables. This project includes a Python script `create_table.py` that        automates this process.
   ```bash
   python create_table.py

## Viewing the Database in VS Code

To view and interact with the SQLite database directly within Visual Studio Code, you can use the SQLite extension. This extension allows you to run SQLite queries and view the database structure and data within VS Code.

### Installing the SQLite Extension in VS Code

1. **Open Visual Studio Code** and navigate to the Extensions view by clicking on the Extensions icon in the Activity Bar on the side of the window or pressing `Ctrl+Shift+X`.

2. **Search for SQLite**: In the Extensions view search box, type "SQLite" and look for the SQLite extension by alexcvzz (or another if you prefer).

3. **Install the Extension**: Click on the Install button to install the SQLite extension.

### Using the SQLite Extension to View the Database

1. **Open the Command Palette**: Press `Ctrl+Shift+P` to open the Command Palette.

2. **Open Database**: Type `SQLite: Open Database` in the command palette and select the command. Then, navigate to your project's database file (typically with a `.db` extension) and open it.

3. **View and Run Queries**: With the database opened, you can view its structure in the SQLite Explorer, run queries, and see the results directly in VS Code.

    - To run a query, open a new SQL file, type your query, and then right-click on the query text and select "Run Query".
    - To view the database structure, use the SQLite Explorer which should now show the structure of the opened database.

## Backend Testing

The backend of the Flask application is equipped with a series of tests to ensure the correctness and robustness of the rules engine. These tests are written using the `pytest` framework.

Ensure you have pytest installed in your environment to run the tests. If you haven't installed pytest, you can do so by running:

```bash
pip install pytest

### Test Files

The tests are organized into separate files based on the functionalities they cover:

- `test_add_rule.py`: Tests the addition of new rules to the system.
- `test_get_rules.py`: Tests the retrieval of all rules from the system.
- `test_edit_rule.py`: Tests the update functionality for existing rules.
- `test_delete_rule.py`: Tests the deletion of rules from the system.

### Running the Tests

To run the tests, navigate to the root directory of the backend and execute the following command:

```bash
pytest



