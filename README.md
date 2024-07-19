# Pydemy

Pydemy provides a convenient way to interact with the **[Udemy Affiliate API](https://www.udemy.com/developers/affiliate)** from your Python applications. You can use Pydemy to search for courses, retrieve course details, fetch reviews, and potentially explore other functionalities offered by the API.

## Udemy API Support

Pydemy currently supports the **Udemy Affiliate API v2.0**. This API allows developers to access public information about Udemy courses.

**Note**: The [Udemy Instructor API](https://www.udemy.com/developers/instructor/), which provides functionalities specific to course creation and management, is not currently supported by Pydemy.

## Main Features

- **Search for Courses**: Easily search for courses based on various criteria like keywords, categories, or
  price filters.
- **Get Detailed Course Information**: Retrieve comprehensive details about a specific course, including
  title, instructor, ratings, curriculum, and more.
- **Fetch Course Reviews**: Gain valuable insights into student experiences by fetching and analyzing reviews
  for particular course.
- **Leverage Pydantic for Data Validation and Management**: Pydantic is a powerful library used throughout the `pydemy` library. It ensures data retrieved from the Udemy API is valid and provides a structured way to work with that data. This simplifies development and promotes robust interactions with the Udemy API.

## Getting Started

1. **Obtain API Credentials**:
   Visit [Udemy API Clients](https://www.udemy.com/user/edit-api-clients/) to create a new API client and obtain your `clientID` and `clientSecret`.

2. **Installation**:
   Install the library using pip:

   ```bash
   pip install pydemy
   ```

3. **Usage**:
   Import the `UdemyClient` class:

   ```python
   from pydemy import UdemyClient
   ```

   Initialize the client with your API credentials:

   ```python
   client_id = "YOUR_CLIENT_ID"
   client_secret = "YOUR_CLIENT_SECRET"

   client = UdemyClient(client_id=client_id, client_secret=client_secret)
   ```

## Quickstart

Here is an example that demonstrates how to use the `UdemyClient` instance to retrieve information about public courses.

```python
client = UdemyClient(client_id="YOUR_CLIENT_ID", client_secret="YOUR_CLIENT_SECRET")

# Get a list of public courses (replace '4534650' with a specific course ID for details)
courses = client.get_public_curriculum_list(course_id=4534650)

# Print course titles
for course in courses:
    print(course.title)
```

## Contributing

We welcome contributions from the community! If you have bug fixes, improvements, or new features, feel free to submit a pull request. For detailed guidelines on contributing, please refer to the [CONTRIBUTING.rst](https://github.com/robelasefa/pydemy/blob/main/CONTRIBUTING.rst) file.

Here's a brief overview:

- Fork the repository.
- Create a new branch for your changes.
- Implement your changes and add unit tests if applicable.
- Follow consistent coding style.
- Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License - see the **[LICENSE.md](https://github.com/robelasefa/pydemy/blob/main/LICENSE)** file for details.
