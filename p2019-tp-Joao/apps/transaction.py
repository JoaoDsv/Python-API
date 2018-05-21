from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from models import User, Token, Transaction


app_transaction = Blueprint('app_transaction', __name__)


# List all transactions of all users
@app_transaction.route('/transactions', methods=['GET'])
def list_transaction():
    # Build query to get all transactions as dictionaries
    query = Transaction.select().dicts()

    # Get transactions dictionary and send JSON list to browser
    return jsonify({ 'list_transaction': list(query) }), 200


# List all transactions of one specific user
@app_transaction.route('/users/<id>/transactions', methods=['GET'])
def list_transaction_user(id):
    try:
        # Build query for matching URL's user_id and transaction's user_id, then convert to dictionnary
        query = Transaction.select().where(Transaction.user_id == id).dicts()

        # Send JSON list to browser
        return jsonify({ 'list_transaction_user': list(query) }), 200

    # Catch error if request fails
    except Exception as error:
        print error

        # Send error to browser
        return jsonify({ 'error': 'Not found' }), 404


# Get one specific transaction
@app_transaction.route('/transactions/<id>', methods=['GET'])
def one_transaction(id):
    try:
        # Build query to get transaction by URL id
        transaction = Transaction.get(Transaction.id == id)

        # Convert to dictionnary & send JSON to browser
        one_transaction = model_to_dict(transaction)
        return jsonify({ 'one_transaction': one_transaction }), 200

    # Catch error if request fails
    except Exception as error:
        print error

        # Send error to browser
        return jsonify({ 'error': 'Not found' }), 404


# Create a new transaction linked to a specific user
@app_transaction.route('/transactions', methods=['POST'])
def create_transaction():
    try:
        # Get params from request
        params = request.get_json()

        # Build attributes with sent params
        user_id = params.get('user_id')
        amount = params.get('amount')

        print 'user_id : ', user_id
        print 'amount : ', amount

        # Create and save new transaction
        query = Transaction.create(amount=amount, user_id=user_id)
        query.save()
        transaction = model_to_dict(query)

        # Send newly created transaction to browser in JSON, 201 means 'success'
        return jsonify({ 'new_transaction': transaction }), 201


    # Catch error if request fails
    except Exception as error:
        print error

        # Send error to browser
        return jsonify({ 'error': 'Not found' }), 404
