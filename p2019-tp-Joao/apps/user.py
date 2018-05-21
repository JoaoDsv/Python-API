from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from models import User, Token
from helpers.hash_helper import hash_password, verify_hash, generate_token
import datetime


app_user = Blueprint('app_user', __name__)


# List all users, even deleted ones
@app_user.route('/users/all', methods=['GET'])
def list_user_all():
    # Build query to get all users as dictionaries
    query = User.select().dicts()

    # Send JSON list to browser
    return jsonify({ 'list_user': list(query) }), 200


# List users, without deleted ones
@app_user.route('/users', methods=['GET'])
def list_user():
    # Build query to get valid users as dictionaries
    query = User.select().where(User.is_deleted == False).dicts()

    # Send JSON list to browser
    return jsonify({ 'list_user': list(query) }), 200


# Get one specific user
@app_user.route('/users/<id>', methods=['GET'])
def one_user(id):
    try:
        # Build query to get user by URL id
        user = User.get(User.id == id)

        # Check if user is deleted
        if user.is_deleted == True:
            return "This user has been deleted."
        else:

            # Convert to dictionnary & send JSON to browser
            one_user = model_to_dict(user)
            return jsonify({ 'one_user': one_user }), 200

    # Catch error if request fails
    except Exception as error:
        print error

        # Send error to browser
        return jsonify({ 'error': 'Not found' }), 404


# Create a new user
@app_user.route('/users', methods=['POST'])
def create_user():
    try:
        # Get params from request
        params = request.get_json()

        # Build user attributes with sent params
        username = params.get('username')
        phone = params.get('phone')
        password = params.get('password')

        # Hash password for security
        hashed_password = hash_password(password)

        print 'username : ', username
        print 'phone : ', phone
        print 'password : ', password
        print 'hashed password : ', hashed_password

        # Create and save new user
        query = User.create(username=username, password=hashed_password, phone=phone)
        query.save()
        user = model_to_dict(query)

        # Send newly created user to browser in JSON
        return jsonify({ 'new_user': user }), 201

    # Catch error if request fails
    except Exception as error:
        print error

        # Send error to browser
        return jsonify({ 'error': 'Not found' }), 404


# Update one specific user
@app_user.route('/users/<id>', methods=['PUT'])
def update_user(id):
    try:
        # Build query to get user by URL id
        user = User.get(User.id == id)

        # Check if user is deleted
        if user.is_deleted == True:
            return "This user has been deleted."
        else:

            # Get params from request
            params = request.get_json()

            # Build user attributes with sent params
            if params.get('username', None) is not None:
                user.username = params.get('username')
            if params.get('phone', None) is not None:
                user.phone = params.get('phone')
            if params.get('password', None) is not None:
                user.password = hash_password(params.get('password'))
            user.updated_at = datetime.datetime.now()

            print 'username : ', user.username
            print 'hashed password : ', user.password
            print 'updated at : ', user.updated_at

            user.save()
            updated_user = model_to_dict(user)

            # Send updated user to browser in JSON
            return jsonify({ 'updated_user': updated_user }), 203

    # Catch error if request fails
    except Exception as error:
        print error

        # Send error to browser
        return jsonify({ 'error': 'Not found' }), 404


# Delete one specific user
@app_user.route('/users/delete/<id>', methods=['PUT'])
def delete_user(id):
    try:
        # Build query to get user by URL id
        user = User.select().where(User.id == id)

        # Check if user is deleted
        if user.is_deleted == True:
            return "This user has already been deleted."
        else:

            # Fake deleting an user, updating "is_deleted" field to True
            user.is_deleted = True
            user.updated_at = datetime.datetime.now()
            user.save()

            # Send falsely deleted user to browser in JSON
            deleted_user = model_to_dict(user)
            return jsonify({ 'deleted_user': deleted_user }), 203

    # Catch error if request fails
    except Exception as error:
        print error

        # Send error to browser
        return jsonify({ 'error': 'Not found' }), 404
