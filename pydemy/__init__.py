"""Python library for interacting with the Udemy Affiliate API."""

__author__ = "mertigenet@gmail.com"
__all__ = ["models", "exceptions", "UdemyClient"]


from . import exceptions, models
from .client import UdemyClient
