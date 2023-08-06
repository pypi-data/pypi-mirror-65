import sys
import traceback
from functools import wraps

from flask_login import login_user, LoginManager
from sqlalchemy.orm.exc import NoResultFound

from gwlib.base.errors import PolicyRoleInvalid, TypeUserNotDefined
from gwlib.services.base_policy_service import BasePolicyService
from gwlib.services.base_user_service import BaseUserService

try:
    from flask import _app_ctx_stack as ctx_stack, request, current_app, jsonify, g
except ImportError:  # pragma: no cover
    from flask import _request_ctx_stack as ctx_stack
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def resource_by_role(resource_name=None):
    from gwlib.security import method_to_permission

    def resource_by_role_decorator(fn):
        @wraps(fn)
        def resource_by_role_innner(*args, **kwargs):
            base_policy_service = BasePolicyService()
            base_user_service = BaseUserService()
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            type_id = current_user.get("type_id")
            user_id = current_user.get("user_id")
            user = base_user_service.get_by_user_id(user_id=user_id)
            print("user", user)
            try:
                resource_permission = base_policy_service.get_resource_permissions(type_id, resource_name)
                print("resource", resource_permission)
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
                print("PERMISION")
                return jsonify(error=True, msg='User not Allowed'), 403

            g.user = user
            print("aqui")
            # login_user(user)

            return fn(*args, **kwargs)

        return resource_by_role_innner

    return resource_by_role_decorator
