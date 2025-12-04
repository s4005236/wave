# Distribution

Details on how WAVE is supplied to its users.

## GitHub Releases

The main focus of the distribution process is to make the installation process as easy and hassle-free as possible for the potential users. WAVE uses the GitHub Release functionality on the start page of the repository to distribute all needed resources.

## Releases

The following releases and installation resources are provided on GitHub:

### Debian ARMhf Image for Raspberry Pi

The main system on which WAVE shall be used is the Raspberry Pi platform with ARMhf architecture. A `.deb` image is provided that can be easily installed and contains everything needed for the application to run right out of the box.

For further information on the GitHub Action workflow packaging this image, please refer to the [GitHub Action Documentation](./GITHUB_ACTIONS.md#release-workflow).

### Docker Image

_to be implemented_

### Build from source

_to be documented_

## Versioning System

WAVE uses Semantic Versioning. It follows the `MAJOR.MINOR.PATCH` format.

- `MAJOR` - breaking changes, incompatibility issues between versions
- `MINOR` - new feature changes that are backwards compatible
- `PATCH` - smaller bug fixes that are backwards compatible

---

> Back to [DevOps](./_DEV_OPS.md).