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

This workflow is triggered by a push into the main branch, commonly after a successful merge, in succession to a successful merge request.

It's purpose is to package the whole application into a `.deb` image file for the `ARMhf` architecture used on raspberry pi.

To accomplish this, the workflow
- builds the application with all dependencies needed
- uses the [_fpm_ package management tool](https://github.com/jordansissel/fpm) to create the image
- proceeds to upload the created image as an artifact to the GitHub repository

The artifact can then be provided as a release on the GitHub home page of the application.

For further documentation on release and versioning please refer to the [Distribution Documentation](./DISTRIBUTION.md).

---

> Back to [DevOps](./_DEV_OPS.md).