"""Pydantic model representing a Quiz object as inferred from the Udemy API response."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Quiz(BaseModel):
    """
    Pydantic model representing a Quiz object from the Udemy API response.

    **Note:** This object structure is inferred from the API response and might not be explicitly
    documented by Udemy.
    """

    id: int
    title: Optional[str] = None
    type: Optional[str] = None
    created: Optional[datetime] = None
    description: Optional[str] = None
    title_cleaned: Optional[str] = None
    is_published: bool = False
    sort_order: int = 0
    object_index: int = 0
    is_draft: bool = False
    version: int = 0
    duration: int = 0
    pass_percent: float = 0.0
