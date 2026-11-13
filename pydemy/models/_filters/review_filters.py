"""Pydantic model for filtering and retrieving course reviews from the Udemy API."""

from typing import Optional

from pydantic import BaseModel, field_validator

from .._user import User


class ReviewFilter(BaseModel):
    """Pydantic model for filtering course reviews on the Udemy API."""

    page: Optional[int] = 1
    page_size: Optional[int] = 10
    is_text_review: bool = False
    rating: Optional[int] = None
    user: Optional[User] = None

    @field_validator("rating")
    @classmethod
    def _validate_rating(cls, value):
        if value is None:
            return value
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("rating must be between 1 and 5")
        return value
