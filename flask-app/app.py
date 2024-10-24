from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Create a new item
@app.route('/item', methods=['POST'])
def create_item():
    item_name = request.json.get('name')
    if not item_name:
        return jsonify({"error": "Name is required"}), 400
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO items (name) VALUES (?)', (item_name,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Item created", "item": {"name": item_name}}), 201

# Read an item by ID
@app.route('/item/<int:item_id>', methods=['GET'])
def read_item(item_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
    item = cursor.fetchone()
    conn.close()

    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    return jsonify({"id": item[0], "name": item[1]}), 200

# Update an item by ID
@app.route('/item/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item_name = request.json.get('name')
    if not item_name:
        return jsonify({"error": "Name is required"}), 400
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE items SET name = ? WHERE id = ?', (item_name, item_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Item updated", "item": {"id": item_id, "name": item_name}}), 200

# Delete an item by ID
@app.route('/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Item deleted"}), 200

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(host='0.0.0.0', port=8080)
