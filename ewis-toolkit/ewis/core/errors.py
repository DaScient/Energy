class EWISException(Exception):
    """Base exception for EWIS."""


class PayloadValidationError(EWISException):
    """Raised when incoming payload is invalid."""


class PluginExecutionError(EWISException):
    """Raised when a plugin fails in a non-recoverable way."""

