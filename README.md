# Metacity

[![Build Status](https://github.com/MetacitySuite/Metacity/workflows/Metacity%20CI/badge.svg)](https://github.com/MetacitySuite/Metacity/actions?query=workflow%3A%22Metacity+CI%22)
[![Coverage Status](https://coveralls.io/repos/github/MetacitySuite/Metacity/badge.svg?branch=main)](https://coveralls.io/github/MetacitySuite/Metacity?branch=main)

Toolkit for Urban Data Processing

https://pypi.org/project/metacity/

## Branches
| Branch | Status | Description |
| ------ | ------ | ----------- |
| main   | [![Build Status](https://github.com/MetacitySuite/Metacity/workflows/Metacity%20CI/badge.svg?branch=main)](https://github.com/MetacitySuite/Metacity/actions?query=workflow%3A%22Metacity+CI%22) | protected, merged PRs auto tested and deployed to PyPI |
| dev    | [![Build Status](https://github.com/MetacitySuite/Metacity/workflows/Metacity%20CI/badge.svg?branch=dev)](https://github.com/MetacitySuite/Metacity/actions?query=workflow%3A%22Metacity+CI%22) | merged PRs auto tested and version bumped if tag present |


## PR Merge Commit message conventions
Use any of the following tags in the merge commit message title to indicate the type of PR:

| In commit message | Descrition | Branches |
| ---------------------- | ----------- | ------- |
| `action::bump` | flag to run bump package version | dev |
| `action::package` | flag to run deploy to PyPI | main |

Dev branch actions (together with `action::bump`):

| In commit message | Descrition | Branches |
| ---------------------- | ----------- | ------- |
| `version::patch` | bump version after patch/bug fix/minor change | dev |
| `version::minor` | bump version after new feature/minor change | dev |
| `version::major` | bump version after major change/breaking change | dev |

If no tag is used, no action runs after the PR is merged. If no version tag is used, the version is bumped as patch.


