from pytest import raises

from common.responses import Response, ErrorCode
from tracker_cli.client import decouple_response, RequestError, ServerError


class TestDecoupleResponse:

    def test_SuccessfulResponse_ReturnsResponseValue(self):
        encoded_response = Response.success(value="some value").encode()

        return_value = decouple_response(encoded_response)

        assert return_value == "some value"

    def test_RequestErrorResponse_RaisesRequestErrorWithResponseMessage(self):
        encoded_response = Response.error(message="some message").encode()

        with raises(RequestError):
            decouple_response(encoded_response)

    def test_ServerErrorResponse_RaisesServerErrorWithResponseMessage(self):
        encoded_response = Response.error(message="some message", code=ErrorCode.SERVER_ERROR).encode()

        with raises(ServerError):
            decouple_response(encoded_response)
