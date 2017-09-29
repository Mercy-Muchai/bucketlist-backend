from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# Local imports
from instance.config import app_config

# Initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    from app.models import Bucketlist
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/bucketlists/', methods=['POST', 'GET'])
    def bucketlists():
        if request.method == "POST":
            bucket_name = str(request.data.get('bucket_name', ''))
            if not bucket_name:
                return {
            "message": "You have not added a bucket yet"
            }, 400
            if bucket_name:
                bucketlist = Bucketlist(bucket_name=bucket_name)
                bucketlist.save()
                response = jsonify({
                    'id': bucketlist.id,
                    'bucket_name': bucketlist.bucket_name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                })
                response.status_code = 201
                return response
        else:
            # GET
            bucketlists = Bucketlist.get_all()
            results = []

            for bucketlist in bucketlists:
                obj = {
                    'id': bucketlist.id,
                    'name': bucketlist.bucket_name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response
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
            }, 200

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

    return app
