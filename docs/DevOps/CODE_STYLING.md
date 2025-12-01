# Code Styling

## Coding Standards
This project follows the [PEP8](https://peps.python.org/pep-0008/) style guide for Python. All contributions must adhere to this standard.

**Why is this necessary?**

> Following a defined style guide gives the developers clarity in their work.

Each developer has different opinions on what is considered "clean code". This is due to different technical experiences, view points or simply personal taste.
Different opinions on the matters at hand are welcome, but the decisions emerging need to be clearly defined. If not, meaningful cooperation between different team members is at risk of getting slow and tidious.

Simply put: Code that is easily traversable for Person A can proove quite the challenge for Person B, having a different notion on what the code in front of them probably does. This slows down development, because Person B has to "rethink" what the other person had been thinking when writing their logic.

To avoid unnecessary questions and general confusion, a style guide is used. Each developer has to back down on their personal believes in order to benefit when reviewing the code of the others. Enforcing a style guide also avoids code smells, potential bugs and design issues, which would mean additional work for the team.

## Tools
To ensure compliance with the PEP8 standard, the following tools are used in this project.

### VSCode Extensions

- **pylint Extension**: A pylint extension for VSCode, used for syntax highlighting and code styling. It is advised to use this extension to instantly get a feedback on the quality of your code. The current configuration for pylint can be viewed in the `.pylintrc` file at root.

[pylint](https://pypi.org/project/pylint/) is a static code analyser for Python 2 or 3. It analyzes the written code without actually running it. Analysis includes checking for errors, finding problems in the code and providing suggestions on how the code could be refactored. As with all tools, pylint should only ever support the developer, not making important choices for them.

### _pre-commit_ hooks

This project uses _pre-commit_ hooks for different tasks. They are automatically installed and activated in the development setup routine.

Pre-commit hooks provide the opportunity to run certain tools the moment a developer conducts a new commit to their local git branch. This is especially useful to enforce code quality standards and stylings as early as possible, right before the code even enters the version control system.

The following tools are triggered by an respective pre-commit hook. Further detail on the configuration can be found in the _pre-commit-config.yaml_ file at root.

- **Black**: A code formatter for Python that enforces PEP8 by automatically reformatting code. If formatting issues are found, Black modifies the affected files.
When this happens, the commit fails and the changes made by black must be staged to retry the commit.
- **isort**: A Python utility that automatically sorts and organizes imports according to PEP8. If import order issues are found, isort modifies the affected files.
When this happens, the commit fails and the changes made by isort must be staged to retry the commit.

### GitHub Actions
- **pylint**: Runs and rates the code on a scale from 0 to 10. A score of 10 means the code fully follows the style rules. The pipeline used within this project fails if the score is below `8.0`.
If the code reaches this measure, the code is generally considered to be of decent quality. This way, bigger problems in the code, which slow down development in the long run, can be avoided successfully. On the other hand, this score still gives developers enough room to breath. Nitpicking every little thing is not practical for the software creation process.

More details on this workflow are provided [here](./GITHUB_ACTIONS.md).

---

> Back to [DevOps](./_DEV_OPS.md).