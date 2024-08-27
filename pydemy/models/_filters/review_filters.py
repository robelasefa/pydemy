"""Pydantic model for filtering and retrieving course reviews from the Udemy API."""

from typing import Optional

from pydantic import BaseModel

from .._user import User


class ReviewFilter(BaseModel):
    """Pydantic model for filtering course reviews on the Udemy API."""

    page: Optional[int] = 1
    page_size: Optional[int] = 10
    is_text_review: bool = False
    rating: str = None
    user: User = None
