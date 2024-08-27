import asyncio
import os

import httpx

from pydemy import AsyncUdemyClient
from pydemy.models import Chapter, CourseFilter, Lecture, Quiz


async def main():
    # Replace with your actual client ID and secret
    client_id = "YOUR_CLIENT_ID"
    client_secret = "YOUR_CLIENT_SECRET"

    async with AsyncUdemyClient(client_id, client_secret) as udemy_client:
        # Example 1: Filter courses by search term (async)
        search_term = "Web Development"
        filters = CourseFilter(search=search_term)  # Filter by search term
        courses = await udemy_client.get_courses(filters=filters)

        print(f"\nFound {len(courses)} courses matching the search term '{search_term}':")
        for course in courses:
            print(f"Course ID: {course.id}, Title: {course.title}")

        # Example 2: Get the public course curriculum (async)
        course_id = 12345  # Replace with the actual course ID
        try:
            curriculum = await udemy_client.get_course_public_curriculum(course_id)

            print(f"\nCourse ID: {course_id} - Public Curriculum:")
            for entry in curriculum:
                print(f"\n- Title: {entry.title}")

                # Access details based on entry type
                if isinstance(entry, Chapter):
                    print("\n\t- Type: Chapter")
                    if entry.description:  # Print description if available
                        print(f"\n\t\t- Description: {entry.description}")
                elif isinstance(entry, Lecture):
                    print("\n\t- Type: Lecture")
                    print(f"\n\t- Asset Title: {entry.asset.title}")  # Access lecture asset title
                    if entry.transcript:  # Print transcript if available
                        print("\n\t- Transcript Available (content not shown here)")
                elif isinstance(entry, Quiz):
                    print("\n\t- Type: Quiz")
                    print("\n\t- Duration: {entry.duration} seconds")
                    print("\n\t- Pass Percentage: {entry.pass_percent:.2f}")

        except Exception as exc:
            print(f"Error retrieving course curriculum: {exc}")

        # Example 3: Get course details with image download (async)
        course_id = 12345  # Replace with the actual course ID
        image_url = None

        try:
            course_details = await udemy_client.get_course_details(course_id)
            print(f"\nCourse Details for ID: {course_details.id}")
            print(f"\n\t- Title: {course_details.title}")

            # Check for available image URL
            if course_details.image_480x270:
                image_url = course_details.image_480x270

            if image_url:
                # Download image
                async with httpx.AsyncClient() as http_client:
                    response = await http_client.get(image_url)
                    if response.status_code == 200:
                        # Create a filename with course ID and extension (assuming image)
                        filename = f"course_{course_id}.jpg"
                        image_path = os.path.join("course_images", filename)  # Customize path

                        # Create directory if it doesn't exist
                        os.makedirs(os.path.dirname(image_path), exist_ok=True)

                        with open(image_path, "wb") as f:
                            f.write(await response.read())
                        print(f"Image downloaded and saved as: {image_path}")
                    else:
                        print(f"Error downloading image: {response.status_code}")
            else:
                print("\n- No image URL available for this course")
        except Exception as exc:
            print(f"Error retrieving course details: {exc}")


if __name__ == "__main__":
    asyncio.run(main())
