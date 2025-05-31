# Lambda utilities

Functions/classes that make AWS Lambda functions more convenient to work with.

## Installation

To create a Lambda layer containing this library:

```bash
# Install the library into a designated directory (must be named "python/"):
python3 -m pip install git+https://github.com/nicdgonzalez/lambda-utils.git --target python/

# Zip the contents of the directory:
zip -r lambda-utils-layer.zip python/

# Upload the layer to AWS:
aws lambda publish-layer-version \
    --layer-name lambda-utils-layer \
    --zip-file fileb://lambda-utils-layer.zip \
    --compatible-runtimes python3.13

# Clean up:
rm --recursive ./python ./lambda-utils-layer.zip
```

## Example

```python
from __future__ import annotations

from typing import TYPE_CHECKING

from lambda_utils import create_response, StatusCode

if TYPE_CHECKING:
    from lambda_utils import Context, Event, IntoResponse


def parse_request_body(body: str) -> bool:
    # Uh oh! An error is thrown here...
    raise HttpException(
        reason="Expected body to be valid JSON",
        status_code=StatusCode.HTTP_400_BAD_REQUEST,
    )


@create_response
def lambda_handler(event: Event, context: Context, /) -> IntoResponse:
    # Don't worry, `@create_response` catches the error and returns a properly
    # formatted response since `HttpException` also implements `IntoResponse`.
    data = parse_request_body(body=event["body"])

    return JSONResponse(
        content="Hello from Lambda!",
        status_code=StatusCode.HTTP_200_OK,
    )
```
