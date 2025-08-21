Contributing
============

We welcome contributions to bhopengraph! This document provides guidelines and information for contributors.

Getting Started
--------------

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch** for your changes
4. **Make your changes** following the coding standards
5. **Test your changes** thoroughly
6. **Submit a pull request**

Development Setup
----------------

.. code-block:: bash

   # Clone your fork
   git clone https://github.com/YOUR_USERNAME/bhopengraph.git
   cd bhopengraph

   # Install in development mode
   pip install -e ".[dev]"

   # Run tests
   python -m pytest tests/

   # Run linting
   flake8 bhopengraph/
   black bhopengraph/

Coding Standards
----------------

**Python Code Style**
* Follow PEP 8 style guidelines
* Use type hints where appropriate
* Write docstrings for all public functions and classes
* Keep functions focused and concise

**Documentation**
* Update relevant documentation when adding new features
* Follow the existing documentation style
* Include examples for new functionality
* Update the changelog for significant changes

**Testing**
* Write tests for new functionality
* Ensure all tests pass before submitting
* Aim for good test coverage
* Include both unit tests and integration tests

**Git Commit Messages**
* Use clear, descriptive commit messages
* Start with a verb (Add, Fix, Update, etc.)
* Reference issues when applicable
* Keep commits focused and atomic

Pull Request Guidelines
----------------------

1. **Title**: Clear, descriptive title
2. **Description**: Explain what the PR does and why
3. **Tests**: Ensure all tests pass
4. **Documentation**: Update docs if needed
5. **Changelog**: Update CHANGELOG.md if applicable

Issue Reporting
--------------

When reporting issues, please include:

* **Description**: Clear description of the problem
* **Steps to reproduce**: Detailed steps to reproduce the issue
* **Expected behavior**: What you expected to happen
* **Actual behavior**: What actually happened
* **Environment**: OS, Python version, bhopengraph version
* **Code example**: Minimal code that reproduces the issue

Code of Conduct
---------------

* Be respectful and inclusive
* Focus on the code and technical aspects
* Help others learn and grow
* Report any inappropriate behavior

Getting Help
------------

* **GitHub Issues**: For bug reports and feature requests
* **GitHub Discussions**: For questions and general discussion
* **Pull Requests**: For code contributions

Thank you for contributing to bhopengraph!
