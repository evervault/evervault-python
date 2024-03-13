class EvervaultError(Exception):
    def __init__(self, message=None, context=None):
        super(EvervaultError, self).__init__(message)
        self.message = message
        self.context = context


class ExceededMaxFileSizeError(EvervaultError):
    pass


class FunctionTimeoutError(EvervaultError):
    pass


class FunctionNotReadyError(EvervaultError):
    pass


class FunctionRuntimeError(EvervaultError):
    def __init__(self, message, stack, id):
        super(EvervaultError, self).__init__(message)
        self.stack = stack
        self.id = id
