# zmx RPM packaging

RPM spec and CI for building [zmx](https://github.com/neurosnap/zmx) packages on Fedora and RHEL-based distributions.

## Install

Download the latest RPM from the [releases page](https://github.com/engie/zmx-rpm/releases) and install:

```bash
sudo dnf install ./zmx-*.rpm
```

## What's included

- `/usr/bin/zmx`
- Bash, Zsh, and Fish shell completions
- LICENSE, README, and CHANGELOG docs

## Building locally

```bash
# Install build tools
sudo dnf install rpm-build rpmdevtools curl tar xz git gcc glibc-devel

# Set up rpmbuild tree and fetch source
rpmdev-setuptree
version=0.4.1
curl -sL "https://github.com/neurosnap/zmx/archive/v${version}.tar.gz" \
    -o ~/rpmbuild/SOURCES/zmx-${version}.tar.gz

# Build
rpmbuild -bb zmx.spec
```

The RPM will be in `~/rpmbuild/RPMS/`.

## CI

The GitHub Actions workflow builds RPMs for x86_64 and aarch64 on Fedora. It triggers on:

- **Version tags** (`v*`) — builds and attaches RPMs to a GitHub release
- **Manual dispatch** — specify a zmx version to build
