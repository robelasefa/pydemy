"""Python library for interacting with the Udemy Affiliate API."""

__author__ = "mertigenet@gmail.com"
__all__ = ["AsyncUdemyClient", "UdemyClient", "_exceptions", "models"]


from . import _exceptions, models
from ._async_client import AsyncUdemyClient
from ._client import UdemyClient
