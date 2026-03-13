# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-03-13

### Changed
- Changed `/wake` timeout responses to return HTTP `504` instead of HTTP `200`

## [2.0.0] - 2026-03-13

### Changed
- Reduced `/wake` response output to a compact payload with `result` and `duration_seconds`
- Stopped appending per-poll wake progress messages to the API response
- Standardized wake outcomes to `success`, `timeout`, and `error`

## [1.1.0] - 2026-03-06

### Changed
- Refactored wake endpoint to use Python wakeonlan library instead of shell script
- Improved timeout handling to prevent Gunicorn worker timeouts
- Increased Gunicorn worker timeout to 60 seconds

### Removed
- Removed wake_on_lan.sh shell script dependency

## [1.0.1] - 2025-11-24

### Added
- Health endpoint (`GET /health`) for service monitoring and health checks
- Health endpoint returns service status, name, and UTC timestamp

## [1.0.0] - 2025-11-24

### Added
- Initial release of WakeOnLanAPI
- Docker support for containerized deployment
- Wake-on-LAN functionality via REST API
- GitHub Actions workflow for automated Docker image building and publishing
