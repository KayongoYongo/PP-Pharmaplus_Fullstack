from api.v1.views import app_views
from flask import request, jsonify, abort
from models.payment import Payment
from models import storage

@app_views.route('/payments', methods=['GET'], strict_slashes=False)
def get_payments():
    """
    Returns all payment instances
    """
    payment_objs = storage.all(Payment)
    payments = [obj.to_dict() for obj in payment_objs.values()]
    
    return jsonify(payments), 200

@app_views.route('/payments/<payment_id>', methods=['GET'], strict_slashes=False)
def get_individual_payments(payment_id):
    """"
    Returns indivuidual payments by id
    """
    payment = storage.get(Payment, payment_id)

    if payment is None:
        abort(404)
    return jsonify(payment.to_dict()), 200

@app_views.route('/payments', methods=['POST'], strict_slashes=False)
def create_payment():
    """
    The function creates a payment instance
    """
    # Get data from the request body
    data = request.get_json()

    if data is None:
        abort(400, 'Not a JSON')
    if data.get("order_id") is None:
        abort(400, 'Missing order id')
    if data.get("customer_id") is None:
        abort(400, 'Missing customer_id')
    if data.get("quantity") is None:
        abort(400, 'Missing quantity')
    if data.get("total_amount") is None:
        abort(400, 'Missing total_amount')
    if data.get("delivery_type") is None:
        abort(400, 'Missing delivery_type')
    if data.get("status") is None:
        abort(400, 'Missing status')

    # Create an instance of the payment class
    new_payment = Payment(**data)
    
    # Use the storage instance to interact with the database
    new_payment.save()

    return jsonify(new_payment.to_dict()), 201

@app_views.route('/payments/<payment_id>', methods=['PUT'], strict_slashes=False)
def update_payment(payment_id):
    """
    This function updates payments based on the ID
    """
    payment = storage.get(Payment, payment_id)

    if payment is None:
        abort(404)

    my_dict = request.get_json()

    if my_dict is None:
        abort(400, 'Not a JSON')

    for k, v in my_dict.items():
        setattr(payment, k, v)

    storage.save()
    return jsonify(payment.to_dict()), 200

@app_views.route('/payments/<payment_id>', methods=['DELETE'], strict_slashes=False)
def delete_payment(payment_id):
    """
    Deletes individual payment by id
    """
    payment = storage.get(Payment, payment_id)

    if payment is None:
        abort(404)

    # Deletes the order
    storage.delete(payment)
    storage.save()
    return jsonify({}), 200