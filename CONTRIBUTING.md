# Contributing to Streamlit AI Chat App

Thank you for your interest in contributing! We welcome bug reports, feature requests, and pull requests.

## Getting Started

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally:
    ```bash
    git clone https://github.com/your-username/streamlit-ai-chat.git
    cd streamlit-ai-chat
    ```
3.  **Create a new branch** for your feature or fix:
    ```bash
    git checkout -b feature/my-amazing-feature
    ```

## Development Workflow

We follow a daily workflow to ensure code quality:

1.  **Pull & Analyze**: Start by pulling the latest code and understanding the task.
2.  **Develop**: Make your changes.
    - Follow `flake8` and `black` standards.
    - Write unit tests for new features in `tests/`.
3.  **Test**: Run the test suite to ensure no regressions.
    ```bash
    pytest
    ```
4.  **Review**: Self-review your code for security and best practices.
5.  **Commit**: Use descriptive commit messages.
    ```bash
    git commit -m "Feature: Add support for XYZ"
    ```
6.  **Push**: Push your branch to GitHub.
    ```bash
    git push origin feature/my-amazing-feature
    ```
7.  **Pull Request**: Open a PR against the `main` branch.

## Coding Standards

- **Formatting**: Use `black` for code formatting.
- **Linting**: Use `flake8` to catch errors.
- **Imports**: Organize imports with `isort`.
- **Testing**: We use `pytest`. All new features must include tests.

## Reporting Bugs

Please include:
- A clear description of the issue.
- Steps to reproduce.
- Expected vs. actual behavior.
- Screenshots or logs if applicable.

## License

By contributing, you agree that your contributions will be licensed under the project's license.
