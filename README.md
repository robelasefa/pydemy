<h1 align="center">
  <img src="https://raw.githubusercontent.com/robelasefa/pydemy/main/assets/logo.jpg" alt="Pydemy Logo" width="380">
  <br>
</h1>

[![PyPI version](https://img.shields.io/pypi/v/pydemy)](https://pypi.org/project/pydemy/)
[![Python versions](https://img.shields.io/pypi/pyversions/pydemy)](https://pypi.org/project/pydemy/)
[![Udemy API version](https://img.shields.io/badge/Udemy%20API-v2.0-blue)](https://www.udemy.com/developers/affiliate)
[![PyPI Monthly Downloads](https://img.shields.io/pypi/dm/pydemy)](https://pypistats.org/packages/pydemy)
[![Publish to PyPI](https://github.com/robelasefa/pydemy/actions/workflows/release_pypi.yml/badge.svg)](https://github.com/robelasefa/pydemy/actions/workflows/release_pypi.yml)
[![GitHub issues](https://img.shields.io/github/issues/robelasefa/pydemy)](https://github.com/robelasefa/pydemy/issues)
[![License](https://img.shields.io/github/license/robelasefa/pydemy)](https://github.com/robelasefa/pydemy/blob/main/LICENSE)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/robelasefa/pydemy/main.svg)](https://results.pre-commit.ci/latest/github/robelasefa/pydemy/main)

Pydemy provides a convenient way to interact with the **[Udemy Affiliate API](https://www.udemy.com/developers/affiliate)** from your Python applications. You can use Pydemy to search for courses, retrieve course details, fetch reviews, and potentially explore other functionalities offered by the API.

## Udemy API Support

Pydemy currently supports the **Udemy Affiliate API v2.0**. This API allows developers to access public information about Udemy courses.

**Note**: The [Udemy Instructor API](https://www.udemy.com/developers/instructor/), which provides functionalities specific to course creation and management, is not currently supported by Pydemy.

## Main Features

- **Synchronous and Asynchronous API Requests**: Choose between synchronous and asynchronous interactions with the Udemy API. This flexibility caters to different development needs and preferences. To enhance application performance, for example, employ asynchronous calls for non-blocking activities.
- **Search for Courses**: Quickly find courses using a variety of parameters, such as price filters, categories, or keywords.
- **Get Detailed Course Information**: Get in-depth information on a particular course, such as the title, curriculum, teacher, ratings, and more.
- **Get Course Reviews**: By retrieving and examining reviews for a specific course, you can learn a great deal about the experiences of students.
- **Use Pydantic for Data Management and Validation**: The `pydemy` library makes extensive use of the potent Pydantic library. It offers an organized method of working with the data and guarantees that the information obtained from the Udemy API is accurate. This facilitates robust interactions with the Udemy API and makes programming easier.

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

Here is an example that demonstrates how to get started with using the `UdemyClient` to retrieve information about public courses.

**For more in-depth examples and usage scenarios, be sure to check out the `examples` folder.**

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
