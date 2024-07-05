"""Pydantic model representing a Quiz object as inferred from the Udemy API response."""

from datetime import datetime

from pydantic import BaseModel


class Quiz(BaseModel):
    """
    Pydantic model representing a Quiz object from the Udemy API response.

    **Note:** This object structure is inferred from the API response and might not be explicitly
    documented by Udemy.
    """

    id: int
    title: str
    type: str
    created: datetime
    description: str
    title_cleaned: str
    is_published: bool
    sort_order: int
    object_index: int
    is_draft: bool
    version: int
    duration: int
    pass_percent: float
