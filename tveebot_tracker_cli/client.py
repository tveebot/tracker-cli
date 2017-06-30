from xmlrpc.client import ServerProxy

from common.responses import Response, ErrorCode
from common.tvshow import TVShow


class ServerError(Exception):
    """ Raised if the response error code corresponds to a server error """


class RequestError(Exception):
    """ Raised if the response error code corresponds to a request error """


class Client:
    """
    The client is responsible for connecting to the daemon and performing the requests. It also handles the responses.
    This client works as an adapter class that translates a response into a returned value or a raised exception.
    If the response indicates the request was successful, then it returns the value received in the response. If the
    response indicates that an error occurred it raises either a RequestError or a ServerError depending on whether
    the error code of the response indicates that a request error or a server error occurred.
    """

    def __init__(self, daemon_url):
        self._daemon = ServerProxy(daemon_url, allow_none=True)

    def add_tvshow(self, tvshow_id):
        """
        Requests the daemon to add a new TV Show to the tracked list.

        :param tvshow_id: the ID of the TV Show to add.
        :return: the TV Show that was added.
        :raises ConnectionError: if it fails to connect to the daemon.
        :raises RequestError: if the daemon indicates that the request was unsuccessful.
        :raises ServerError: if the daemon indicates a Server Error.
        """
        encoded_response = self._daemon.add_tvshow(tvshow_id)
        encoded_tvshow = decouple_response(encoded_response)
        return TVShow(*encoded_tvshow)

    def remove_tvshow(self, tvshow_id):
        """
        Requests the daemon to remove a new TV Show from the tracked list.

        :param tvshow_id: the ID of the TV Show to remove.
        :raises ConnectionError: if it fails to connect to the daemon.
        :raises RequestError: if the daemon indicates that the request was unsuccessful.
        :raises ServerError: if the daemon indicates a Server Error.
        """
        encoded_response = self._daemon.remove_tvshow(tvshow_id)
        return decouple_response(encoded_response)

    def tvshows(self):
        """
        Requests the daemon for the list with all TV Show currently being tracked.

        :return: list with the tv shows being tracked.
        :raises ConnectionError: if it fails to connect to the daemon.
        :raises RequestError: if the daemon indicates that the request was unsuccessful.
        :raises ServerError: if the daemon indicates a Server Error.
        """
        encoded_response = self._daemon.tvshows()
        tvshows = decouple_response(encoded_response)

        # convert the tvshows in tuple format to TV Show objects
        return [TVShow(*tvshow) for tvshow in tvshows]


def decouple_response(encoded_response):
    """
    If the response indicates the request was successful, then it returns the value received in the response. If the
    response indicates that an error occurred it raises either a RequestError or a ServerError depending on whether
    the error code of the response indicates that a request error or a server error occurred.

    :param encoded_response: response returned from a request.
    :return: the value of the response if successful.
    :raises RequestError: if the response error code indicates a request error.
    :raises ServerError: if the response error code indicates a server error.
    """
    response = Response.decode(encoded_response)

    if response.error_code == ErrorCode.OK:
        return response.value

    elif response.error_code == ErrorCode.REQUEST_ERROR:
        raise RequestError(response.message)

    elif response.error_code == ErrorCode.SERVER_ERROR:
        raise ServerError(response.message)
