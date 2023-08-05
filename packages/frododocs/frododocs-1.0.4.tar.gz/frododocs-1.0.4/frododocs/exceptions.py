from __future__ import unicode_literals
from click import ClickException


class FrodoDocsException(ClickException):
    """Base exceptions for all FrodoDocs Exceptions"""


class ConfigurationError(FrodoDocsException):
    """Error in configuration"""
