from .decorators import *

method_to_permission = {
    "POST": "can_create",
    "GET": "can_read",
    "DELETE": "can_delete",
    "PUT": "can_update",
}
