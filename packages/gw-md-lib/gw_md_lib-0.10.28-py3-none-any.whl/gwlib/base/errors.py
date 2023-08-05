class ConstErrors:
    FieldRequired = "0001"
    FieldError = "0002"


"""
Authrentication and permission Exceptions
"""


class UserNotAllowed(Exception):
    def __init__(self, user):
        # Call the base class constructor with the parameters it needs
        message = "Wrong User or password: {} ".format(user)
        super().__init__(message)
        # Now for your custom code...


class TypeUserNotDefined(Exception):
    def __init__(self, user):
        # Call the base class constructor with the parameters it needs
        message = "The user {}, has not type defined ".format(user)
        super().__init__(message)
        # Now for your custom code...


class PolicyRoleInvalid(Exception):
    def __init__(self, user):
        # Call the base class constructor with the parameters it needs
        message = "Role policy invalid to user: {} ".format(user)
        super().__init__(message)
        # Now for your custom code...


"""
Fields Exceptions

"""


class FieldRequired(Exception):
    def __init__(self, field, errors):
        # Call the base class constructor with the parameters it needs
        message = "The field {} is required".format(field)
        super().__init__(message)
        # Now for your custom code...
        self.errors = errors


class FieldError(Exception):
    def __init__(self, field, errors):
        # Call the base class constructor with the parameters it needs
        message = "The field {} is wrong".format(field)
        super().__init__(message)
        # Now for your custom code...
        self.errors = errors


class FieldNotInModel(Exception):
    def __init__(self, field, errors):
        # Call the base class constructor with the parameters it needs
        message = "Field {}, Not In Model".format(field)
        super().__init__(message)
        # Now for your custom code...
        self.errors = errors
