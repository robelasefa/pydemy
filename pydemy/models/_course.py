"""
Pydantic model representing a Udemy Course object with nested models for price details,
instructors, and locale.
"""

from typing import Any, Dict, List, Optional

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

    job_title: Optional[str] = None
    image_50x50: Optional[str] = None
    image_100x100: Optional[str] = None
    initials: Optional[str] = None
    url: Optional[str] = None


class Locale(BaseModel):
    """Pydantic model for a course's locale information."""

    locale: str = ""
    title: Optional[str] = None
    english_title: Optional[str] = None
    simple_english_title: Optional[str] = None


class Course(BaseModel):
    """Pydantic model representing a Udemy Course."""

    id: int
    title: str
    url: Optional[str] = None
    is_paid: bool = False
    price: Optional[str] = None
    price_detail: Optional[PriceDetail] = None
    price_serve_tracking_id: Optional[str] = None
    visible_instructors: List[Instructor] = []
    image_125_H: Optional[str] = None
    image_240x135: Optional[str] = None
    is_practice_test_course: bool = False
    image_480x270: Optional[str] = None
    published_title: Optional[str] = None
    tracking_id: str = ""
    locale: Optional[Locale] = None
    predictive_score: Optional[float] = None
    relevancy_score: Optional[float] = None
    input_features: Optional[Dict[str, Any]] = None
    lecture_search_result: Optional[Dict[str, Any]] = None
    curriculum_lectures: Optional[List[Dict[str, Any]]] = []
    order_in_results: Optional[int] = None
    curriculum_items: Optional[List[Dict[str, Any]]] = []
    headline: Optional[str] = None
    instructor_name: Optional[str] = None
