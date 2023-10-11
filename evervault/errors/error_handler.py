from . import evervault_errors as errors


def raise_errors_on_function_run_failure(function_body):
    error = function_body.get("error")
    if (error):
        message = error.get("message")
        stack = error.get("stack")
        id = function_body.get("id")
        if ('The function failed to initialize.' in message):
            raise errors.FunctionInitializationError(message, stack, id)
        raise errors.FunctionRuntimeError(message, stack, id)
    raise errors.UnexpectedError("An unexpected error occurred. Please contact Evervault support")


def raise_errors_on_function_run_request_failure(resp, function_body):
    if resp.status_code >= 200 and resp.status_code < 300:
        return
    code = function_body.get("code")
    detail = function_body.get("detail")

    if code == 'unauthorized':
        raise errors.AuthenticationError(detail)
    if code == 'forbidden':
        raise errors.ForbiddenError(detail)
    if code == 'resource-not-found':
        raise errors.FunctionNotFoundError(detail)
    if code == 'request-timeout':
        raise errors.FunctionTimeoutError(detail)
    if code == 'function-not-ready':
        raise errors.FunctionNotReadyError(detail)
    if code == 'invalid-request':
        raise errors.BadRequestError(detail)
    if code == 'unprocessable-content':
        raise errors.DecryptionError(detail)
    if code == 'function/forbidden-ip':
        raise errors.ForbiddenIPError(detail)
    raise errors.UnexpectedError(detail)


def raise_errors_on_failure(resp, body=None):
    if resp.status_code < 400:
        return
    if resp.status_code == 404:
        raise errors.ResourceNotFound("Resource Not Found")
    elif resp.status_code == 400:
        raise errors.BadRequestError("Bad request")
    elif resp.status_code == 401:
        raise errors.AuthenticationError("Unauthorized")
    elif resp.status_code == 403:
        if (
            "x-evervault-error-code" in resp.headers
            and resp.headers["x-evervault-error-code"] == "forbidden-ip-error"
        ):
            raise errors.ForbiddenIPError("IP is not present in Cage whitelist")
        else:
            raise errors.AuthenticationError("Forbidden")
    elif resp.status_code == 408:
        raise errors.TimeoutError("Request timed out")
    elif resp.status_code == 422:
        raise errors.DecryptionError("Unable to decrypt data")
    elif resp.status_code == 500:
        raise errors.ServerError("Server Error")
    elif resp.status_code == 502:
        raise errors.BadGatewayError("Bad Gateway Error")
    elif resp.status_code == 503:
        raise errors.ServiceUnavailableError("Service Unavailable")
    else:
        raise errors.UnexpectedError(__message_for_unexpected_error_without_type(body))


def __message_for_unexpected_error_without_type(error_details):
    if error_details is not None:
        message = error_details["message"]
        status_code = error_details["statusCode"]
        return (
            "An unexpected error occured. It occurred with the message: %s and http_code: '%s'. Please contact Evervault support"
            % (message, status_code)
        )
    else:
        return "An unexpected error occurred without message or status code. Please contact Evervault support"
