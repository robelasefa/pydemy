"""Pydantic model representing a Udemy User with basic profile information."""

from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    """Pydantic model for a basic User object from the Udemy API."""

    id: Optional[int] = None
    title: Optional[str] = None
    name: Optional[str] = None
    display_name: str
