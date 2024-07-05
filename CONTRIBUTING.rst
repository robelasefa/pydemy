Contributing to Pydemy
=======================

Setting Up
----------

1. **Fork the `pydemy` repository** to your GitHub account.

2. **Clone your forked repository**:

   .. code-block:: bash

      $ git clone https://github.com/robelasefa/pydemy --recursive
      $ cd pydemy

3. **Add a remote to the original repository**:

   .. code-block:: bash

      $ git remote add upstream https://github.com/robelasefa/pydemy

4. **Install dependencies**:

   .. code-block:: bash

      $ pip install -r requirements.txt

5. **Install pre-commit hooks**:

   These hooks help enforce code style and formatting before committing.

   .. code-block:: bash

      $ pre-commit install

Finding Tasks
-------------

Check the `issue tracker`_ for ideas or create a new issue if you have something in mind. Comment on the issue to let us know you’re working on it.

Making Changes
--------------

1. **Create a branch** for your feature:

   .. code-block:: bash

      $ git fetch upstream
      $ git checkout master
      $ git merge upstream/master
      $ git checkout -b your-branch-name

2. **Make your changes**. Each commit should be self-contained with a clear message. Follow `PEP 8 Style Guide`_ and use type hints.

3. **Commit your changes**:

   .. code-block:: bash

      $ git add your-file-changed.py
      $ git commit -m "Your commit message"

4. **Push to your fork**:

   .. code-block:: bash

      $ git push origin your-branch-name

Creating a Pull Request
-----------------------

1. **Open a pull request** from your branch on GitHub.
2. **Describe your changes** in the pull request.
3. **Respond to feedback** and make necessary changes.

Cleaning Up
-----------

1. **Delete your branch** after the pull request is merged:

   .. code-block:: bash

      $ git branch -D your-branch-name
      $ git push origin --delete your-branch-name

Style Guide
-----------

- Write `assert` statements as `assert actual == expected`.
- Use keyword arguments for optional parameters.

Continuous Integration
-----------

This project might use a Continuous Integration (CI) service like Travis CI or GitHub Actions.
When you create a pull request, your changes will be automatically tested on the CI server.

Additional Resources
-----------

.. _`issue tracker`: https://github.com/robelasefa/pydemy/issues
.. _`PEP 8 Style Guide`: https://www.python.org/dev/peps/pep-0008/