import traceback

import sqlalchemy
import sys
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from build.lib.gwlib.http.responses import HTTP_SERVER_ERROR
from gwlib.base.errors import UserNotAllowed
from gwlib.http.responses import HTTP_BAD_REQUEST, HTTP_CONFLICT, HTTP_RESPONSE
from gwlib.http.responses import HTTP_NOT_FOUND


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

        print("response", response)
        return HTTP_RESPONSE(response)

