class PHIAKException(Exception):
    """Base exception."""


class PayloadValidationError(PHIAKException):
    """Invalid payload."""


class PrivacyViolationError(PHIAKException):
    """Raised when a payload violates privacy guardrails."""


class PluginExecutionError(PHIAKException):
    """A plugin failed."""
