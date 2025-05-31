"""
Defines a typed version of the `Event` object passed to the Lambda handler.
"""

from typing import TypedDict

__all__ = ("Event", "RequestContext", "Http")


class Http(TypedDict):
    """Represents the HTTP request details.

    Attributes
    ----------
    method
        The HTTP method used for the request (e.g., GET, POST, etc.).
    path
        The path of the requested resource.
    protocol
        The protocol used for the request (e.g., HTTP/1.1).
    sourceIp
        The IP address of the client making the request.
    userAgent
        The user agent string of the client making the request.
    """

    method: str
    path: str
    protocol: str
    sourceIp: str
    userAgent: str


class RequestContext(TypedDict):
    """Represents the context of the incoming request.

    Attributes
    ----------
    accountId
        The AWS account ID associated with the request.
    apiId
        The API identifier for the request.
    domainName
        The domain name of the API.
    domainPrefix
        The domain prefix for the API.
    http
        The HTTP request details.
    requestId
        A unique identifier for the request.
    routeKey
        The route key for the request.
    stage
        The stage of the API (e.g., dev, prod).
    time
        The time when the request was received, in a human-readable format.
    timeEpoch
        The time when the request was received, in epoch format.
    """

    accountId: str
    apiId: str
    domainName: str
    domainPrefix: str
    http: Http
    requestId: str
    routeKey: str
    stage: str
    time: str
    timeEpoch: int


class Event(TypedDict):
    """Represents the Lambda function's incoming request.

    Attributes
    ----------
    version
        The version of the event format.
    routeKey
        The route key for the request.
    rawPath
        The raw path of the request.
    rawQueryString
        The raw query string of the request.
    headers
        A dictionary of HTTP headers included in the request.
    requestContext
        The context of the request.
    body
        The body of the request, typically containing the payload.
    isBase64Encoded
        Indicates whether the body is Base64-encoded.
    """

    version: str
    routeKey: str
    rawPath: str
    rawQueryString: str
    headers: dict[str, str]
    requestContext: RequestContext
    body: str
    isBase64Encoded: bool
