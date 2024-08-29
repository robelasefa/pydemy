"""
Pydantic model representing a Course Subcategory with a nested CourseCategory model and a static
list of possible subcategories.
"""

from typing import List

from pydantic import BaseModel, Field

from ._course_category import CourseCategory


class CourseSubcategory(BaseModel):
    """Pydantic model for a Course Subcategory on the Udemy API."""

    category: CourseCategory
    sort_order: int
    title: str
    title_cleaned: str = Field(default_factory=lambda t: t.title.lower().replace(" ", "-"))

    # Define a list of possible subcategories
    POSSIBLE_SUBCATEGORIES: List[str] = [
        "3D & Animation",
        "Accounting & Bookkeeping",
        "Affiliate Marketing",
        "Apple",
        "Architectural Design",
        "Arts & Crafts",
        "Beauty & Makeup",
        "Branding",
        "Business Analytics & Intelligence",
        "Business Law",
        "Business Strategy",
        "Career Development",
        "Commercial Photography",
        "Communication",
        "Compliance",
        "Content Marketing",
        "Creativity",
        "Cryptocurrency & Blockchain",
        "Dance",
        "Data Science",
        "Database Design & Development",
        "Design Tools",
        "Digital Marketing",
        "Digital Photography",
        "E-Commerce",
        "Economics",
        "Engineering",
        "Entrepreneurship",
        "Esoteric Practices",
        "Essential Tech Skills",
        "Fashion Design",
        "Finance",
        "Finance Cert & Exam Prep",
        "Financial Modeling & Analysis",
        "Fitness",
        "Food & Beverage",
        "Game Design",
        "Game Development",
        "Gaming",
        "General Health",
        "Google",
        "Graphic Design & Illustration",
        "Growth Hacking",
        "Happiness",
        "Hardware",
        "Home Improvement & Gardening",
        "Human Resources",
        "Humanities",
        "Industry",
        "Influence",
        "Instruments",
        "Interior Design",
        "Investing & Trading",
        "IT Certifications",
        "Language Learning",
        "Leadership",
        "Management",
        "Marketing Analytics & Automation",
        "Marketing Fundamentals",
        "Martial Arts & Self Defense",
        "Math",
        "Media",
        "Meditation",
        "Memory & Study Skills",
        "Mental Health",
        "Microsoft",
        "Mobile Development",
        "Money Management Tools",
        "Motivation",
        "Music Fundamentals",
        "Music Production",
        "Music Software",
        "Music Techniques",
        "Network & Security",
        "No-Code Development",
        "Nutrition & Diet",
        "Online Education",
        "Operating Systems & Servers",
        "Operations",
        "Oracle",
        "Other Business",
        "Other Design",
        "Other Finance & Accounting",
        "Other Health & Fitness",
        "Other IT & Software",
        "Other Lifestyle",
        "Other Marketing",
        "Other Music",
        "Other Office Productivity",
        "Other Personal Development",
        "Other Photography & Video",
        "Other Teaching & Academics",
        "Paid Advertising",
        "Parenting & Relationships",
        "Personal Brand Building",
        "Personal Growth & Wellness",
        "Personal Productivity",
        "Personal Transformation",
        "Pet Care & Training",
        "Photography",
        "Photography Tools",
        "Portrait Photography",
        "Product Marketing",
        "Productivity & Professional Skills",
        "Programming Languages",
        "Project Management",
        "Public Relations",
        "Real Estate",
        "Religion & Spirituality",
        "Safety & First Aid",
        "Sales",
        "SAP",
        "Science",
        "Search Engine Optimization",
        "Self Esteem & Confidence",
        "Social Media Marketing",
        "Social Science",
        "Software Development Tools",
        "Software Engineering",
        "Software Testing",
        "Sports",
        "Stress Management",
        "Taxes",
        "Teacher Training",
        "Test Prep",
        "Travel",
        "User Experience Design",
        "Video & Mobile Marketing",
        "Video Design",
        "Vocal",
        "Vodafone",
        "Web Design",
        "Web Development",
        "Yoga",
    ]