"""Pydantic model representing a Course Category with a static list of possible categories."""

from typing import List

from pydantic import BaseModel


class CourseCategory(BaseModel):
    """Pydantic model for a Course Category on the Udemy API."""

    sort_order: int
    title: str
    title_cleaned: str

    # Define a list of possible categories
    POSSIBLE_CATEGORIES: List[str] = [
        "Business",
        "Design",
        "Development",
        "Finance & Accounting",
        "Health & Fitness",
        "IT & Software",
        "Lifestyle",
        "Marketing",
        "Music",
        "Office Productivity",
        "Personal Development",
        "Photography & Video",
        "Teaching & Academics",
        "Udemy Free Resource Center",
        "Vodafone",
    ]
