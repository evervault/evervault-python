import json
from . import evervault_errors as errors


def raise_errors_on_function_run_failure(function_body):
    error = function_body.get("error")
    if error:
        message = error.get("message")
        stack = error.get("stack")
        id = function_body.get("id")
        raise errors.FunctionRuntimeError(message, stack, id)
    raise errors.EvervaultError(
        "An unexpected error occurred running your Function. Please contact Evervault support"
    )


def raise_errors_on_api_error(resp, response_body):
    if resp.status_code >= 200 and resp.status_code < 300:
        return
    if type(response_body) is not dict:
        try:
            response_body = json.loads(response_body)
        except:
            raise errors.EvervaultError(
                "An unexpected error occurred. Please contact Evervault support"
            )
    code = response_body.get("code")
    detail = response_body.get("detail")

    if code == "functions/request-timeout":
        raise errors.FunctionTimeoutError(detail)
    if code == "functions/function-not-ready":
        raise errors.FunctionNotReadyError(detail)
    raise errors.EvervaultError(detail)


def raise_error_using_status_code(resp, body=None):
    if resp.status_code < 400:
        return
    if resp.status_code == 404:
        raise errors.EvervaultError("Resource not found")
    elif resp.status_code == 400:
        raise errors.EvervaultError("Bad request")
    elif resp.status_code == 401:
        raise errors.EvervaultError("Unauthorized")
    elif resp.status_code == 403:
        if (
            "x-evervault-error-code" in resp.headers
            and resp.headers["x-evervault-error-code"] == "forbidden-ip-error"
        ):
            raise errors.EvervaultError("IP is not present in Function whitelist")
        else:
            raise errors.EvervaultError("Forbidden")
    elif resp.status_code == 408:
        raise errors.FunctionRuntimeError("Request timed out")
    elif resp.status_code == 422:
        raise errors.EvervaultError("Unable to decrypt data")
    elif resp.status_code == 500:
        raise errors.EvervaultError("Server Error")
    elif resp.status_code == 502:
        raise errors.EvervaultError("Bad Gateway Error")
    elif resp.status_code == 503:
        raise errors.EvervaultError("Service Unavailable")
    else:
        raise errors.EvervaultError(__message_for_unexpected_error_without_type(body))


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
