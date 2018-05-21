from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from models import User, Token, CodeLogin
from helpers.hash_helper import hash_password, verify_hash, generate_token
import datetime
import nexmo


app_login = Blueprint('app_login', __name__)
client = nexmo.Client(key='', secret='')


# Match user data with request params, send sms code
@app_login.route('/login/send-code', methods=['POST'])
def login_send_code():
    try:
        # Get params from request
        params = request.get_json()

        # Build user attributes with sent params
        login_username = params.get('username')
        login_password = params.get('password')

        print 'login username : ', login_username
        print 'login password : ', login_password

        # Check if username is given
        if login_username == None:
            return 'Missing username.'
        else:

            # Fetch user data, depending of given login username
            user = User.get(User.username == login_username)

            # Check if user is deleted
            if user.is_deleted == True:
                return "This user has been deleted."
            else:

                # Check if user's password match with given login password
                if verify_hash(login_password, user.password) == False:
                    return "Password doesn't match."
                else:

                    # User successfully logged, so build a new login code
                    user_id = user.id
                    code_login = generate_token(2)

                    print 'user_id : ', user_id
                    print 'code login : ', code_login

                    # Send code to user by sms with Nexmo
                    client.send_message({
                      'from': 'Code Login - Python TP',
                      'to': user.phone,
                      'text': code_login,
                    })

                    # Create and save new login code
                    code_query = CodeLogin.create(user_id=user_id, code=code_login)
                    code_query.save()
                    code_login = model_to_dict(code_query)

                    # Send newly created login code to browser in JSON
                    return jsonify({ 'new_code': code_login }), 201

    # Catch error if request fail
    except Exception as error:
        print error

        # Send error to browser
        return jsonify({ 'error': 'Not found' }), 404


# Match sent code with request params, create a token
@app_login.route('/login/verify-code', methods=['POST'])
def login_validate_code():
    try:
        # Get params from request
        params = request.get_json()

        # Build attributes with sent params
        login_username = params.get('username')
        login_code = params.get('code')

        print 'login username : ', login_username
        print 'login code : ', login_code

        # Check if username is given
        if username == None:
            return 'Missing username.'

        # Check if code is given
        if login_code == None:
            return 'Missing code.'
        else:

            # Fetch user data, depending of given login ussername
            user = User.get(User.username == login_username)

            # Fetch code data, depending of given login code
            code = CodeLogin.get(CodeLogin.code == login_code)

            # Check if user is deleted
            if user.is_deleted == True:
                return "This user has been deleted."
            else:

                # Check if user's code match with given login code
                if user.id != code.user_id :
                    return "Code doesn't match."
                else:

                    # User successfully logged, so build a new token
                    user_id = user.id
                    login_token = generate_token(16)

                    print 'user_id : ', user_id
                    print 'token : ', login_token

                    # Create and save new token
                    token_query = Token.create(user_id=user_id, login_token=login_token)
                    token_query.save()
                    token = model_to_dict(token_query)

                    # Send newly created token to browser in JSON
                    return jsonify({'new_token': token }), 201

    # Catch error if request fail
    except Exception as error:
        print error

        # Send error to browser
        return jsonify({ 'error': 'Not found' }), 404
