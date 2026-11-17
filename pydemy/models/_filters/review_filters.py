"""Pydantic model for filtering and retrieving course reviews from the Udemy API."""

from pydantic import BaseModel, field_validator

from .._user import User


class ReviewFilter(BaseModel):
    """Pydantic model for filtering course reviews on the Udemy API."""

    page: int | None = 1
    page_size: int | None = 10
    is_text_review: bool = False
    rating: int | None = None
    user: User | None = None

    @field_validator("rating")
    @classmethod
    def _validate_rating(cls, value):
        if value is None:
            return value
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("rating must be between 1 and 5")
        return value
