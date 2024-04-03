from api.v1.views import app_views
from flask import request, jsonify, abort
from models.order import Order
from models import storage

@app_views.route('/orders', methods=['GET'], strict_slashes=False)
def get_orders():
    """
    Returns all orders
    """
    order_objs = storage.all(Order)
    orders = [obj.to_dict() for obj in order_objs.values()]
    
    return jsonify(orders), 200

@app_views.route('/orders/<order_id>', methods=['GET'], strict_slashes=False)
def get_individual_order(order_id):
    """"
    Returns indivuidual orders by id
    """
    order = storage.get(Order, order_id)

    if order is None:
        abort(404)
    return jsonify(order.to_dict()), 200

@app_views.route('/orders', methods=['POST'], strict_slashes=False)
def create_order():
    """
    The function creates an order entity
    """
    # Get data from the request body
    data = request.get_json()

    if data is None:
        abort(400, 'Not a JSON')
    if data.get("customer_id") is None:
        abort(400, 'Missing customer_id')
    if data.get("medicine_id") is None:
        abort(400, 'Missing medicine id')
    if data.get("quantity") is None:
        abort(400, 'Missing quantity')
    if data.get("total_amount") is None:
        abort(400, 'Missing total_amount')
    if data.get("status") is None:
        abort(400, 'Missing status')

    # Create an instance of the order class
    new_order = Order(**data)
    
    # Use the storage instance to interact with the database
    new_order.save()

    return jsonify(new_order.to_dict()), 201

@app_views.route('/orders/<order_id>', methods=['PUT'], strict_slashes=False)
def update_order(order_id):
    """
    This function updates orders based on the ID
    """
    order = storage.get(Order, order_id)

    if order is None:
        abort(404)

    my_dict = request.get_json()

    if my_dict is None:
        abort(400, 'Not a JSON')

    for k, v in my_dict.items():
        setattr(order, k, v)

    storage.save()
    return jsonify(order.to_dict()), 200

@app_views.route('/orders/<order_id>', methods=['DELETE'], strict_slashes=False)
def delete_order(order_id):
    """
    Deletes individual order by id
    """
    order = storage.get(Order, order_id)

    if order is None:
        abort(404)

    # Deletes the order
    storage.delete(order)
    storage.save()
    return jsonify({}), 200