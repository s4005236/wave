# GitHub Actions

GitHub Actions are automated workflows which are executed within the GitHub repository. They provide a way of automating the software development processes and can be used for _Continues Integration_ / _Continues Deployment_ pipelines.

The actions are defined via `.yml` files within the `.github/workflows` directory.

The current CI/CD setup for WAVE makes use out of the following implemented workflows:

## Pylint workflow

> `pylint.yml`

This workflow is triggered upon a pull/merge request from a development branch into the main branch.

It's purpose is to check the provided code from the development branch. If the code doesn't exceed the required score, the merge request is blocked until the code got refactored.

For more information about so enforced code styling practises, please refer to WAVEs [Code Styling Documentation](./CODE_STYLING.md).

## Release workflow

> `release.yml`

This workflow is triggered by a push into the main branch, commonly after a successful merge after a successful merge request.

It's purpose is to package the whole application into TODO