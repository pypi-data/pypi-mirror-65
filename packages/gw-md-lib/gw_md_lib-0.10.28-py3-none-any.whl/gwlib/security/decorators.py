import sys
import traceback
from functools import wraps

from sqlalchemy.orm.exc import NoResultFound

from gwlib.base.errors import PolicyRoleInvalid, TypeUserNotDefined
from gwlib.dao.user_dao import UserDAO

try:
    from flask import _app_ctx_stack as ctx_stack, request, current_app, jsonify
except ImportError:  # pragma: no cover
    from flask import _request_ctx_stack as ctx_stack
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def resource_by_role(resource=None):
    from gwlib.security import method_to_permission

    def resource_by_role_decorator(fn):
        @wraps(fn)
        def resource_by_role_innner(*args, **kwargs):
            user_dao = UserDAO()
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            user_id = current_user.get("user_id")
            print(user_id)
            try:
                resource_permission = user_dao.get_permissions_by_resource(user_id, resource)
                permission = method_to_permission.get(request.method)
            except PolicyRoleInvalid as e:
                print("Error: PolicyRoleInvalid")
                return jsonify(error=True, msg=str(e)), 403
            except TypeUserNotDefined as e:
                print("Error: TypeUserNotDefined")
                return jsonify(error=True, msg=str(e)), 403
            except NoResultFound:
                print("Error: NoResultFound")
                return jsonify(error=True, msg="Invalid User"), 403
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                print("ERROR >>>>>>>", e)
                return jsonify(error=True, msg='User not Allowed'), 403

            if not resource_permission.get(permission):
                return jsonify(error=True, msg='User not Allowed'), 403
            return fn(*args, **kwargs)
        return resource_by_role_innner

    return resource_by_role_decorator
