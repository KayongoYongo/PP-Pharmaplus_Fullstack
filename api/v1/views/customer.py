from api.v1.views import app_views
from flask import request, jsonify, abort
from models.customer import Customer
from models import storage

@app_views.route('/customers', methods=['GET'], strict_slashes=False)
def get_customers():
    """
    Returns all customers
    """
    customer_objs = storage.all(Customer)
    customers = [obj.to_dict() for obj in customer_objs.values()]
    
    return jsonify(customers), 200

@app_views.route('/customers/<customer_id>', methods=['GET'], strict_slashes=False)
def get_individual_customers(customer_id):
    """"
    Returns indivuidual customers by id
    """
    customer = storage.get(Customer, customer_id)

    if customer is None:
        abort(404)
    return jsonify(customer.to_dict()), 200

@app_views.route('/customers', methods=['POST'], strict_slashes=False)
def create_customers():
    """
    The function creates a customer
    """
    # Get data from the request body
    data = request.get_json()

    if data is None:
        abort(400, 'Not a JSON')
    if data.get("email") is None:
        abort(400, 'Missing email')
    if data.get("password") is None:
        abort(400, 'Missing password')
    if data.get("age") is None:
        abort(400, 'Missing age')

    # Create an instance of the customer class
    new_customer = Customer(**data)
    
    # Use the storage instance to interact with the database
    new_customer.save()

    return jsonify(new_customer.to_dict()), 201

@app_views.route('/customers/<customer_id>', methods=['PUT'], strict_slashes=False)
def update_customers(customer_id):
    """
    This function updates a customer based on the ID
    """
    customer = storage.get(Customer, customer_id)

    if customer is None:
        abort(404)

    my_dict = request.get_json()

    if my_dict is None:
        abort(400, 'Not a JSON')

    for k, v in my_dict.items():
        setattr(customer, k, v)

    storage.save()
    return jsonify(customer.to_dict()), 200

@app_views.route('/customers/<customer_id>', methods=['DELETE'], strict_slashes=False)
def delete_customers(customer_id):
    """
    Deletes individual customers by id
    """
    customer = storage.get(Customer, customer_id)

    if customer is None:
        abort(404)

    # Deletes the customer
    storage.delete(customer)
    storage.save()
    return jsonify({}), 200