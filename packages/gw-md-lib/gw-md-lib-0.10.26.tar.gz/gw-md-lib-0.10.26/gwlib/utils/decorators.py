from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims


class PolicyRoles:
    def __init__(self, resource=None):
        self.resource = resource

    def __call__(self, func):
        def verify_by_resource(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt_claims()
            print(self.resource)
            print(claims)
            if claims['roles'] != 'admin':
                return jsonify(msg='Admins only!'), 403
            else:
                return fn(*args, **kwargs)

        return verify_by_resource()