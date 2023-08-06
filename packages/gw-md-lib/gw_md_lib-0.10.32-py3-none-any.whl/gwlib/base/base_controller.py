import sys
import traceback

import sqlalchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from gwlib.base.errors import UserNotAllowed
from gwlib.http.responses import HTTP_BAD_REQUEST, HTTP_CONFLICT, HTTP_RESPONSE, HTTP_SERVER_ERROR, HTTP_NOT_FOUND


class BaseController:

    def build_response(self, method=None, **kwargs):
        """
        Method to call a Service function and return a Http Response
        :type kwargs: dict
        :type method: function
        """
        try:
            response = method(**kwargs)
        # authentication section
        except UserNotAllowed as e:
            traceback.print_exc(file=sys.stdout)
            print("ERROR", e)
        except KeyError as e:
            print("ERROR", e)
            traceback.print_exc(file=sys.stdout)
            return HTTP_BAD_REQUEST(e)
        except IntegrityError as e:
            print("ERROR", e)
            traceback.print_exc(file=sys.stdout)
            return HTTP_CONFLICT(e)
        except NoResultFound as e:
            print("ERROR", e)
            traceback.print_exc(file=sys.stdout)
            return HTTP_NOT_FOUND({"error": "Not found"})
        except MultipleResultsFound as e:
            print("ERROR", e)
            traceback.print_exc(file=sys.stdout)
            return HTTP_NOT_FOUND({"error": "Not found"})
        except sqlalchemy.exc.InvalidRequestError as e:
            print("ERROR", e)
            traceback.print_exc(file=sys.stdout)
            return HTTP_BAD_REQUEST({"error": str(e)})
        except Exception as e:
            print("ERROR", e)
            traceback.print_exc(file=sys.stdout)
            return HTTP_SERVER_ERROR({"error": str(e)})

        return HTTP_RESPONSE(response)

