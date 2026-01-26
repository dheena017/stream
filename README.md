# Streamlit AI Chat App

A multimodal AI chat application built with Streamlit, supporting various providers (Google, OpenAI, Anthropic, etc.) and features like analytics, ethics monitoring, and data backup.

## Project Structure

- `ui/`: User interface and core application logic.
- `tools/`: Utility scripts for analytics and testing.
- `tests/`: Unit and integration tests.
- `scripts/`: Backup and maintenance scripts.
- `logs/`: Application logs.

## Development

### Prerequisites

- Python 3.x
- Dependencies listed in `requirements.txt`

### Running Tests

```bash
pytest
```

### Code Quality

This project uses `flake8`, `black`, and `isort` for code quality.

```bash
flake8 .
black .
isort .
```
