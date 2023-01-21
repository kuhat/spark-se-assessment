import json

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, db
from project.server.models import User

auth_blueprint = Blueprint('auth', __name__)


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def get(self):
        responseObject = {
            'status': 'success',
            'message': 'Request successful but please send an HTTP POST request to register the user.'
        }
        return make_response(jsonify(responseObject)), 201

    def post(self):
        # get the post data
        # req = json.dumps(request.data)
        post_data = request.get_json();
        print(request)
        email = post_data.get('email')
        print(email)
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )

                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                print(auth_token)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                print(str(e))
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202


# define the API resources
registration_view = RegisterAPI.as_view('register_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST', 'GET']
)


class getUsersAPI(MethodView):
    """
        get User Resource
    """

    def get(self):
        users = User.query.all()
        user_data = []
        for user in users:
            user_data.append({
                'email': str(user.email)
            })
        print(str(user_data))
        responseObject = {
            'status': 'success',
            'data': user_data
        }
        return make_response(jsonify(responseObject)), 201


getUsersAPI_api = getUsersAPI.as_view('get_users_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/users/index',
    view_func=getUsersAPI_api,
    methods=['GET']
)
