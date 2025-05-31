import json

from .response import IntoResponse, Response
from .status_code import StatusCode

__all__ = ("HttpException",)


class HttpException(Exception, IntoResponse):
    """Represents an error that occurred while processing a request.

    This exception is used to signal errors in request processing and includes
    a reason for the error and an associated HTTP status code. It implements
    the `IntoResponse` protocol, allowing it to return a properly formatted
    error message suitable for returning from AWS Lambda function handlers.

    Errors are converted into a JSON response with a single field, `error`:

    ```json
    {"error": reason}
    ```

    Where `reason` is the value passed in for the `reason` argument.

    Parameters
    ----------
    reason
        A description of the error that occurred, which will be included in the
        error response body.
    status_code
        The HTTP status code associated with the error. Defaults to
        500 Internal Server Error.
    """

    headers = {
        "Content-Type": "application/json",
    }

    def __init__(
        self,
        reason: str = "Internal server error",
        status_code: StatusCode = StatusCode.HTTP_500_INTERNAL_SERVER_ERROR,
        *args: object,
    ) -> None:
        super().__init__(reason)
        self.content = reason
        self.status_code = status_code

    def into_response(self) -> Response:
        return Response(
            statusCode=self.status_code,
            headers=self.headers,
            body=json.dumps({"error": self.content}),
        )
