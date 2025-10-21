# Code Styling

## Coding Standards
This project follows the [PEP8](https://peps.python.org/pep-0008/) style guide for Python. All contributions must adhere to this standard.

## Tools
To ensure compliance with the PEP8 standard, the following tools are used in this project.

### VSCode Extensions

- **Pylint Extension**: An extension for VSCode, used for syntax highlighting and code styling. It is advised to use this extension to instantly get a feedback on the quality of your code.

### _pre-commit_ hooks

This project uses _pre-commit_ hooks for different tasks. They are automatically installed and activated in the development setup routine.

Pre-commit hooks provide the opportunity to run certain tools the moment a developer conducts a new commit to their local git branch. This is especially useful to enforce code quality standards and stylings as early as possible, right before the code even enters the version control system.

The following tools are triggered by an respective pre-commit hook. Further detail on the configuration can be found in the _pre-commit-config.yaml_ file at root.

- **Black**: A code formatter for Python that enforces PEP8 by automatically reformatting code. If formatting issues are found, Black modifies the affected files.
When this happens, the commit fails and the changes made by black must be staged to retry the commit.
- **isort**: A Python utility that automatically sorts and organizes imports according to PEP8. If import order issues are found, isort modifies the affected files.
When this happens, the commit fails and the changes made by isort must be staged to retry the commit.

### GitHub Actions
- **Pylint**: Runs as an action when and rates the code from 0 to 10. A score of 10 means the code fully follows the style rules. The pipeline fails if the score is below 8.0.

More details on this workflow are provided [here](./GITHUB_ACTIONS.md).

---

> Back to [DevOps](./_DEV_OPS.md).