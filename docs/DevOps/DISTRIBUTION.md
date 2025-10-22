# Distribution

Details on how WAVE is supplied to its users.

## GitHub Releases

The main focus of the distribution process is to make the installation process as easy and hassle free as possible for the potential users. WAVE uses the GitHub Release functionality on the repo start page to distribute all needed ressources.

## Releases

The following releases and installation ressources are provided on GitHub:

### Debian ARMhf Image for Raspberry Pi

The main system, on which WAVE shall be used, is the Raspberry Pi platform with ARMhf architecture. A `.deb` image is provided which can be easily installed and contains everything needed for the application to run right out of the box.

For further information on the GitHub Action workflow packaging this image, please refer to the [GitHub Action Documentation](./GITHUB_ACTIONS.md#release-workflow).

### Docker Image

_planned for future releases_

### Build from source

_planned for future releases_

## Versioning System

WAVE uses Semantic Versioning. It follows the `MAJOR.MINOR.PATCH` format.

- `MAJOR` - breaking changes, incompatibility issues between versions
- `MINOR` - new feature changes, that are backwards compatible
- `PATCH` - smaller bug fixes, that are backwards compatible

---

> Back to [DevOps](./_DEV_OPS.md).