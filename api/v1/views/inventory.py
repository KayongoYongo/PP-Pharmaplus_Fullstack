from api.v1.views import app_views
from flask import request, jsonify, abort
from models.inventory import Inventory
from models import storage

@app_views.route('/inventories', methods=['GET'], strict_slashes=False)
def get_inventories():
    """
    Returns all inventories
    """
    inventory_objs = storage.all(Inventory)
    inventories = [obj.to_dict() for obj in inventory_objs.values()]
    
    return jsonify(inventories), 200

@app_views.route('/inventories/<inventory_id>', methods=['GET'], strict_slashes=False)
def get_individual_inventory(inventory_id):
    """"
    Returns indivuidual medicines by id
    """
    inventory = storage.get(Inventory, inventory_id)

    if inventory is None:
        abort(404)
    return jsonify(inventory.to_dict()), 200

@app_views.route('/inventories', methods=['POST'], strict_slashes=False)
def create_inventory():
    """
    The function creates an inventory entity
    """
    # Get data from the request body
    data = request.get_json()

    if data is None:
        abort(400, 'Not a JSON')
    if data.get("quantity") is None:
        abort(400, 'Missing quantity')
    if data.get("medicine_id") is None:
        abort(400, 'Missing medicine id')

    # Create an instance of the customer class
    new_inventory = Inventory(**data)
    
    # Use the storage instance to interact with the database
    new_inventory.save()

    return jsonify(new_inventory.to_dict()), 201

@app_views.route('/inventories/<inventory_id>', methods=['PUT'], strict_slashes=False)
def update_inventory(inventory_id):
    """
    This function updates medicine based on the ID
    """
    inventory = storage.get(Inventory, inventory_id)

    if inventory is None:
        abort(404)

    my_dict = request.get_json()

    if my_dict is None:
        abort(400, 'Not a JSON')

    for k, v in my_dict.items():
        setattr(inventory, k, v)

    storage.save()
    return jsonify(inventory.to_dict()), 200

@app_views.route('/inventories/<inventory_id>', methods=['DELETE'], strict_slashes=False)
def delete_inventory(inventory_id):
    """
    Deletes individual medicine by id
    """
    inventory = storage.get(Inventory, inventory_id)

    if inventory is None:
        abort(404)

    # Deletes the medicine
    storage.delete(inventory)
    storage.save()
    return jsonify({}), 200