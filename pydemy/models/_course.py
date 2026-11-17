"""
Pydantic model representing a Udemy Course object with nested models for price details,
instructors, and locale.
"""

from typing import Any

from pydantic import BaseModel

from ._user import User


class PriceDetail(BaseModel):
    """Pydantic model for a course's price details."""

    amount: float = 0
    currency: str = ""
    price_string: str = ""
    currency_symbol: str = ""


class Instructor(User):
    """Pydantic model for a course instructor inheriting from User."""

    job_title: str | None = None
    image_50x50: str | None = None
    image_100x100: str | None = None
    initials: str | None = None
    url: str | None = None


class Locale(BaseModel):
    """Pydantic model for a course's locale information."""

    locale: str = ""
    title: str | None = None
    english_title: str | None = None
    simple_english_title: str | None = None


class Course(BaseModel):
    """Pydantic model representing a Udemy Course."""

    id: int
    title: str
    url: str | None = None
    is_paid: bool = False
    price: str | None = None
    price_detail: PriceDetail | None = None
    price_serve_tracking_id: str | None = None
    visible_instructors: list[Instructor] = []
    image_125_H: str | None = None
    image_240x135: str | None = None
    is_practice_test_course: bool = False
    image_480x270: str | None = None
    published_title: str | None = None
    tracking_id: str = ""
    locale: Locale | None = None
    predictive_score: float | None = None
    relevancy_score: float | None = None
    input_features: dict[str, Any] | None = None
    lecture_search_result: dict[str, Any] | None = None
    curriculum_lectures: list[dict[str, Any]] | None = []
    order_in_results: int | None = None
    curriculum_items: list[dict[str, Any]] | None = []
    headline: str | None = None
    instructor_name: str | None = None
