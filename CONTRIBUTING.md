# Contributing to Social Media Platform

Thank you for your interest in contributing to the Social Media Platform! All contributions are welcome. Here are some guidelines to help you get started.

## Code of Conduct

Please follow our [Code of Conduct](CODE_OF_CONDUCT.md) in all interactions.

## How Can I Contribute?

### Reporting Bugs

- Use the issue tracker to report bugs
- Describe the bug in detail with steps to reproduce
- Include information about your environment (OS, Python version, etc.)
- Provide example code that demonstrates the issue if possible

### Suggesting Features

- Use the issue tracker to suggest new features
- Explain the feature and why it would be useful
- Provide examples of how the feature might be used

### Code Contributions

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite (`python manage.py test`)
6. Format your code (`black .`, `isort .`, `ruff check . --fix`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd socialmedia-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pre-commit  # For code quality hooks
   ```

4. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   ```

## Code Quality Standards

### Python Code Style
- Follow [PEP 8](https://pep8.org/) guidelines
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Use [ruff](https://github.com/charliermarsh/ruff) for linting

### Testing
- Write tests for new features
- Ensure all tests pass before submitting a pull request
- Aim for high test coverage

### Documentation
- Document new functions and classes with docstrings
- Update README.md if adding new major features
- Add comments for complex logic

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Add tests for new functionality
3. Ensure test suite passes
4. Review your code for any potential security issues
5. Update documentation as needed
6. Submit your pull request

## Development Guidelines

### Django Best Practices
- Follow Django's coding style
- Use Django's ORM instead of raw SQL when possible
- Implement proper validation
- Follow security best practices
- Use Django's built-in authentication and authorization

### Security Considerations
- Validate all user inputs
- Use Django's built-in protections (CSRF, XSS, etc.)
- Sanitize data properly
- Follow the principle of least privilege

### Performance
- Optimize database queries
- Use caching where appropriate
- Consider pagination for large datasets
- Profile code for bottlenecks

## Getting Help

If you need help:
- Check the existing issues
- Ask questions in your pull request
- Contact the maintainers

Thank you for contributing!