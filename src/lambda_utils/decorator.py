from __future__ import annotations

import functools
import logging
from typing import TYPE_CHECKING

from .error import HttpException
from .response import IntoResponse

if TYPE_CHECKING:
    from typing import Callable, TypeAlias

    from .context import Context
    from .event import Event
    from .response import Response

    LambdaHandler: TypeAlias = Callable[[Event, Context], IntoResponse]

__all__ = ("create_response",)


def create_response(fn: LambdaHandler) -> Callable[[Event, Context], Response]:
    """A decorator for converting an `IntoResponse` into a `Response`."""
    # The following is a bit "clever", so here is a brief explanation.
    #
    # AWS Lambda handlers are expected to return a `dict` formatted in a
    # specific way. A typed version of this dict is implemented as `Response`
    # for use within this context.
    #
    # Instead of complicating function signatures to return `... | Response`
    # when an error may occur, we take a different approach:
    #
    # Helper functions that return a response can return one of several helper
    # types that implement the `IntoResponse` protocol, which is an abstract
    # base class designed to produce the expected `Response` object.
    #
    # If an error occurs, helpers should throw `HttpException`. This exception
    # implements `IntoResponse`, allowing us to return an appropriate response
    # for uncaught errors.

    @functools.wraps(fn)
    def wrapper(event: Event, context: object) -> Response:
        try:
            r = fn(event, context)
            assert isinstance(r, IntoResponse)
            return r.into_response()
        except HttpException as exc:
            assert isinstance(exc, IntoResponse)
            return exc.into_response()
        except Exception as exc:
            logging.root.error(f"An unhandled error occurred: {exc}")
            return HttpException(reason=str(exc)).into_response()

    return wrapper
