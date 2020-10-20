from . import evervault_errors as errors


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
        raise errors.AuthenticationError("Forbidden")
    elif resp.status_code == 500:
        raise errors.ServerError("Server Error")
    elif resp.status_code == 502:
        raise errors.BadGatewayError("Bad Gateway Error")
    elif resp.status_code == 503:
        raise errors.ServiceUnavailableError("Service Unavailable")
    else:
        raise errors.UnexpectedError(__message_for_unexpected_error_without_type(body))


def __message_for_unexpected_error_without_type(error_details):
    if error_details != None:
        message = error_details["message"]
        status_code = error_details["statusCode"]
        return (
            "An unexpected error occured. It occurred with the message: %s and http_code: '%s'. Please contact Evervault support"
            % (message, status_code)
        )
    else:
        return "An unexpected error occurred without message or status code. Please contact Evervault support"
