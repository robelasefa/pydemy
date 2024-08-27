from pydemy import UdemyClient
from pydemy.models import CourseFilter, Price

# Replace with your actual client ID and secret
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

# Create a Udemy client object
client = UdemyClient(client_id, client_secret)

# Example 1: Filter courses by search term
search_term = "AI Development"
filters = CourseFilter(search=search_term)  # Filter by search keyword
courses = client.get_courses(filters=filters)

print(f"\nFound {len(courses)} courses matching the search term '{search_term}':")
for course in courses:
    print(f"\n\t - Course ID: {course.id}, Title: {course.title}")

# Example 2: Filter free courses in a specific category
category = "Photography & Video"
filters = CourseFilter(category=category, price=Price.PRICE_FREE)
free_courses = client.get_courses(filters=filters)

print(f"\nFound {len(free_courses)} free courses in the '{category}' category:")
for course in free_courses:
    print(f"\n\t- Course ID: {course.id}, Title: {course.title}")
    
# Example 3: Get details of a specific course with error handling
course_id = 12345  # Replace with the actual course ID
try:
    course_details = client.get_course_details(course_id)
    print(f"\nCourse Details for ID: {course_details.id}")
    print(f"\n\t- Title: {course_details.title}")
    print(f"\n\t- URL: {course_details.url}")
    print(f"\n\t- Instructor: {course_details.instructor_name}")

    # Paid/Free Status
    if course_details.is_paid:
        print("\n\t- Paid Course")
        if course_details.price:
            print(f"\n\t\t- Price: {course_details.price}")
    else:
        print("\n\t- Free Course")

    # Image URL
    if course_details.image_480x270:
        print(f"\n\t- Image URL: {course_details.image_480x270}")

except Exception as exc:
    print(f"Error retrieving course details: {exc}")
