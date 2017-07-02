from hypothesis import given
from hypothesis.strategies import builds, text, sampled_from

from responses import Response, ErrorCode, rpc_response


# noinspection PyUnresolvedReferences
class TestResponse:

    @given(builds(
        Response,
        value=text(),
        error_code=sampled_from(ErrorCode),
        message=text()
    ))
    def test_EncodingAResponseAndThenDecodingItReturnsTheSameResponse(self, response):
        assert Response.decode(response.encode()) == response

    def test_FunctionReturnsAValue_ReturnsSuccessResponseWithTheReturnedValue(self):

        @rpc_response()
        def some_function():
            return 'some value'

        response = some_function()
        response = Response.decode(response)

        assert response.value == 'some value'
        assert response.error_code == ErrorCode.OK
        assert response.message == 'OK'

    def test_FunctionDoesNotReturnAnything_ReturnsSuccessResponseWithValueSetToNone(self):

        @rpc_response()
        def some_function():
            pass

        response = some_function()
        response = Response.decode(response)

        assert response.value is None
        assert response.error_code == ErrorCode.OK
        assert response.message == 'OK'

    def test_FunctionRaisesSomeException_ReturnsRequestErrorResponseWithMessageSetToExceptionMessage(self):

        @rpc_response(ValueError)
        def some_function():
            raise ValueError("some error message")

        response = some_function()
        response = Response.decode(response)

        assert response.error_code == ErrorCode.REQUEST_ERROR
        assert response.message == "some error message"

    def test_FunctionRaisesErrorThatShouldBeAServerError_ResponseErrorCodeIsSetToSERVERERROR(self):

        @rpc_response()
        def some_function():
            raise OSError("some error message")

        response = some_function()
        response = Response.decode(response)

        assert response.error_code == ErrorCode.SERVER_ERROR
        assert response.message == "some error message"
