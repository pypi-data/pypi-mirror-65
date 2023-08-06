"""Common RBX exceptions."""


class FatalException(Exception):
    """Raise this exception for non-transient errors.

    These exceptions can be given an extra details object, which may be used by the caller to log
    this as extra information.
    """
    def __init__(self, message='Something went wrong!', details=None):
        super().__init__(message)
        self.details = details

    def to_dict(self):
        rv = {
            'message': str(self)
        }

        if self.details:
            rv['details'] = self.details

        return rv


class Invalid(FatalException):
    """Generic invalid exception."""


class InvalidRequest(Invalid):
    """An Invalid exception with an HTTP status code and a URL."""
    def __init__(self, message, status_code=400, url=None, **kwargs):
        super().__init__(message, **kwargs)
        self.status_code = status_code
        self.url = url

    def to_dict(self):
        rv = super().to_dict()
        if self.url:
            rv['url'] = self.url

        return rv


class ClientException(InvalidRequest):
    """Raised from within the rbx.clients package."""


class InvalidVersion(FatalException):
    """Generic invalid version exception."""


class TransientException(Exception):
    """Raise this exception when we know the cause is transient (e.g.: connection errors,
    consistency error, ...).
    """
