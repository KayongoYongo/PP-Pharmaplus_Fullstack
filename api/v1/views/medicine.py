from api.v1.views import app_views
from flask import request, jsonify, abort
from models.medicine import Medicine
from models import storage

@app_views.route('/medicines', methods=['GET'], strict_slashes=False)
def get_medicines():
    """
    Returns all medicines
    """
    medicine_objs = storage.all(Medicine)
    medicines = [obj.to_dict() for obj in medicine_objs.values()]
    
    return jsonify(medicines), 200

@app_views.route('/medicines/<medicine_id>', methods=['GET'], strict_slashes=False)
def get_individual_medicines(medicine_id):
    """"
    Returns indivuidual medicines by id
    """
    medicine = storage.get(Medicine, medicine_id)

    if medicine is None:
        abort(404)
    return jsonify(medicine.to_dict()), 200

@app_views.route('/medicines', methods=['POST'], strict_slashes=False)
def create_medicine():
    """
    The function creates a medicine entity
    """
    # Get data from the request body
    data = request.get_json()

    if data is None:
        abort(400, 'Not a JSON')
    if data.get("name") is None:
        abort(400, 'Missing name')
    if data.get("dosage") is None:
        abort(400, 'Missing dosage')
    if data.get("cost") is None:
        abort(400, 'Missing cost')
    if data.get("description") is None:
        abort(400, 'Missing description')
    if data.get("storage_conditions") is None:
        abort(400, 'Missing storage_conditions')
    if data.get("manufacturer") is None:
        abort(400, 'Missing manufacturer')  

    # Create an instance of the customer class
    new_medicine = Medicine(**data)
    
    # Use the storage instance to interact with the database
    new_medicine.save()

    return jsonify(new_medicine.to_dict()), 201

@app_views.route('/medicines/<medicine_id>', methods=['PUT'], strict_slashes=False)
def update_medicines(medicine_id):
    """
    This function updates medicine based on the ID
    """
    medicine = storage.get(Medicine, medicine_id)

    if medicine is None:
        abort(404)

    my_dict = request.get_json()

    if my_dict is None:
        abort(400, 'Not a JSON')

    for k, v in my_dict.items():
        setattr(medicine, k, v)

    storage.save()
    return jsonify(medicine.to_dict()), 200

@app_views.route('/medicines/<medicine_id>', methods=['DELETE'], strict_slashes=False)
def delete_medicine(medicine_id):
    """
    Deletes individual medicine by id
    """
    medicine = storage.get(Medicine, medicine_id)

    if medicine is None:
        abort(404)

    # Deletes the medicine
    storage.delete(medicine)
    storage.save()
    return jsonify({}), 200