# GitHub Settings

The following provides a summary over the settings explicitly configured for the WAVE GitHub repository.

## Issue Templates

GitHub provides Issues as a way for the users to interact with the developer team. The WAVE repository provides templates for [bug reports](/.github/ISSUE_TEMPLATE/bug_report.md) and [feature requests](/.github/ISSUE_TEMPLATE/new_feature.md). This is to standardize and organize the way, in which the users turn in their suggestions and feedback, in order to make processing the different support items easier for the maintainers of the project.

Alongside of this, pull request are the usual way, in which contributions start their way into the repository. To ensure, that the changes of each pull request are properly described, a [pull request template](/.github/PULL_REQUEST_TEMPLATE/new_pull_request.md) is also provided.

## Branch Protection

WAVE utilizes branch protection rules to protect the default branch `main`. This restricts users from pushing their code directly to this branch, enforcing the [code review](#code-review) routines described below.
These rules also ensure, that the default branch shall be in a proper, working and clean state at all times because the branch serves as a starting point for all newly created branches. Code, that wasn't properly reviewed shall never be part of the default branch.

Of course those rules slow down the development process a bit. But they are essential, especially to open source repositories. When many different developers contribute to a project with all kinds of changes, branch protection rules are absolutely necessary.

## Code Review

Because of the branch protection rules described above, the only suitable way to push code into the default branch is through pull requests. These are a essential part of the code review process.

After a developer is finished with the changes they worked on inside their branch they open a pull request. Then, there a few checks that must pass, before the changes are merged into the default branch.

- **Code Quality Check**: Before the code is ready to be merged, a code quality check is conducted. The [pylint GitHub Action workflow](GITHUB_ACTIONS.md#pylint-workflow) fulfills this task. If the achieved score for the application with the additional changes is sufficient, the check passes.

- **Conflict Checks**: GitHub automatically 

- **Maintainer Review**: After the automatic checks, the pull request needs to be approved by a number of maintainers in order to be able to be merged in the default branch. The developers engage in a conversation which leaves room for discussion, feedback and criticism. The author of the pull request is able to defend their coding choices or has the opportunity to improve their made changes. After enough developers found the code to be approved, the changes are merged into the default branch. The 

After a sufficient number of developers approved the changes, the pull request can be merged into the default branch. The branch, from which the changes were merged into main, is now no longer needed and is often deleted to keep the number of remote branches in the repository to a manageable amount.

### Copilot Review

_to be configured_


---

> Back to [DevOps](./_DEV_OPS.md).