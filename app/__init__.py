from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response

# Local imports
from instance.config import app_config

# Initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    from app.models import Bucketlist, User
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/bucketlists/', methods=['POST', 'GET'])
    def bucketlists():
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # Go ahead and handle the request, the user is authenticated
                if request.method == "POST":
                    bucket_name = str(request.data.get('bucket_name', ''))
                    belongs_to = int()
                    if not bucket_name:
                        return {
                    "message": "Please add a goal to your bucketlist"
                    }, 404
                    if bucket_name:
                        bucketlist = Bucketlist(bucket_name=bucket_name)
                        bucketlist.belongs_to = user_id
                        bucketlist.save()
                        response = jsonify({
                            'id': bucketlist.id,
                            'bucket_name': bucketlist.bucket_name,
                            'date_created': bucketlist.date_created,
                            'date_modified': bucketlist.date_modified,
                            'belongs_to': user_id
                        })

                        return make_response(response), 201

                else:
                    # GET all buckets
                    bucketlists = Bucketlist.query.filter_by(belongs_to=user_id)
                    results = []

                    for bucketlist in bucketlists:
                        obj = {
                            'id': bucketlist.id,
                            'bucket_name': bucketlist.bucket_name,
                            'date_created': bucketlist.date_created,
                            'date_modified': bucketlist.date_modified,
                            'belongs_to': bucketlist.belongs_to
                        }
                        results.append(obj)

                    return make_response(jsonify(results)), 200
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def bucketlist_manipulation(id, **kwargs):
     # retrieve a buckelist using it's ID
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            return {
                "message": "Oops!Looks like that bucketlist does not exist"
            }, 404

        if request.method == 'DELETE':
            bucketlist.delete()
            return {
                "message": "Bucketlist {} deleted successfully".format(bucketlist.id)
            }, 204

        elif request.method == 'PUT':
            bucket_name = str(request.data.get('bucket_name', ''))
            bucketlist.bucket_name = bucket_name
            bucketlist.save()
            response = jsonify({
                'id': bucketlist.id,
                'bucket_name': bucketlist.bucket_name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': bucketlist.id,
                'bucket_name': bucketlist.bucket_name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            })
            response.status_code = 200
            return response

     # import the authentication blueprint and register it on the app
    from auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
