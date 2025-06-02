from __future__ import annotations

import json
from typing import TYPE_CHECKING, Protocol, TypedDict, runtime_checkable

from .status_code import StatusCode

if TYPE_CHECKING:
    from typing import Any, Mapping, MutableMapping

__all__ = ("Response", "IntoResponse", "PlainTextResponse", "JsonResponse")


class Response(TypedDict):
    statusCode: StatusCode
    headers: Mapping[str, str]
    body: str


@runtime_checkable
class IntoResponse(Protocol):
    def into_response(self) -> Response:
        """Convert the current instance into a `Response` object suitable for
        returning from the main AWS Lambda function handler.

        Returns
        -------
        Response
            A typed `dict` that defines the expected entries to be returned by
            the AWS Lambda function.
        """
        raise NotImplementedError


class PlainTextResponse(IntoResponse):
    """Represents an HTTP response with the `application/json` content type.

    Parameters
    ----------
    content
        The contents of the response body.
    status_code
        The HTTP status code associated with this response. Defaults to 200 OK.
    headers
        `Content-Type` is already set; this is for any additional headers.
    """

    def __init__(
        self,
        content: str,
        status_code: StatusCode = StatusCode.HTTP_200_OK,
        headers: MutableMapping[str, str] = {},
    ) -> None:
        self.content = content
        self.status_code = status_code
        headers.setdefault("Content-Type", "text/plain")
        self.headers = headers

    def into_response(self) -> Response:
        return Response(
            statusCode=self.status_code,
            headers=self.headers,
            body=self.content,
        )


class JsonResponse(IntoResponse):
    """Represents an HTTP response with the `application/json` content type.

    Parameters
    ----------
    content
        Represents the response body. WARNING: This object must be serializable
        using `json.dumps`.
    status_code
        The HTTP status code associated with this response. Defaults to 200 OK.
    headers
        `Content-Type` is already set; this is for any additional headers.

    Raises
    ------
    TypeError
        A key or value in `content` is not serializable into valid JSON.
    """

    def __init__(
        self,
        content: Mapping[str, Any] | list[Any] | str | int | bool | None,
        status_code: StatusCode = StatusCode.HTTP_200_OK,
        headers: MutableMapping[str, str] = {},
    ) -> None:
        self.content = json.dumps(content)
        self.status_code = status_code
        headers.setdefault("Content-Type", "application/json")
        self.headers = headers

    def into_response(self) -> Response:
        return Response(
            statusCode=self.status_code,
            headers=self.headers,
            body=self.content,
        )
