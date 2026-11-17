"""Pydantic model representing a Udemy User with basic profile information."""

from pydantic import BaseModel


class User(BaseModel):
    """Pydantic model for a basic User object from the Udemy API."""

    id: int | None = None
    title: str | None = None
    name: str | None = None
    display_name: str
