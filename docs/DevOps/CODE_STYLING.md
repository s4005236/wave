# Code Styling

## Coding Standards
This project follows the [PEP8](https://peps.python.org/pep-0008/) style code for Python code. Please ensure that your contributions adhere to this standard.

## Tools
To ensure compliance with this standard, the following tools are used in this project:

### Locally (pre-commit)
- **Black**: A code formatter for Python that enforces PEP8 by automatically reformatting code. If formatting issues are found, Black modifies the affected files. The commit fails, and you must stage the changes and retry the commit.
- **isort**: A Python utility that automatically sorts and organizes imports according to PEP8. If import order issues are found, isort modifies the affected files. The commit fails, and you must stage the changes and retry the commit.

### CI/CD
- **Pylint**: Runs as a GitHub Action and rates the code from 0 to 10. A score of 10 means the code fully follows the style rules. The pipeline fails if the score is below 8.0.

---

> Back to [DevOps](./_DEV_OPS.md).