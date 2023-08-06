# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2020-02-25
### Added
- Reconfigure CD with Github Actions (includes: package, publish, release)
- Reconfigure CI with Github Actions (includes: lint, test, security scan)
- Support for pre-commit
- GitHub issue templates for Bug report and Feature request
- Badges for the project in README
- Setup CI with Travis
- Test coverage support with Codecov
- Pre-commit hooks
- Pylint / shellcheck code fixes

## [0.1.0] - 2020-04-12
### Added
- More debug logging for (in)valid URL
- Tests for canonical urls
- Tests for (in)valid urls
- Tests for extracting url domain
- Tests for detecting same url domain
- Tests for crawlers detection
- Tests for commands detection
- Tests for crawler command

### Changed
- Regex for valid URL
- Poetry project details
- Updated README

### Fixed
- Logger bug, where log level would not behave as expected if command verbosity level and environment variable are set

## [0.0.5] - 2020-02-24
### Added
- Project skeleton: setup conda for project environment, setup poetry for project dependencies, setup githooks
- Makefile, Bash scripts to handle project setup
- License, README, CHANGELOG
- Docker setup
- Settings, Logs configuration
- Code comments
- CLI setup, available commands: crawl with verbose
- Crawler: Universal breadth first search graph traversal
- Crawler features: Asynchronous calls, page url scraper, same domain url filter, visited urls filter, file type filtering, url length limits, handle relative urls, respect robots.txt file
- Output as graph

[Unreleased]: https://github.com/nichelia/ekrhizoc/compare/0.1.1...HEAD
[0.1.1]: https://github.com/nichelia/ekrhizoc/compare/0.1.0...0.1.1
[0.1.0]: https://github.com/nichelia/ekrhizoc/compare/0.0.5...0.1.0
[0.0.5]: https://github.com/nichelia/ekrhizoc/releases/tag/0.0.5
