"""
Pydantic model representing a Udemy Course object with nested models for price details,
instructors, and locale.
"""

from typing import Any, Dict, List, Optional

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

    job_title: Optional[str] = None
    image_50x50: Optional[str] = None
    image_100x100: Optional[str] = None
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
    price: Optional[str]
    price_detail: Optional[PriceDetail]
    price_serve_tracking_id: Optional[str]
    visible_instructors: List[Instructor]
    image_125_H: str
    image_240x135: str
    is_practice_test_course: bool
    image_480x270: str
    published_title: str
    tracking_id: str = ""
    locale: Locale
    predictive_score: Optional[float] = None
    relevancy_score: Optional[float] = None
    input_features: Optional[Dict[str, Any]] = None
    lecture_search_result: Optional[Dict[str, Any]] = None
    curriculum_lectures: Optional[List[Dict[str, Any]]] = []
    order_in_results: Optional[int] = None
    curriculum_items: Optional[List[Dict[str, Any]]] = []
    headline: Optional[str] = None
    instructor_name: Optional[str] = None
