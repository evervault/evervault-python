class EvervaultError(Exception):
    def __init__(self, message=None, context=None):
        super(EvervaultError, self).__init__(message)
        self.message = message
        self.context = context


class ArgumentError(ValueError, EvervaultError):
    pass


class HttpError(EvervaultError):
    pass


class ResourceNotFound(EvervaultError):
    pass


class AuthenticationError(EvervaultError):
    pass


class TimeoutError(EvervaultError):
    pass


class DecryptionError(EvervaultError):
    pass


class ServerError(EvervaultError):
    pass


class BadGatewayError(EvervaultError):
    pass


class ServiceUnavailableError(EvervaultError):
    pass


class BadRequestError(EvervaultError):
    pass


class UndefinedDataError(EvervaultError):
    pass


class InvalidPublicKeyError(EvervaultError):
    pass


class UnexpectedError(EvervaultError):
    pass


class MissingTeamEcdhKey(EvervaultError):
    pass


class UnknownEncryptType(EvervaultError):
    pass


class CertDownloadError(EvervaultError):
    pass


class ForbiddenIPError(EvervaultError):
    pass


class UnsupportedCurveError(EvervaultError):
    pass
