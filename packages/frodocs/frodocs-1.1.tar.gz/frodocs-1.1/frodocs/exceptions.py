from click import ClickException


class FrodocsException(ClickException):
    """Base exceptions for all Frodocs Exceptions"""


class ConfigurationError(FrodocsException):
    """Error in configuration"""
