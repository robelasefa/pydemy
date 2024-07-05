"""Pydantic model representing a Udemy User with basic profile information."""

from pydantic import BaseModel


class User(BaseModel):
    """Pydantic model for a basic User object from the Udemy API."""

    title: str
    name: str
    display_name: str
