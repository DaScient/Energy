class WOIKException(Exception):
    """Base exception."""


class PayloadValidationError(WOIKException):
    """Invalid payload."""


class PluginExecutionError(WOIKException):
    """A plugin failed."""
