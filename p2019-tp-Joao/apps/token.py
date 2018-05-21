from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from models import User, Token


app_token = Blueprint('app_token', __name__)


# List all tokens
@app_token.route('/tokens', methods=['GET'])
def list_token():

    # Build query to get all tokens as dictionaries
    query = Token.select().dicts()

    # Get tokens dictionary and send JSON list to browser
    return jsonify({ 'list_token': list(query) }), 200


# Get one specific token
@app_token.route('/tokens/<id>', methods=['GET'])
def one_token(id):
    try:
        # Build query to get token by URL id
        token = Token.get(Token.id == id)

        # Convert to dictionnary & send JSON to browser
        one_token = model_to_dict(token)
        return jsonify({ 'one_token': one_token }), 200

    # Catch error if request fails
    except Exception as error:
        print error

        # Send error to browser
        return jsonify({ 'error': 'Not found' }), 404
