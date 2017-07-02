from enum import IntEnum
from functools import wraps


class ErrorCode(IntEnum):
    """ Defines the set of possible error codes"""

    OK = 200,               # request was successful
    REQUEST_ERROR = 400,    # request failed
    SERVER_ERROR = 500,     # request caused a server error


class Response:
    """
    Defines a response to be provided to clients. A response is composed of 3 attributes: the error code,
    the message, and the returned value.
    """

    def __init__(self, value, error_code: ErrorCode, message: str):
        self.value = value
        self.error_code = error_code
        self.message = message

    def __eq__(self, other):
        return self.value == other.value and self.error_code == other.error_code and self.message == other.message

    def encode(self):
        """ Encodes the response into a tuple that can be converted by the xmlrpc module to an array """
        return self.value, int(self.error_code), self.message,

    @staticmethod
    def decode(encoded_response: tuple):
        """
        Decodes a response that was encoded using the encode() method above.
        This method should be used by the client to decode a response returned in some request.
        """
        return Response(*encoded_response)

    @staticmethod
    def success(value, message="OK"):
        """ Builds a standard success response """
        return Response(value, error_code=ErrorCode.OK, message=message)

    @staticmethod
    def error(message, code=ErrorCode.REQUEST_ERROR):
        """ Builds an error response. By default it sets the code to a request error. """
        return Response(value=None, error_code=code, message=message)


# noinspection PyPep8Naming
class rpc_response:
    """
    This is supposed to be used as a decorator to convert the return values or raised exceptions to an response that
    can be returned by an RPC method.
    """

    def __init__(self, *request_errors):
        self._request_errors= request_errors

    def __call__(self, func):

        @wraps(func)
        def build_response(*args, **kwargs):

            try:
                value = func(*args, **kwargs)
                return Response.success(value).encode()

            except self._request_errors as exception:
                return Response.error(message=str(exception)).encode()

            except Exception as exception:
                return Response.error(message=str(exception), code=ErrorCode.SERVER_ERROR).encode()

        return build_response
