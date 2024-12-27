from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta
import json

app = Flask(__name__)

# Shelf life dictionary (food item name -> shelf life in days)
SHELF_LIFE = {
    "Tomato": 7,
    "Cucumber": 5,
    "Apple": 14,
    "Banana": 7,
    "Carrot": 14,
    "Potato": 30,
    "Onion": 30,
    "Milk": 7,
    "Bread": 3,
    "Lettuce": 5
}

# Load inventory from JSON file
def load_inventory():
    with open('data/inventory.json', 'r') as file:
        return json.load(file)

# Save inventory to JSON file
def save_inventory(inventory):
    with open('data/inventory.json', 'w') as file:
        json.dump(inventory, file)

# Function to calculate expiry date
def calculate_expiry_date(purchase_date, shelf_life):
    purchase_date_obj = datetime.strptime(purchase_date, '%Y-%m-%d')
    expiry_date_obj = purchase_date_obj + timedelta(days=shelf_life)
    return expiry_date_obj.strftime('%Y-%m-%d')

@app.route('/')
def home():
    inventory = load_inventory()
    # Calculate expiry dates for all items
    for item in inventory:
        item['expiry_date'] = calculate_expiry_date(item['purchase_date'], item['shelf_life'])
    return render_template('index.html', inventory=inventory)

@app.route('/add_item', methods=['POST'])
def add_item():
    item_name = request.form['item_name']
    purchase_date = request.form['purchase_date']
    
    # Look up shelf life from the dictionary
    shelf_life = SHELF_LIFE.get(item_name, None)
    
    # If the item is not in the dictionary, return an error message
    if shelf_life is None:
        return f"Error: Shelf life for '{item_name}' not found. Please enter a valid item."
    
    # Calculate expiry date for the new item
    expiry_date = calculate_expiry_date(purchase_date, shelf_life)
    
    inventory = load_inventory()
    inventory.append({
        'name': item_name,
        'purchase_date': purchase_date,
        'shelf_life': shelf_life,
        'expiry_date': expiry_date
    })
    
    save_inventory(inventory)
    return redirect('/')

@app.route('/remove_item', methods=['POST'])
def remove_item():
    item_name = request.form['item_name']
    inventory = load_inventory()
    inventory = [item for item in inventory if item['name'] != item_name]
    save_inventory(inventory)
    return redirect('/')

@app.route('/get_recipes')
def get_recipes():
    # Dummy recipes based on inventory
    recipes = ['Tomato Soup', 'Cucumber Salad']
    return render_template('recipes.html', recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)
