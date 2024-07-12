# Pydemy

This Python library provides a simple interface to interact with the Udemy API. It allows you to retrieve course information, manage enrollments (if authorized), and potentially explore other functionalities offered by the API.

## Getting Started

1. **Obtain API Credentials**:
   Visit [Udemy API Clients](https://www.udemy.com/user/edit-api-clients/) to create a new API client and obtain your `clientID` and `clientSecret`.

2. **Installation**:
   Install the library using pip:

   ```bash
   pip install pydemy
   ```

3. **Usage**
   Import the `UdemyClient` class:

   ```python
   from pydemy import UdemyClient
   ```

   Initialize the client with your API credentials:

   ```python
   import os

   client_id = os.environ.get('UDEMY_CLIENT_ID')
   client_secret = os.environ.get('UDEMY_CLIENT_SECRET')

   client = UdemyClient(client_id=client_id, client_secret=client_secret)
   ```

## Quickstart

Here is example that demonstrates how to use the `UdemyClient` instance to retrieve information about public courses.

```python
client = UdemyClient(client_id, client_secret)

# Get a list of public courses (replace '4534650' with a specific course ID for details)
courses = client.get_course_public_curriculum(course_id="4534650")

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
