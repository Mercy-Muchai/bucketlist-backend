from . import auth_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User


class RegistrationView(MethodView):
    """This class registers a new user."""

    def post(self):
        """POST USER"""

        # Query to see if the user already exists
        user = User.query.filter_by(email=request.data['email']).first()

        if not user:
            try:
                post_data = request.data
                email = post_data['email']
                password = post_data['password']
                username = post_data['username']
                first_name = post_data['first_name']
                last_name = post_data['last_name']
                user = User(email=email, password=password, username=username, 
                first_name=first_name, last_name=last_name)
                user.save()

                response = {
                    'message': 'You registered successfully. Please log in.'
                }
                # return a response notifying the user that they registered successfully
                return make_response(jsonify(response)), 201
            except Exception as e:
                # An error occured, therefore return a string message containing the error
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            # There is an existing user. We don't want to register users twice
            # Return a message to the user telling them that they they already exist
            response = {
                'message': 'email already in use. Please login/register.'
            }

            return make_response(jsonify(response)), 202


registration_view = RegistrationView.as_view('register_view')
# Define the rule for the registration url --->  /auth/register
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST'])
