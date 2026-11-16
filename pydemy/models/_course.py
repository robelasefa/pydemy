"""
Pydantic model representing a Udemy Course object with nested models for price details,
instructors, and locale.
"""

from typing import Any

from pydantic import BaseModel

from ._user import User


class PriceDetail(BaseModel):
    """Pydantic model for a course's price details."""

    amount: float
    currency: str
    price_string: str
    currency_symbol: str


class Instructor(User):
    """Pydantic model for a course instructor inheriting from User."""

    job_title: str | None = None
    image_50x50: str | None = None
    image_100x100: str | None = None
    initials: str
    url: str


class Locale(BaseModel):
    """Pydantic model for a course's locale information."""

    locale: str
    title: str
    english_title: str
    simple_english_title: str


class Course(BaseModel):
    """Pydantic model representing a Udemy Course."""

    id: int
    title: str
    url: str
    is_paid: bool
    price: str | None
    price_detail: PriceDetail | None
    price_serve_tracking_id: str | None
    visible_instructors: list[Instructor]
    image_125_H: str
    image_240x135: str
    is_practice_test_course: bool
    image_480x270: str
    published_title: str
    tracking_id: str = ""
    locale: Locale
    predictive_score: float | None = None
    relevancy_score: float | None = None
    input_features: dict[str, Any] | None = None
    lecture_search_result: dict[str, Any] | None = None
    curriculum_lectures: list[dict[str, Any]] | None = []
    order_in_results: int | None = None
    curriculum_items: list[dict[str, Any]] | None = []
    headline: str | None = None
    instructor_name: str | None = None
